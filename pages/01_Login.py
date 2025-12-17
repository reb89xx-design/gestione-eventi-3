import os
import sys
import streamlit as st

# Assicura che la root del progetto sia nel path (per importare db, models, utils)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Ora possiamo importare init_db da db.py
try:
    from db import init_db
except Exception as e:
    st.error("Errore import db: " + str(e))
    st.stop()

# Inizializza DB (crea tabelle se non esistono)
init_db()

# --- Autenticazione ---
# Preferibile usare st.secrets per password/chiavi in produzione:
# es. st.secrets["auth"]["users"] = {"ale": {"name":"Ale","password":"<hash>"}}
try:
    import streamlit_authenticator as stauth
except Exception as e:
    st.error("streamlit-authenticator non trovato. Installa la dipendenza: pip install streamlit-authenticator")
    st.stop()

st.set_page_config(page_title="Login - Agency Planner", layout="centered")

# Configurazione prototipo: usa st.secrets se disponibile, altrimenti fallback
# In produzione NON lasciare password in chiaro nel codice
plain_passwords = []
credentials = {}

if "auth" in st.secrets and "users" in st.secrets["auth"]:
    # struttura attesa in secrets.toml:
    # [auth.users.ale]
    # name = "Ale"
    # password = "<plain_or_hash>"
    users = st.secrets["auth"]["users"]
    # Se gli hash sono già forniti, puoi usarli direttamente; qui assumiamo plain per prototipo
    usernames = list(users.keys())
    names = [users[u].get("name", u) for u in usernames]
    plain_passwords = [users[u].get("password", "") for u in usernames]
else:
    # Fallback per sviluppo: un utente demo
    usernames = ["ale"]
    names = ["Ale"]
    plain_passwords = ["changeme"]

# Genera hash delle password (eseguito una volta ad ogni run; in produzione salva gli hash)
try:
    hashed_passwords = stauth.Hasher(plain_passwords).generate()
except Exception as e:
    st.error("Errore nella generazione degli hash delle password: " + str(e))
    st.stop()

# Costruisci il dict credentials richiesto da streamlit-authenticator
credentials = {"usernames": {}}
for u, n, h in zip(usernames, names, hashed_passwords):
    credentials["usernames"][u] = {"name": n, "password": h}

# Cookie config (per prototipo usa valori semplici; in produzione prendi key da secrets)
cookie_name = "agency_cookie"
cookie_key = st.secrets.get("cookie_key", "replace_with_secure_key")
cookie_expiry_days = 30

auth = stauth.Authenticate(
    credentials,
    cookie_name,
    cookie_key,
    cookie_expiry_days
)

name, auth_status, username = auth.login("Login", "main")

if auth_status:
    st.success(f"Benvenuto {name}")
    st.write("Usa il menu a sinistra per navigare nell'app.")
elif auth_status is False:
    st.error("Username o password errati")
else:
    st.info("Inserisci le credenziali per accedere")
