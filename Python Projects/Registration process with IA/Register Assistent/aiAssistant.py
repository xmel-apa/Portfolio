import os
import logging
import anthropic
from dotenv import load_dotenv

#-- Estruturação das requisições da API Claude

load_dotenv()
logger = logging.getLogger(__name__)

# Conexão da API
_client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY', ''))

# Prompet de iniciação
_SYSTEM_PROMPT = """Você é um assistente especializado em cadastro de fornecedores para empresas brasileiras.
Sua função é analisar os dados de um novo fornecedor antes de seu cadastro no SAP e identificar:
1. Inconsistências ou campos suspeitos nos dados fornecidos
2. Problemas no endereço (formato incorreto, CEP ausente, etc.)
3. Dados bancários inválidos ou incompletos
4. Qualquer outra irregularidade que possa impedir o cadastro correto

Responda SEMPRE em formato JSON válido com a seguinte estrutura:
{
  "aprovado": true ou false,
  "alertas": ["lista de alertas não críticos"],
  "erros": ["lista de erros que impedem o cadastro"],
  "endereco_normalizado": {
    "logradouro": "...",
    "numero": "...",
    "bairro": "...",
    "cidade": "...",
    "uf": "...",
    "cep": "..."
  },
  "observacoes": "texto livre com observações adicionais"
}

Se não houver alertas ou erros, retorne listas vazias. O campo endereco_normalizado deve conter o endereço
interpretado a partir do texto fornecido, preenchendo os campos que for possível identificar."""

# Função para validação dos dados recebidos no cadastro
def analisar_cadastro(dados: dict, dados_receita: dict = None) -> dict:
    """
    Uses Claude to validate and enrich vendor registration data.

    Args:
        dados: registration fields from the POST request
        dados_receita: enriched data returned by BrasilAPI/Receita Federal (optional)

    Returns:
        dict with keys: aprovado (bool), alertas (list), erros (list),
                        endereco_normalizado (dict), observacoes (str)
    """
    contexto_receita = ""
    if dados_receita and dados_receita.get('razao_social'):
        contexto_receita = f"""
Dados confirmados na Receita Federal:
- Razão Social: {dados_receita.get('razao_social', '')}
- Município: {dados_receita.get('municipio', '')}
- UF: {dados_receita.get('uf', '')}
- Situação: {dados_receita.get('situacao', '')}
"""

    mensagem_usuario = f"""Analise os dados do seguinte fornecedor para cadastro:

CNPJ: {dados.get('cnpj', '')}
Empresa: {dados.get('empresa', '')}
Endereço completo: {dados.get('endereco', '')}
Inscrição Estadual: {dados.get('inscricao_estadual', '')}
Inscrição Municipal: {dados.get('inscricao_municipal', '')}
Telefone: {dados.get('telefone', '')}
Celular: {dados.get('celular', '')}
E-mail: {dados.get('email', '')}
Descrição do produto/serviço: {dados.get('descricao_produto', '')}
Finalidade: {dados.get('finalidade', '')}
Banco: {dados.get('banco', '')}
Agência: {dados.get('agencia', '')}
Conta: {dados.get('conta', '')}
PIX: {dados.get('pix', '')}
Área solicitante: {dados.get('area_solicitante', '')}
Solicitante: {dados.get('solicitante', '')}
{contexto_receita}
Verifique se o nome da empresa informada condiz com a razão social da Receita Federal (se disponível),
se o endereço está completo e em formato brasileiro válido, se os dados bancários são consistentes,
e se há qualquer irregularidade que deva ser alertada antes do cadastro no SAP."""
    
    # Callback
    try:
        response = _client.messages.create(
            model="claude-opus-4-7",
            max_tokens=1024,
            thinking={"type": "adaptive"},
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": mensagem_usuario}],
        )

        texto = next(
            (b.text for b in response.content if b.type == "text"),
            "{}"
        )

        import json
        import re
        json_match = re.search(r'\{[\s\S]*\}', texto)
        if json_match:
            resultado = json.loads(json_match.group())
        else:
            resultado = json.loads(texto)

        resultado.setdefault('aprovado', True)
        resultado.setdefault('alertas', [])
        resultado.setdefault('erros', [])
        resultado.setdefault('endereco_normalizado', {})
        resultado.setdefault('observacoes', '')
        return resultado
    
    # Tratamento de erros
    except Exception as e:
        logger.warning(f"IA indisponível, prosseguindo sem análise: {e}")
        return {
            'aprovado': True,
            'alertas': ['Análise de IA indisponível — cadastro prosseguiu sem revisão automática'],
            'erros': [],
            'endereco_normalizado': {},
            'observacoes': '',
        }
