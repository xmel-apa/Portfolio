import logging
import os
from flask import Flask, request, jsonify
from cnpjVerification import validar_cnpj
from sapConnector import criar_fornecedor_odata

# Configurações de logg
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

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


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
