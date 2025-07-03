# app.py

import streamlit as st

st.set_page_config(
    page_title="Last War Dashboard Principal",
    page_icon="📊",
    layout="wide"
)

st.title("¡Bienvenido al Dashboard de Last War!")
st.write("Selecciona una página en la barra lateral izquierda para explorar los datos.")

st.markdown("""
    Este dashboard te permite visualizar diferentes aspectos del juego Last War:
    - **Dashboard de Alianzas:** Visualiza el historial de puntos de las alianzas.
    - **Gestión de Datos:** Herramientas para administrar los datos de la base de datos.
    - **Acerca de:** Información sobre la aplicación.
""")

# Puedes añadir más contenido a tu página principal aquí si lo deseas
# st.image("tu_imagen_de_bienvenida.png")