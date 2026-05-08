from flask import Flask, request, jsonify
from validar_cnpj import validar_cnpj
from sap_connector import criar_fornecedor_sap

app = Flask(__name__)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.json
    cnpj = dados.get('cnpj', '')
    if not validar_cnpj(cnpj):
        return jsonify({'erro': 'CNPJ inválido'}), 400

    resultado = criar_fornecedor_sap(dados)
    if 'erro' in resultado:
        return jsonify(resultado), 500
    return jsonify(resultado), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)