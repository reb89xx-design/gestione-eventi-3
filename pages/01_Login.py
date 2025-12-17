# pages/01_Login.py
import os
import sys
import json
from pathlib import Path
import streamlit as st

# Assicura che la root del progetto sia nel path (per importare db, models, utils)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import opzionale di init_db se presente
try:
    from db import init_db
    init_db()
except Exception:
    # Se db.py non è presente o init_db fallisce, non bloccare la login
    pass

st.set_page_config(page_title="Login - Agency Planner", layout="centered")

# Dipendenza per hashing
try:
    import bcrypt
except Exception:
    st.error("Manca la libreria 'bcrypt'. Installa con: pip install bcrypt")
    st.stop()

USERS_FILE = Path(ROOT_DIR) / "users.json"

def load_users():
    """
    Legge users.json o st.secrets["auth"]["users"] se presente.
    Restituisce dict: {username: {name, email, password_hash OR password}}
    """
    # Preferisci st.secrets se su Streamlit Cloud
    if "auth" in st.secrets and "users" in st.secrets["auth"]:
        return st.secrets["auth"]["users"]
    if USERS_FILE.exists():
        try:
            return json.loads(USERS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_users(users: dict):
    """
    Sovrascrive users.json con i dati aggiornati (usato per convertire password in hash).
    """
    try:
        USERS_FILE.write_text(json.dumps(users, indent=2, ensure_ascii=False), encoding="utf-8")
        return True
    except Exception:
        return False

def is_hashed(pw_value: str) -> bool:
    """
    Semplice controllo: gli hash bcrypt iniziano con $2b$ o $2a$ o $2y$
    """
    return isinstance(pw_value, str) and pw_value.startswith("$2")

def hash_password(plain_pw: str) -> str:
    return bcrypt.hashpw(plain_pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_pw: str, hashed_pw: str) -> bool:
    try:
        return bcrypt.checkpw(plain_pw.encode("utf-8"), hashed_pw.encode("utf-8"))
    except Exception:
        return False

# Carica utenti
users = load_users()

st.title("Login")
st.write("Accedi con le tue credenziali di test (username: **test**, password: **test**)")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Accedi")

    if submitted:
        if not username or not password:
            st.error("Inserisci username e password")
        elif username not in users:
            st.error("Utente non trovato")
        else:
            user_record = users[username]

            # Se il record contiene 'password' in chiaro, convertilo in hash e salva
            if "password" in user_record and not is_hashed(user_record["password"]):
                try:
                    new_hash = hash_password(user_record["password"])
                    user_record["password_hash"] = new_hash
                    # rimuovi la password in chiaro
                    user_record.pop("password", None)
                    users[username] = user_record
                    saved = save_users(users)
                    if not saved:
                        st.warning("Impossibile salvare users.json: la conversione a hash è stata fatta in memoria ma non è stata salvata su file (ambiente di sola lettura?).")
                except Exception as e:
                    st.error("Errore durante la generazione dell'hash: " + str(e))
                    st.stop()

            # Verifica password usando password_hash
            hashed = user_record.get("password_hash")
            if not hashed:
                st.error("Nessuna password valida trovata per l'utente. Contatta l'amministratore.")
            else:
                if verify_password(password, hashed):
                    st.success(f"Benvenuto {user_record.get('name', username)}")
                    # salva stato di autenticazione in session_state
                    st.session_state["user"] = {
                        "username": username,
                        "name": user_record.get("name", username),
                        "email": user_record.get("email", "")
                    }
                    # Ricarica la pagina per riflettere stato loggato
                    st.experimental_rerun()
                else:
                    st.error("Password errata")

# Se già loggato mostra info e link rapidi
if st.session_state.get("user"):
    u = st.session_state["user"]
    st.info(f"Sei loggato come **{u['name']}** ({u['username']}) — {u.get('email','')}")
    st.write("Vai al menu a sinistra per navigare nell'app.")
