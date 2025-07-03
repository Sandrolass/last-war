# app.py

import streamlit as st

st.set_page_config(
    page_title="Last War Dashboard Principal",
    page_icon="📊",
    layout="wide"
)

st.title("¡Welcome to Last War Dashboard!")
st.write("Select a page at the sidebar to navigate")

st.markdown("""
    This dashboard allows you to visualize different aspects of the game Last War:

            - Alliance Dashboard: Visualize the alliance points history.

            - Data Management: Tools for managing database data.

            - About: Information about the application.
""")

# Puedes añadir más contenido a tu página principal aquí si lo deseas
# st.image("tu_imagen_de_bienvenida.png")