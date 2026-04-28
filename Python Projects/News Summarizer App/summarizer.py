from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

NOME_MODELO = "phpaiola/ptt5-base-summ-xlsum"

# --- Carrega o modelo e o tokenizador pré-treinado para sumarização de motícias em português ---
# tokenizer transforma o texto em números (tokens) que o modelo entende
tokenizer = AutoTokenizer.from_pretrained(NOME_MODELO)
# modelo é a rede neural pré-treinada que gera os resumos a partir desses tokens
modelo = AutoModelForSeq2SeqLM.from_pretrained(NOME_MODELO)

# --- Função que gera o resumo de um texto usando o modelo pré-treinado ---
def resumir(texto, max_length=150, min_length=30):
    # Limpa espaços
    texto = re.sub(r'\s+', ' ', texto).strip()

    # Tokenização
    inputs = tokenizer(texto, return_tensors="pt", max_length=1000, truncation=True)

    # Geração do resumo
    summary_ids = modelo.generate(
        inputs["input_ids"],
        max_length=800,
        min_length=80,
        length_penalty=4.0,      # Personaliza resumos mais curtos
        num_beams=4,             # Número de sequências a serem considerados
        no_repeat_ngram_size=3,  # Evita repetição de frases
        early_stopping=True      # Para parar quando atingir o comprimento máximo ou mínimo
    )

    # Decodificação do resumo gerado
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
