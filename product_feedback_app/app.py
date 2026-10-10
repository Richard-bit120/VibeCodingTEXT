import streamlit as st
import pandas as pd
from database import inicializar_base_datos, guardar_comentario, obtener_todos_comentarios, obtener_estadisticas_generales
from sentiment_analyzer import analizar_sentimiento
from text_processor import validar_comentario, es_duplicado_estricto
from importer import procesar_archivo_masivo

# Configuración de página
st.set_page_config(
    page_title="Análisis de Comentarios de Productos",
    page_icon="🛍️",
    layout="wide"
)

# Inicializar base de datos
inicializar_base_datos()

def main():
    st.title("🛍️ Sistema Inteligente de Análisis de Comentarios de Productos")
    st.markdown(
        "Aplicación desarrollada para la materia de **Ingeniería de Software**. "
        "Permite registrar, procesar mediante NLP, auditar y analizar opiniones de clientes."
    )

    menu = st.sidebar.selectbox(
        "Navegación", 
        ["Panel Principal", "Registro Manual", "Procesamiento Masivo (CSV/TXT)", "Historial y Filtros", "Estadísticas Avanzadas"]
    )

    if menu == "Panel Principal":
        st.header("📊 Panel General de Métricas")
        total, positivos, negativos, neutrales, satisfaccion = obtener_estadisticas_generales()

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Comentarios", total)
        col2.metric("Positivos", positivos, delta="😊")
        col3.metric("Negativos", negativos, delta="😞", delta_color="inverse")
        col4.metric("Neutrales", neutrales, delta="😐")
        col5.metric("Satisfacción", f"{satisfaccion:.1f}%")

        st.markdown("---")
        if total > 0:
            st.subheader("Distribución de Sentimientos")
            data_chart = pd.DataFrame({
                'Sentimiento': ['Positivo', 'Negativo', 'Neutral'],
                'Cantidad': [positivos, negativos, neutrales]
            })
            st.bar_chart(data_chart.set_index('Sentimiento'))
        else:
            st.info("Aún no hay datos registrados para mostrar gráficos.")

    elif menu == "Registro Manual":
        st.header("✍️ Registrar Nuevo Comentario")
        
        with st.form("form_comentario"):
            col1, col2 = st.columns(2)
            with col1:
                producto = st.text_input("Nombre o ID del Producto *")
            with col2:
                cliente = st.text_input("Nombre del Cliente *")
            
            comentario = st.text_area("Texto del Comentario *")
            
            col_l, col_d = st.columns(2)
            with col_l:
                likes = st.number_input("Likes iniciales", min_value=0, value=0)
            with col_d:
                dislikes = st.number_input("Dislikes iniciales", min_value=0, value=0)

            submit = st.form_submit_button("🚀 Analizar y Guardar")

            if submit:
                valido, msg_error = validar_comentario(comentario)
                if not producto.strip() or not cliente.strip():
                    st.error("Error: El producto y el cliente son obligatorios.")
                elif not valido:
                    st.error(f"Error: {msg_error}")
                elif es_duplicado_estricto(producto, cliente, comentario):
                    st.warning("Advertencia: Este cliente ya ha registrado exactamente el mismo comentario para este producto.")
                else:
                    # Análisis NLP
                    sentimiento, analisis = analizar_sentimiento(comentario)
                    
                    # Guardar
                    guardar_comentario(
                        producto=producto.strip(),
                        cliente=cliente.strip(),
                        likes=likes,
                        dislikes=dislikes,
                        comentario=comentario.strip(),
                        sentimiento=sentimiento,
                        analisis=analisis,
                        estado="Procesado Correctamente"
                    )
                    st.success(f"✅ Comentario analizado como **{sentimiento}** y guardado exitosamente.")
                    st.info(f"**Análisis:** {analisis}")

    elif menu == "Procesamiento Masivo (CSV/TXT)":
        st.header("📂 Importación Masiva de Comentarios")
        st.markdown("Sube un archivo `.csv` o `.txt` con las columnas: `producto`, `cliente`, `comentario`, `likes`, `dislikes`.")

        archivo = st.file_uploader("Selecciona archivo de datos", type=["csv", "txt"])

        if archivo and st.button("📥 Procesar Archivo"):
            with st.spinner("Procesando lote de comentarios..."):
                exitosos, errores, err_msg = procesar_archivo_masivo(archivo)
                if err_msg:
                    st.error(err_msg)
                else:
                    st.success(f"Proceso completado. Registros exitosos: **{exitosos}** | Errores/Omitidos: **{errores}**")

    elif menu == "Historial y Filtros":
        st.header("📋 Historial de Comentarios y Auditoría")
        
        registros = obtener_todos_comentarios()
        if not registros:
            st.info("No hay registros en la base de datos.")
        else:
            df = pd.DataFrame(registros, columns=["ID", "Producto", "Cliente", "Likes", "Dislikes", "Comentario", "Sentimiento", "Análisis", "Fecha", "Estado"])
            
            # Filtros interactivos
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                filtro_prod = st.selectbox("Filtrar por Producto", ["Todos"] + list(df["Producto"].unique()))
            with col_f2:
                filtro_sent = st.selectbox("Filtrar por Sentimiento", ["Todos"] + list(df["Sentimiento"].unique()))
            with col_f3:
                filtro_cli = st.selectbox("Filtrar por Cliente", ["Todos"] + list(df["Cliente"].unique()))

            df_filtrado = df.copy()
            if filtro_prod != "Todos":
                df_filtrado = df_filtrado[df_filtrado["Producto"] == filtro_prod]
            if filtro_sent != "Todos":
                df_filtrado = df_filtrado[df_filtrado["Sentimiento"] == filtro_sent]
            if filtro_cli != "Todos":
                df_filtrado = df_filtrado[df_filtrado["Cliente"] == filtro_cli]

            st.dataframe(df_filtrado, use_container_width=True)

    elif menu == "Estadísticas Avanzadas":
        st.header("📈 Estadísticas y Tendencias")
        registros = obtener_todos_comentarios()
        if not registros:
            st.info("No hay datos suficientes para generar estadísticas avanzadas.")
        else:
            df = pd.DataFrame(registros, columns=["ID", "Producto", "Cliente", "Likes", "Dislikes", "Comentario", "Sentimiento", "Análisis", "Fecha", "Estado"])
            
            st.subheader("Top Productos con más comentarios")
            top_prod = df["Producto"].value_counts().reset_index()
            top_prod.columns = ["Producto", "Cantidad"]
            st.bar_chart(top_prod.set_index("Producto"))

            st.subheader("Distribución general por Sentimiento")
            st.bar_chart(df["Sentimiento"].value_counts())

if __name__ == "__main__":
    main()