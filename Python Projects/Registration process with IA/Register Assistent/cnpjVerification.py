# ------------------------------------------------------#
# Data de criação: 2026-05-11
# Autor: Pamela Almeida
# email: pamela.almeidasp@gmail.com
# GitHub: xmel-apa
# linkedin: pamela-almeida-7b6695320
# -------------------------------------------------------#

import re
import requests

#-- Validação do CNPJ

# Importação da API BrasilApi
_BRASILAPI_URL = "https://brasilapi.com.br/api/cnpj/v1/{}"

# Limpeza de formatação do dado
def _limpar(cnpj: str) -> str:
    return re.sub(r'\D', '', cnpj or '')

# Verificação dos dados (Ajustar dependendo da entrada)
def _formato_valido(cnpj: str) -> bool:
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    # Verifica a entrada do digito
    def digito(seq, pesos):
        soma = sum(int(d) * p for d, p in zip(seq, pesos))
        r = soma % 11
        return 0 if r < 2 else 11 - r

    d1 = digito(cnpj[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    d2 = digito(cnpj[:13], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    return d1 == int(cnpj[12]) and d2 == int(cnpj[13])

# Acessa a API e retorna a validação
def validar_cnpj(cnpj: str) -> dict:
    """
    Validates CNPJ format and checks active status on Receita Federal via BrasilAPI.
    Returns dict with 'valido' (bool) and 'situacao'/'motivo' (str).
    """
    # Chamada de Função
    cnpj_limpo = _limpar(cnpj)
    # Chamada de Função
    if not _formato_valido(cnpj_limpo):
        return {'valido': False, 'motivo': 'Dígitos verificadores inválidos'}
    # CallBacks
    try:
        resp = requests.get(_BRASILAPI_URL.format(cnpj_limpo), timeout=15)
    except requests.Timeout:
        return {'valido': False, 'situacao': 'Timeout ao consultar Receita Federal'}
    except requests.RequestException as e:
        return {'valido': False, 'situacao': f'Erro de conexão com Receita Federal: {e}'}

    if resp.status_code == 404:
        return {'valido': False, 'situacao': 'CNPJ não encontrado na Receita Federal'}
    if resp.status_code != 200:
        return {'valido': False, 'situacao': f'Receita Federal retornou HTTP {resp.status_code}'}

    dados = resp.json()
    situacao = dados.get('descricao_situacao_cadastral', '').upper()

    return {
        'valido': situacao == 'ATIVA',
        'situacao': dados.get('descricao_situacao_cadastral', ''),
        'razao_social': dados.get('razao_social', ''),
        'municipio': dados.get('municipio', ''),
        'uf': dados.get('uf', ''),
    }
