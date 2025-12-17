import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError

# Assicura che models sia importabile (se models.py è nella root)
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in os.sys.path:
    os.sys.path.insert(0, ROOT_DIR)

try:
    from models import Base
except Exception as e:
    raise ImportError("Impossibile importare models.Base: " + str(e))

# Configurazione DB: per prototipo usiamo SQLite locale
DB_FILE = os.environ.get("AGENCY_DB_FILE", "agency.db")
DATABASE_URL = f"sqlite:///{DB_FILE}"

# Engine e session factory
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
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

def get_db():
    """
    Restituisce una sessione DB. Usare in try/finally o con context manager.
    Esempio:
        db = get_db()
        try:
            ...
        finally:
            db.close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility semplice per ottenere una sessione (non generator) quando serve
def get_session():
    """
    Restituisce una sessione SQLAlchemy attiva. Ricordati di chiuderla con session.close().
    """
    return SessionLocal()
