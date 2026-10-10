import pandas as pd
from text_processor import validar_comentario, es_duplicado_estricto
from sentiment_analyzer import analizar_sentimiento
from database import guardar_comentario

def procesar_archivo_masivo(archivo):
    """
    Procesa archivos CSV o TXT delimitados por comas o tabulaciones.
    Columnas esperadas: producto, cliente, comentario, likes (opcional), dislikes (opcional).
    """
    try:
        if archivo.name.endswith('.csv'):
            df = pd.read_csv(archivo)
        elif archivo.name.endswith('.txt'):
            df = pd.read_csv(archivo, sep=None, engine='python')
        else:
            return 0, 0, "Formato de archivo no soportado. Use CSV o TXT."

        # Validar columnas mínimas
        columnas_requeridas = {'producto', 'cliente', 'comentario'}
        if not columnas_requeridas.issubset(df.columns):
            return 0, 0, f"Error: El archivo debe contener las columnas: {list(columnas_requeridas)}"

        exitosos = 0
        errores = 0

        for _, row in df.iterrows():
            producto = str(row['producto']).strip()
            cliente = str(row['cliente']).strip()
            comentario = str(row['comentario']).strip()
            likes = int(row['likes']) if 'likes' in df.columns and pd.notna(row['likes']) else 0
            dislikes = int(row['dislikes']) if 'dislikes' in df.columns and pd.notna(row['dislikes']) else 0

            # Validaciones
            valido, msg = validar_comentario(comentario)
            if not valido or not producto or not cliente:
                errores += 1
                continue

            if es_duplicado_estricto(producto, cliente, comentario):
                errores += 1
                continue

            # Análisis
            sentimiento, analisis = analizar_sentimiento(comentario)
            
            # Guardado
            guardar_comentario(
                producto=producto,
                cliente=cliente,
                likes=likes,
                dislikes=dislikes,
                comentario=comentario,
                sentimiento=sentimiento,
                analisis=analisis,
                estado="Procesado Correctamente"
            )
            exitosos += 1

        return exitosos, errores, None

    except Exception as e:
        return 0, 0, f"Error al procesar el archivo: {str(e)}"