import sqlite3

def validar_comentario(texto):
    """Valida que el texto no esté vacío y cumpla con la longitud mínima."""
    if not texto or not texto.strip():
        return False, "El campo de comentario no puede estar vacío."
    if len(texto.strip()) < 3:
        return False, "El comentario es demasiado corto."
    return True, ""

def es_duplicado_estricto(producto, cliente, comentario):
    """
    Verifica si existe un registro idéntico con el mismo producto, cliente y texto.
    Nota ingenieril: Dos clientes distintos escribiendo el mismo comentario NO son duplicados.
    """
    conn = sqlite3.connect("feedback_system.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM comentarios_productos 
        WHERE producto = ? AND cliente = ? AND comentario = ?
    """, (producto, cliente, comentario))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0