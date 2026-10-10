import sqlite3
from datetime import datetime

DB_NAME = "feedback_system.db"

def inicializar_base_datos():
    """Ejecuta el esquema SQL para inicializar la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios_productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            cliente TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            dislikes INTEGER DEFAULT 0,
            comentario TEXT NOT NULL,
            sentimiento TEXT NOT NULL,
            analisis TEXT NOT NULL,
            fecha_creacion TEXT NOT NULL,
            estado_procesamiento TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def guardar_comentario(producto, cliente, likes, dislikes, comentario, sentimiento, analisis, estado):
    """Guarda un registro utilizando consultas parametrizadas para evitar inyección SQL."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO comentarios_productos 
        (producto, cliente, likes, dislikes, comentario, sentimiento, analisis, fecha_creacion, estado_procesamiento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (producto, cliente, likes, dislikes, comentario, sentimiento, analisis, fecha_actual, estado))
    
    conn.commit()
    conn.close()

def obtener_todos_comentarios():
    """Recupera todos los comentarios registrados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comentarios_productos ORDER BY id DESC")
    registros = cursor.fetchall()
    conn.close()
    return registros

def obtener_estadisticas_generales():
    """Retorna métricas clave para el panel principal."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM comentarios_productos")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM comentarios_productos WHERE sentimiento = 'Positivo'")
    positivos = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM comentarios_productos WHERE sentimiento = 'Negativo'")
    negativos = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM comentarios_productos WHERE sentimiento = 'Neutral'")
    neutrales = cursor.fetchone()[0]
    
    conn.close()
    
    satisfaccion = (positivos / total * 100) if total > 0 else 0.0
    return total, positivos, negativos, neutrales, satisfaccion