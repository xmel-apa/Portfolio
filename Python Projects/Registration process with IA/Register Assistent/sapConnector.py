from pyrfc import Connection, ABAPApplicationError, LogonError

def criar_fornecedor_sap(dados: dict):
    try:
        conn = Connection(
            ashost='SEU_SERVIDOR_SAP',  # ou mshost
            sysnr='00',
            client='100',
            user='SEU_USUARIO',
            passwd='SUA_SENHA'
        )
    except LogonError:
        return {'erro': 'Falha na autenticação SAP'}

    general_data = {
        'NAME': dados.get('razao_social'),
        'COUNTRY': dados.get('pais', 'BR'),
        'CITY': dados.get('cidade', ''),
        # demais campos conforme a BAPI
    }
    company_data = {
        'COMP_CODE': dados.get('empresa', '1000'),
        'RECON_ACCT': dados.get('conta_contabil', '140000')
    }
    purchasing_data = {
        'PURCH_ORG': dados.get('org_compras', '0010')
    }

    try:
        result = conn.call('BAPI_VENDOR_CREATE',
                           GENERALDATA=general_data,
                           COMPANYDATA=company_data,
                           PURCHASINGDATA=purchasing_data)
    except ABAPApplicationError as e:
        conn.close()
        return {'erro': f'Erro ABAP: {str(e)}'}

    mensagens = result.get('RETURN', [])
    for msg in mensagens:
        if msg['TYPE'] == 'E':
            conn.call('BAPI_TRANSACTION_ROLLBACK')
            conn.close()
            return {'erro': msg['MESSAGE']}

    # Sucesso
    conn.call('BAPI_TRANSACTION_COMMIT')
    vendor_code = result.get('VENDOR', '')
    conn.close()
    return {'sucesso': True, 'codigo_fornecedor': vendor_code}