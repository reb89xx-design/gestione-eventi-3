import streamlit as st
import streamlit_authenticator as stauth
from db import init_db

st.set_page_config(page_title="Login")
init_db()

# --- CONFIGURAZIONE PROTOTIPO ---
# Per prototipo locale: definisci le password qui (meglio usare st.secrets in produzione)
plain_passwords = ["changeme"]  # sostituisci con password sicura o usa st.secrets

# Genera gli hash una sola volta
try:
    hashed_passwords = stauth.Hasher(plain_passwords).generate()
except Exception as e:
    st.error("Errore nella generazione degli hash delle password. Controlla la versione di streamlit-authenticator.")
    st.stop()

# Costruisci le credenziali usando gli hash
credentials = {
    "usernames": {
        "ale": {
            "name": "Ale",
            "password": hashed_passwords[0]
        }
    }
}

# Inizializza l'autenticatore
auth = stauth.Authenticate(
    credentials,
    cookie_name="agency_cookie",
    key="some_random_key",            # in produzione usa un valore sicuro da secrets
    cookie_expiry_days=30
)

name, auth_status, username = auth.login("Login", "main")

if auth_status:
    st.success(f"Benvenuto {name}")
    st.write("Vai al menu a sinistra per navigare.")
elif auth_status is False:
    st.error("Username o password errati")
else:
    st.info("Inserisci le credenziali")

