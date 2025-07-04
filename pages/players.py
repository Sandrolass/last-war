# pages/X_Lista_Usuarios.py

import streamlit as st
import mysql.connector
import pandas as pd

from auth_utils import authentication

authenticator = authentication()

if st.session_state.get('authentication_status'):
    authenticator.logout(location='sidebar')  # Permite al usuario cerrar sesión desde la barra lateral
# --- Configuración de la Conexión a la Base de Datos ---
# Asegúrate de que estas credenciales estén en tu .streamlit/secrets.toml
    DB_CONFIG = {
        "host": st.secrets.connections.mysql.host,
        "user": st.secrets.connections.mysql.user,
        "port": st.secrets.connections.mysql.port,
        "password": st.secrets.connections.mysql.password,
        "database": st.secrets.connections.mysql.database
    }

    @st.cache_data # Cachea los datos para no hacer la consulta cada vez que Streamlit redibuja
    def get_users_data_from_db():
        """Conecta a MySQL, obtiene los datos de usuarios y retorna un DataFrame."""
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True) # Para obtener resultados como diccionarios

            # Consulta para obtener los datos de la tabla de usuarios
            # (Ajusta el nombre de la tabla si no es 'User' o 'users')
            query = """
            SELECT
                user_id,
                user_name,
                alliance_name,
                server_id,
                hero_power
            FROM
                user; -- Asumiendo que tu tabla de usuarios se llama 'User'. Si es 'users', cámbialo.
            """
            cursor.execute(query)
            data = cursor.fetchall()

            df = pd.DataFrame(data)
            return df

        except mysql.connector.Error as err:
            st.error(f"Error al conectar o consultar la base de datos de usuarios: {err}")
            st.warning("Verifica la tabla 'User' y las credenciales en .streamlit/secrets.toml.")
            return pd.DataFrame() # Retorna un DataFrame vacío en caso de error
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None and conn.is_connected():
                conn.close()

    # --- Interfaz de Streamlit para esta página ---

    st.set_page_config(layout="wide") # Ajusta el diseño si aún no está hecho en app.py
    st.title("👥 Players list")
    st.markdown("Filter and Expore for Players data")
    st.markdown("---")

    # Obtener los datos de los usuarios
    df_users = get_users_data_from_db()

    if not df_users.empty:
        st.subheader("Filters:")

        # FILTRO POR SERVER_ID (DESPLEGABLE)
        # Obtener valores únicos de server_id para el desplegable
        all_servers = ['Todos'] + sorted(df_users['server_id'].unique().tolist())
        selected_server = st.selectbox("Select server:", all_servers)

        # FILTRO POR USER_NAME (TEXTO LIBRE)
        search_user_name = st.text_input("Search by Username:", "").strip() # .strip() para eliminar espacios extra

        # Aplicar filtros
        filtered_df = df_users.copy() # Trabajar en una copia para no modificar el original

        if selected_server != 'Todos':
            filtered_df = filtered_df[filtered_df['server_id'] == selected_server]

        if search_user_name: # Si el campo de búsqueda no está vacío
            # Usamos .str.contains() para una búsqueda parcial insensible a mayúsculas/minúsculas
            filtered_df = filtered_df[
                filtered_df['user_name'].astype(str).str.contains(search_user_name, case=False, na=False)
            ]

        st.subheader("Player Results:")
        if not filtered_df.empty:
            st.dataframe(filtered_df)
        else:
            st.info("No players were found with this filters.")

        st.markdown("---")
        st.write("Datos obtenidos de tu base de datos MySQL.")

        # Botón para recargar los datos
        if st.button("Recharger Players Data"):
            st.cache_data.clear() # Limpia la caché para forzar una nueva consulta
            st.rerun() # Vuelve a ejecutar la aplicación

    else:
        st.warning("No se pudieron cargar los datos de usuarios o no hay datos disponibles en la tabla 'User'.")
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')