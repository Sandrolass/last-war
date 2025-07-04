# pages/4_Visualizacion_Batallas.py

import streamlit as st
import mysql.connector
import pandas as pd

from auth_utils import authentication

authenticator = authentication()

# --- Configuración de la Conexión a la Base de Datos ---
if st.session_state.get('authentication_status'):
    authenticator.logout(location='sidebar')
    DB_CONFIG = {
        "host": st.secrets.connections.mysql.host,
        "user": st.secrets.connections.mysql.user,
        "port": st.secrets.connections.mysql.port,
        "password": st.secrets.connections.mysql.password,
        "database": st.secrets.connections.mysql.database
    }

    icon_const = {
        'A':{
            'prefix_1':'ATTACKER_',
            'prefix_2':'OBTAINED_'
        },
        'D':{
            'prefix_1':'DEFENDER_',
            'prefix_2':'LOST_'
        }
    } 

    @st.cache_data
    def get_battle_data_from_db():
        """
        Conecta a MySQL y obtiene los datos de batallas.
        Los campos ATTACKER_X y DEFENDER_X ahora son VARCHAR (códigos de alianza).
        """
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            query = """
            SELECT
                BATTLE_ID,
                ATTACKER_1, OBTAINED_1,
                ATTACKER_2, OBTAINED_2,
                ATTACKER_3, OBTAINED_3,
                DEFENDER_1, LOST_1,
                DEFENDER_2, LOST_2,
                DEFENDER_3, LOST_3,
                SEASON_ID,
                ROUND
            FROM
                BATTLE
            ORDER BY
                SEASON_ID DESC, ROUND DESC, BATTLE_ID DESC;
            """
            cursor.execute(query)
            data = cursor.fetchall()

            df = pd.DataFrame(data)

            # Rellenar valores NULL en los nombres de atacantes/defensores con una cadena vacía
            # para facilitar el conteo de participantes
            for col in ['ATTACKER_1', 'ATTACKER_2', 'ATTACKER_3', 'DEFENDER_1', 'DEFENDER_2', 'DEFENDER_3']:
                df[col] = df[col].fillna('')

            return df

        except mysql.connector.Error as err:
            st.error(f"Error al conectar o consultar la base de datos de batallas: {err}")
            st.warning("Verifica la tabla 'BATTLE' y las credenciales.")
            return pd.DataFrame()
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None and conn.is_connected():
                conn.close()

    # --- Función para generar los iconos ---
    def get_icons(count, icon_emoji, color,row,type):
        """Genera una cadena de iconos HTML para Streamlit."""
        icons_html = ""
        for t in range(count):
            colName = icon_const[type]['prefix_1']+str(t+1)
            colVal = icon_const[type]['prefix_2']+str(t+1)
            nm = row[colName]

            nm2 = 1 * row[colVal] if type == 'A' else -1 * row[colVal]

            icons_html += f"<span style='text-align: center;font-size: 2em; color: {color}; display: block; margin: 0 auto;'>{icon_emoji} <span>{nm} : {nm2}</span></span>"
        return icons_html

    # --- Interfaz de Streamlit para esta página ---

    st.title("⚔️ Visualización de Batallas")
    st.markdown("Observa el despliegue de atacantes y defensores en cada batalla.")
    st.markdown("---")

    df_battles = get_battle_data_from_db()

    if not df_battles.empty:
        st.subheader("Filtros de Batallas:")

        # FILTROS
        all_seasons = ['Todas'] + sorted(df_battles['SEASON_ID'].unique().tolist())
        all_rounds = ['Todas'] + sorted(df_battles['ROUND'].unique().tolist())
        all_attackers = ['Todos'] + sorted(df_battles['ATTACKER_1'].unique().tolist())
        all_defenders = ['Todos'] + sorted(df_battles['DEFENDER_1'].unique().tolist())

        col_filters = st.columns(2)
        with col_filters[0]:
            selected_season = st.selectbox("Selecciona Temporada:", all_seasons)
        with col_filters[1]:
            selected_round = st.selectbox("Selecciona Ronda:", all_rounds)
        col_filters_2 = st.columns(2)
        with col_filters_2[0]:
            selected_attacker = st.selectbox("Select Attacker:", all_attackers)
        with col_filters_2[1]:
            selected_defender = st.selectbox("Select Defender:", all_defenders)    

        filtered_df_battles = df_battles.copy()

        if selected_season != 'Todas':
            filtered_df_battles = filtered_df_battles[filtered_df_battles['SEASON_ID'] == selected_season]
        if selected_round != 'Todas':
            filtered_df_battles = filtered_df_battles[filtered_df_battles['ROUND'] == selected_round]
        if selected_attacker != 'Todos':
            filtered_df_battles = filtered_df_battles[filtered_df_battles['ATTACKER_1'] == selected_attacker]
        if selected_defender != 'Todos':
            filtered_df_battles = filtered_df_battles[filtered_df_battles['DEFENDER_1'] == selected_defender]
        st.subheader("Representación Visual de Batallas:")

        if not filtered_df_battles.empty:
            for idx, row in filtered_df_battles.iterrows():
                # Contar atacantes y defensores
                num_attackers = sum(1 for col in ['ATTACKER_1', 'ATTACKER_2', 'ATTACKER_3'] if row[col])
                num_defenders = sum(1 for col in ['DEFENDER_1', 'DEFENDER_2', 'DEFENDER_3'] if row[col])

                # Generar iconos
                attacker_icons_html = get_icons(num_attackers, "⚔️", "red",row,'A')
                defender_icons_html = get_icons(num_defenders, "🛡️", "blue",row,'D')

                # Mostrar información de la batalla
                st.markdown(f"### Batalla ID: {row['BATTLE_ID']} (Temporada: {row['SEASON_ID']}, Ronda: {row['ROUND']})")

                # Usar columnas para el diseño "Espadas vs VS vs Escudos"
                col_left, col_center, col_right = st.columns([1, 0.5, 1]) # Proporciones de las columnas

                with col_left:
                    st.markdown("<div style='text-align: center;'>**Atacantes:**</div>", unsafe_allow_html=True)
                    st.markdown(attacker_icons_html, unsafe_allow_html=True)
                    # Opcional: Mostrar nombres de atacantes
                    attacker_names = [row[f'ATTACKER_{i}'] for i in range(1, 4) if row[f'ATTACKER_{i}']]
                    if attacker_names:
                        st.markdown(f"<div style='text-align: center; font-size: 0.9em;'>({', '.join(attacker_names)})</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: center; font-weight: bold; color: darkgreen;'>Obtenido: {row['OBTAINED_1'] + row['OBTAINED_2'] + row['OBTAINED_3']}</div>", unsafe_allow_html=True)


                with col_center:
                    st.markdown("<div style='text-align: center;margin-top:30px; font-size: 3em; font-weight: bold; color: gray; line-height: 1;'>VS</div>", unsafe_allow_html=True)

                with col_right:
                    st.markdown("<div style='text-align: center;'>**Defensores:**</div>", unsafe_allow_html=True)
                    st.markdown(defender_icons_html, unsafe_allow_html=True)
                    # Opcional: Mostrar nombres de defensores
                    defender_names = [row[f'DEFENDER_{i}'] for i in range(1, 4) if row[f'DEFENDER_{i}']]
                    if defender_names:
                        st.markdown(f"<div style='text-align: center; font-size: 0.9em;'>({', '.join(defender_names)})</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: center; font-weight: bold; color: darkred;'>Perdido: {row['LOST_1'] + row['LOST_2'] + row['LOST_3']}</div>", unsafe_allow_html=True)


                st.markdown("---") # Separador visual entre batallas
        else:
            st.info("No hay batallas que coincidan con los filtros aplicados.")

    else:
        st.warning("No se pudieron cargar los datos de batallas o la tabla 'BATTLE' está vacía.")

    st.markdown("---")
    st.write("Visualización de batallas para un análisis rápido.")

    if st.button("Recargar Datos de Batallas"):
        st.cache_data.clear()
        st.rerun()
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')