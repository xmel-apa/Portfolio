# ------------------------------------------------------#
# Data de criação: 2026-05-11
# Autor: Pamela Almeida
# email: pamela.almeidasp@gmail.com
# GitHub: xmel-apa
# linkedin: pamela-almeida-7b6695320
# -------------------------------------------------------#

import logging
import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify
from cnpjVerification import validar_cnpj
from sapConnector import criar_fornecedor_odata
from aiAssistant import analisar_cadastro

#-- Raiz do projeto

# Configurações de logg
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

# Chamada do Flask para roteamento
app = Flask(__name__)

_CAMPOS_OBRIGATORIOS = [
    'cnpj', 'empresa', 'endereco', 'email',
    'telefone', 'area_solicitante', 'solicitante',
]

# Estruturação do método post
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    """
    Receives registration data from Power Automate (SharePoint email bot@dacarto.com.br).

    Expected JSON body:
        cnpj                – "10.636.133/0001-02"
        empresa             – "Pádua E Santos Transportes Ltda"
        endereco            – "Rua X, 123 – Bairro Cidade/UF CEP: 00000-000"
        inscricao_estadual  – "00110915300-68"
        inscricao_municipal – optional
        telefone            – "(035) 3181-0155"
        celular             – "(035) 9.9725-3163"
        email               – "paula@sulmineira.net"
        descricao_produto   – "Serviços"
        finalidade          – "TRANSPORTADORA"
        banco               – "BOLETO" or bank name
        agencia             – "BOLETO" or agency number
        conta               – "BOLETO" or account number
        pix                 – "BOLETO" or pix key
        area_solicitante    – "Expedição/Balança"
        solicitante         – "JOHNNY"
        email_solicitante   – "LOGISTICA@DACARTO.COM.BR"
        data_cadastro       – "06/05/2026"

    Returns 201 on success, 400 on validation error, 500 on SAP error.
    Power Automate reads 'status' field to route email to Processados or Falhas.
    """
    # Retorno de falha ao log
    dados = request.get_json(force=True)
    if not dados:
        return jsonify({'status': 'erro', 'mensagem': 'Corpo da requisição ausente ou inválido'}), 400

    # Retorno de falta de preenchimento de campos
    campos_faltando = [c for c in _CAMPOS_OBRIGATORIOS if not str(dados.get(c, '')).strip()]
    if campos_faltando:
        msg = f'Campos obrigatórios ausentes: {", ".join(campos_faltando)}'
        logger.warning(msg)
        return jsonify({'status': 'erro', 'mensagem': msg}), 400

    cnpj = dados['cnpj']
    logger.info(f"Iniciando cadastro | CNPJ: {cnpj} | Empresa: {dados.get('empresa')}")

    # Validação do CNPJ pela API gov
    validacao = validar_cnpj(cnpj)
    if not validacao['valido']:
        motivo = validacao.get('situacao') or validacao.get('motivo', 'CNPJ inválido')
        logger.warning(f"CNPJ recusado: {cnpj} | Motivo: {motivo}")
        return jsonify({'status': 'erro', 'mensagem': f'CNPJ inválido: {motivo}'}), 400

    logger.info(f"CNPJ {cnpj} aprovado | Situação: {validacao.get('situacao')}")

    # Análise de IA: valida consistência dos dados antes de enviar ao SAP
    analise = analisar_cadastro(dados, dados_receita=validacao)
    if analise['erros']:
        logger.warning(f"IA bloqueou cadastro | CNPJ: {cnpj} | Erros: {analise['erros']}")
        return jsonify({
            'status': 'erro',
            'mensagem': 'Dados recusados pela análise de IA',
            'erros': analise['erros'],
            'alertas': analise.get('alertas', []),
        }), 400
    if analise['alertas']:
        logger.info(f"IA aprovou com alertas | CNPJ: {cnpj} | Alertas: {analise['alertas']}")

    # Enriquece o endereço com a interpretação da IA quando disponível
    if analise.get('endereco_normalizado'):
        dados['_endereco_ia'] = analise['endereco_normalizado']

    # Cadastrando os fornecedores
    resultado = criar_fornecedor_odata(dados)
    if 'erro' in resultado:
        logger.error(f"Erro SAP | CNPJ: {cnpj} | {resultado['erro']}")
        return jsonify({'status': 'erro', 'mensagem': resultado['erro']}), 500

    # Retorno de sucesso ao log
    codigo = resultado['codigo_fornecedor']
    logger.info(f"Fornecedor criado | CNPJ: {cnpj} | Código SAP: {codigo}")
    return jsonify({
        'status': 'sucesso',
        'codigo_fornecedor': codigo,
        'empresa': dados.get('empresa'),
        'cnpj': cnpj,
    }), 201

# Verificação de saude da aplicação Flask
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

# Inicialização do Server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
