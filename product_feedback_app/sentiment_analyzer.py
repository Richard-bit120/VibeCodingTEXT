def analizar_sentimiento(texto):
    """
    Analiza el texto mediante reglas léxicas en español.
    Identifica sentimiento: Positivo, Negativo o Neutral y genera un análisis explicativo.
    """
    if not texto or not isinstance(texto, str):
        return "Neutral", "Comentario vacío o inválido para análisis."

    texto_lower = texto.lower()

    # Listas de términos clave ponderados
    palabras_positivas = [
        "excelente", "perfecto", "rápido", "bueno", "encantó", "maravilloso", 
        "feliz", "recomiendo", "calidad", "agradable", "eficiente", "excele", "satisfecho"
    ]
    palabras_negativas = [
        "mala", "malo", "pésimo", "horrible", "falló", "roto", "decepcionó", 
        "tardó", "problema", "defecto", "inútil", "queja", "esperaba algo mejor", "no funciona"
    ]

    score_positivo = sum(1 for palabra in palabras_positivas if palabra in texto_lower)
    score_negativo = sum(1 for palabra in palabras_negativas if palabra in texto_lower)

    # Heurística para matices (ej: "no funciona... excelente atención")
    if score_positivo > score_negativo:
        sentimiento = "Positivo"
        analisis = f"Se detectaron términos de satisfacción ({score_positivo} positivos vs {score_negativo} negativos). Tono general favorable."
    elif score_negativo > score_positivo:
        sentimiento = "Negativo"
        analisis = f"Se identificaron expresiones de insatisfacción o problemas ({score_negativo} negativos vs {score_positivo} positivos)."
    else:
        # Analizamos si hay contenido neutral o balanceado
        if score_positivo == 0 and score_negativo == 0:
            sentimiento = "Neutral"
            analisis = "El texto es descriptivo o neutral, sin carga evaluativa fuerte evidente."
        else:
            sentimiento = "Neutral"
            analisis = "El texto presenta opiniones mixtas o equilibradas entre aspectos positivos y negativos."

    return sentimiento, analisis