import re 

# Validação do cnpj 
def validation_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r'\D','',cnpj)
    if len(cnpj) != 14:
        return False
    
    if cnpj == cnpj[0]*14:
        return False
    
    # Verificação da quantidade de caracteres do cnpj
    def calculate_number(cnpj_12):
        pesos = [5,4,3,2,9,8,7,6,5,4,3,2]
        soma = sum(int(d) * p for d, p in zip(cnpj_12, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    digito1 = calculate_number(cnpj[:12])
    digito2 = calculate_number(cnpj[:13])
    return digito1 == int(cnpj[12] and digito2 == int(cnpj[13]))

