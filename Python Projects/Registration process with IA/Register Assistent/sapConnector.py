import os
import re
import logging
import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)

_SAP_BASE  = os.environ.get('SAP_BASE_URL',  'https://SEU_SERVIDOR_SAP/sap/opu/odata/sap/API_BUSINESS_PARTNER')
_SAP_USER  = os.environ.get('SAP_USER',      'SEU_USUARIO')
_SAP_PASS  = os.environ.get('SAP_PASSWORD',  'SUA_SENHA')
_CLIENT    = os.environ.get('SAP_CLIENT',    '100')
_COMP_CODE = os.environ.get('SAP_COMP_CODE', '1000')
_PURCH_ORG = os.environ.get('SAP_PURCH_ORG', '0010')
_RECON_ACC = os.environ.get('SAP_RECON_ACC', '140000')


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _nums(v: str) -> str:
    return re.sub(r'\D', '', v or '')


def _parsear_endereco(endereco: str) -> dict:
    """
    Expects Brazilian format: "Rua X, 123 – Bairro Cidade/UF CEP: 00000-000"
    Uses ViaCEP for city/state enrichment when CEP is present.
    """
    end = {'logradouro': '', 'numero': '', 'bairro': '', 'cidade': '', 'uf': '', 'cep': ''}

    cep_m = re.search(r'\bCEP[:\s]+(\d{5}-?\d{3})', endereco, re.IGNORECASE)
    if cep_m:
        end['cep'] = _nums(cep_m.group(1))

    if end['cep']:
        try:
            r = requests.get(f"https://viacep.com.br/ws/{end['cep']}/json/", timeout=5)
            if r.status_code == 200:
                v = r.json()
                if not v.get('erro'):
                    end['cidade'] = v.get('localidade', '')
                    end['uf']     = v.get('uf', '')
        except Exception:
            pass

    # Street and number come before the dash separator
    antes_traco = re.split(r'\s*[–—\-]\s*', endereco)[0]
    m = re.match(r'^(.+?)[,\s]+(\d+\w*)(?:\s|,|$)', antes_traco)
    if m:
        end['logradouro'] = m.group(1).strip().rstrip(',')
        end['numero']     = m.group(2)

    # Fallback UF from "Cidade/UF" pattern
    if not end['uf']:
        uf_m = re.search(r'/([A-Z]{2})(?:\s|$)', endereco)
        if uf_m:
            end['uf'] = uf_m.group(1)

    # Neighborhood: text between first dash and city name
    if end['cidade']:
        bairro_m = re.search(r'[–—\-]\s*(.+?)\s+' + re.escape(end['cidade']), endereco)
        if bairro_m:
            end['bairro'] = bairro_m.group(1).strip()

    return end


def _sessao() -> requests.Session:
    s = requests.Session()
    s.auth = HTTPBasicAuth(_SAP_USER, _SAP_PASS)
    s.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'sap-client': _CLIENT,
    })
    return s


def _csrf(sessao: requests.Session) -> str:
    r = sessao.get(
        f"{_SAP_BASE}/A_BusinessPartner",
        params={'$top': '1', '$format': 'json'},
        headers={'X-CSRF-Token': 'Fetch'},
        timeout=30,
    )
    r.raise_for_status()
    return r.headers.get('x-csrf-token', '')


def _post(sessao, url, payload, token, timeout=30):
    r = sessao.post(url, json=payload, headers={'X-CSRF-Token': token}, timeout=timeout)
    r.raise_for_status()
    return r.json().get('d', {})


# ---------------------------------------------------------------------------
# main function
# ---------------------------------------------------------------------------

# Chama a função que faz o input dos dados através dos métodos Odata (**Precisar ajustar aqui**)
def criar_fornecedor_odata(dados: dict) -> dict:
    """
    Creates a vendor in SAP S/4HANA via OData API_BUSINESS_PARTNER.

    SharePoint fields expected in 'dados':
        cnpj, empresa, endereco, inscricao_estadual, inscricao_municipal,
        telefone, celular, email, descricao_produto, finalidade,
        banco, agencia, conta, pix, area_solicitante, solicitante,
        email_solicitante, data_cadastro
    """
    sessao = _sessao()

    try:
        token = _csrf(sessao)
    except Exception as e:
        return {'erro': f'Falha ao conectar ao SAP: {e}'}

    end  = _parsear_endereco(dados.get('endereco', ''))
    cnpj = _nums(dados.get('cnpj', ''))

    # 1 – Business Partner (Organization)
    try:
        bp = _post(sessao, f"{_SAP_BASE}/A_BusinessPartner", {
            "BusinessPartnerCategory": "2",
            "BusinessPartnerGrouping": "0001",
            "OrganizationBPName1": dados.get('empresa', ''),
            "SearchTerm1": dados.get('empresa', '')[:20],
            "IndustryKeyDescription": dados.get('finalidade', ''),
        }, token)
        bp_num = bp.get('BusinessPartner', '')
    except requests.HTTPError as e:
        return {'erro': f'Erro ao criar Business Partner: {e.response.text}'}

    if not bp_num:
        return {'erro': 'SAP não retornou número de Business Partner'}

    # 2 – Address
    addr_id = ''
    try:
        addr = _post(sessao, f"{_SAP_BASE}/A_BusinessPartnerAddress", {
            "BusinessPartner": bp_num,
            "StreetName":      end['logradouro'],
            "HouseNumber":     end['numero'],
            "StreetPrefixName": end['bairro'],
            "CityName":        end['cidade'],
            "Region":          end['uf'],
            "PostalCode":      end['cep'],
            "Country":         "BR",
            "Language":        "PT",
        }, token)
        addr_id = addr.get('AddressID', '')
    except requests.HTTPError as e:
        logger.warning(f"Endereço não criado para {bp_num}: {e.response.text}")

    # 3 – Phone numbers
    for phone, default, tipo in [
        (_nums(dados.get('telefone', '')), True,  ''),
        (_nums(dados.get('celular',   '')), False, 'CELL'),
    ]:
        if phone and addr_id:
            payload = {"AddressID": addr_id, "Person": "0",
                       "PhoneNumber": phone, "IsDefaultPhoneNumber": default}
            if tipo:
                payload["PhoneNumberType"] = tipo
            try:
                _post(sessao, f"{_SAP_BASE}/A_AddressPhoneNumber", payload, token, 15)
            except Exception:
                pass

    # 4 – Email
    email = dados.get('email', '')
    if email and addr_id:
        try:
            _post(sessao, f"{_SAP_BASE}/A_AddressEmailAddress", {
                "AddressID": addr_id, "Person": "0",
                "EmailAddress": email, "IsDefaultEmailAddress": True,
            }, token, 15)
        except Exception:
            pass

    # 5 – Tax numbers: CNPJ (BR1) and Inscrição Estadual (BR2)
    for tax_type, tax_val in [
        ("BR1", cnpj),
        ("BR2", _nums(dados.get('inscricao_estadual', ''))),
        ("BR3", _nums(dados.get('inscricao_municipal', ''))),
    ]:
        if tax_val:
            try:
                _post(sessao, f"{_SAP_BASE}/A_BusinessPartnerTaxNumber", {
                    "BusinessPartner": bp_num,
                    "TaxIdType": tax_type,
                    "TaxIdNumber": tax_val,
                }, token, 15)
            except Exception:
                pass

    # 6 – Supplier role
    try:
        _post(sessao, f"{_SAP_BASE}/A_Supplier", {"Supplier": bp_num}, token)
    except requests.HTTPError as e:
        return {'erro': f'Erro ao criar papel Fornecedor: {e.response.text}'}

    # 7 – Company and Purchasing Org
    for url, payload in [
        (f"{_SAP_BASE}/A_SupplierCompany",
         {"Supplier": bp_num, "CompanyCode": _COMP_CODE, "ReconciliationAccount": _RECON_ACC}),
        (f"{_SAP_BASE}/A_SupplierPurchasingOrg",
         {"Supplier": bp_num, "PurchasingOrganization": _PURCH_ORG}),
    ]:
        try:
            _post(sessao, url, payload, token)
        except requests.HTTPError as e:
            logger.warning(f"Dado complementar não salvo ({url}): {e.response.text}")

    # 8 – Banking data (skip when payment is via BOLETO)
    banco  = dados.get('banco',   '').upper().strip()
    agencia = dados.get('agencia', '').upper().strip()
    conta  = dados.get('conta',   '').upper().strip()
    if banco not in ('', 'BOLETO') and agencia not in ('', 'BOLETO'):
        try:
            _post(sessao, f"{_SAP_BASE}/A_BusinessPartnerBank", {
                "BusinessPartner":        bp_num,
                "BankIdentification":     "001",
                "BankCountryKey":         "BR",
                "BankName":               banco,
                "BankNumber":             _nums(agencia),
                "BankAccount":            _nums(conta),
                "BankAccountHolderName":  dados.get('empresa', ''),
            }, token, 15)
        except Exception as e:
            logger.warning(f"Dados bancários não salvos para {bp_num}: {e}")

    return {'sucesso': True, 'codigo_fornecedor': bp_num}
