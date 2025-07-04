import streamlit as st
import streamlit_authenticator as stauth

def authentication():
    try:
        users = []
        for user in st.secrets["auth"]["users"]:
            users.append(user)

        credentials = {"usernames": {}}
        for user in users:
            username = user['username']
            credentials["usernames"][username] = {
                "name": user['name'],
                "password": user['password']
            }

        cookie_name = st.secrets["auth"]["cookie_name"]
        cookie_key = st.secrets["auth"]["cookie_key"]
        cookie_expiry_days = int(st.secrets["auth"]["cookie_expiry_days"])

    except KeyError as e:
        st.error("Falta configurar la sección 'auth' en secrets.toml")
        st.stop()

    # --- Autenticador ---
    authenticator = stauth.Authenticate(
        credentials,
        cookie_name,
        cookie_key,
        cookie_expiry_days
    )

    # ✅ Aquí está bien el uso de "main"
    try:
        authenticator.login(location='sidebar')

    except Exception as e:
        st.error(e)
    return authenticator