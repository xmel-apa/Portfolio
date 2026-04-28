from LeIA import SentimentIntensityAnalyzer

analizador = SentimentIntensityAnalyzer()

def analisar_sentimento(texto: str) -> dict:
    """
    Analisa o sentimento de um texto e retorna um dicionário com classificação,
    score compound e emoji.
    """
    texto_para_analise = texto[:1000]
    scores = analizador.polarity_scores(texto_para_analise)
    compound_score = scores['compound']

    if compound_score >= 0.05:
        classificacao = "Positivo"
        emoji = "🟢"
    elif compound_score <= -0.05:
        classificacao = "Negativo"
        emoji = "🔴"
    else:
        classificacao = "Neutro"
        emoji = "⚪"

    return {
        "classificacao": classificacao,
        "emoji": emoji,
        "score_compound": compound_score,
        "scores": scores
    }

if __name__ == "__main__":
    texto_teste = "Este é um exemplo de texto para análise de sentimento. Estou muito feliz com os resultados!"
    resultado = analisar_sentimento(texto_teste)
    print(f"Classificação: {resultado['classificacao']} {resultado['emoji']}")