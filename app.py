import streamlit as st
import mysql.connector
import pandas as pd

# --- Configuración de la Conexión a la Base de Datos ---
# ADVERTENCIA: No pongas credenciales directamente en el código para producción.
# Usa variables de entorno o st.secrets para mayor seguridad.
DB_CONFIG = {
    "host": st.secrets.connections.mysql.host,
    "user": st.secrets.connections.mysql.user,
    "port": st.secrets.connections.mysql.port,
    "password": st.secrets.connections.mysql.password,
    "database": st.secrets.connections.mysql.database
}

@st.cache_data # Cachea los datos para no hacer la consulta cada vez que Streamlit redibuja
def get_data_from_db():
    """Conecta a MySQL, obtiene los datos y retorna un DataFrame."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True) # dictionary=True para obtener resultados como diccionarios

        # Consulta para alliance_points_history y join con Alianzas para el nombre
        query = """
        SELECT
            aph.register_id,
            a.alliance_name,
            aph.season_id,
            aph.points,
            aph.register_date
        FROM
            alliance_points_history aph
        JOIN
            alliance a ON aph.alliance_id = a.alliance_id
        ORDER BY
            aph.register_date DESC, a.alliance_name;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        
        df = pd.DataFrame(data)
        return df

    except mysql.connector.Error as err:
        st.error(f"Error al conectar o consultar la base de datos: {err}")
        return pd.DataFrame() # Retorna un DataFrame vacío en caso de error
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# --- Interfaz de Streamlit ---

st.set_page_config(layout="wide") # Configura el diseño de la página
st.title("Historial de Puntos de Alianzas")
st.markdown("---")

# Obtener los datos
df_points = get_data_from_db()

if not df_points.empty:
    st.subheader("Datos Recientes:")
    st.dataframe(df_points) # Muestra el DataFrame en una tabla interactiva

    st.subheader("Estadísticas Básicas:")
    st.write(df_points.describe())

    # Puedes añadir gráficos aquí si lo deseas
    st.subheader("Puntos por Servidor (Último Registro por Alianza):")
    # Para obtener el último registro de cada alianza, podemos agrupar por alianza y tomar el max fecha
    # Esto es una simplificación; un enfoque más robusto usaría ROW_NUMBER() en SQL si tienes SQL 8.0+
    latest_points = df_points.sort_values('register_date', ascending=False).drop_duplicates('alliance_name')
    st.bar_chart(latest_points.set_index('alliance_name')['points'])

else:
    st.warning("No se pudieron cargar los datos o no hay datos disponibles en la tabla 'alliance_points_history'.")

st.markdown("---")
st.write("Aplicación Streamlit para visualizar datos de MySQL.")

# Botón para recargar los datos
if st.button("Recargar Datos"):
    st.cache_data.clear() # Limpia la caché para forzar una nueva consulta
    st.rerun() # Vuelve a ejecutar la aplicación