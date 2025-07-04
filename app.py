import streamlit as st
from auth_utils import authentication

authenticator = authentication()

if st.session_state.get('authentication_status'):
    authenticator.logout(location='sidebar')
    
    st.title("¡Welcome to Last War Dashboard!")
    st.write("Select a page at the sidebar to navigate")

    st.markdown("""
        This dashboard allows you to visualize different aspects of the game Last War:

                - Alliance Dashboard: Visualize the alliance points history.

                - Data Management: Tools for managing database data.

                - About: Information about the application.
    """)
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')