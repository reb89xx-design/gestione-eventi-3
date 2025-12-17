# db.py
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError

# Assicura che la root del progetto sia nel path (per importare models)
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

try:
    from models import Base
except Exception as e:
    raise ImportError("Impossibile importare models.Base: " + str(e))

# Configurazione DB: per prototipo usiamo SQLite locale
DB_FILE = os.environ.get("AGENCY_DB_FILE", "agency.db")
DATABASE_URL = f"sqlite:///{DB_FILE}"

# Engine e session factory
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    """
    Crea tutte le tabelle definite in models.Base.
    Chiamare all'avvio dell'app (una volta).
    """
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as e:
        raise RuntimeError("Errore durante init_db: " + str(e))

def get_session():
    """
    Restituisce una sessione SQLAlchemy attiva.
    Ricordati di chiuderla con session.close() dopo l'uso.
    Esempio:
        db = get_session()
        try:
            ...
        finally:
            db.close()
    """
    return SessionLocal()

# Utility generator (opzionale) per pattern with-like
def get_db():
    """
    Generator che yield una sessione e la chiude automaticamente.
    Uso tipico in contesti che supportano generator consumption.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
