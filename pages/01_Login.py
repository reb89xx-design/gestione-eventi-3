import streamlit as st
import streamlit_authenticator as stauth
import yaml

st.set_page_config(page_title="Login")

config = {
    "credentials": {
        "usernames": {
            "ale": {"name":"Ale", "password": stauth.Hasher(['password']).generate()[0]}
        }
    },
    "cookie": {"name":"agency_cookie","key":"some_random_key","expiry_days":30},
    "preauthorized": {"emails": []}
}

auth = stauth.Authenticate(config['credentials'], config['cookie']['name'], config['cookie']['key'], config['cookie']['expiry_days'])
name, authentication_status, username = auth.login("Login", "main")

if authentication_status:
    st.success(f"Benvenuto {name}")
elif authentication_status is False:
    st.error("Username/password errati")
else:
    st.info("Inserisci le credenziali")
