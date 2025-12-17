# scripts/create_tables.py
from sqlalchemy import create_engine
from models import Base
import os

# Leggi la stringa di connessione dal tuo env o usa sqlite locale
DB_URL = os.environ.get("AGENCY_DB_URL") or os.environ.get("AGENCY_DB_FILE") or "sqlite:///data/agency.db"

# Se DB_URL è un path file come "data/agency.db" converti in sqlite URL
if DB_URL.endswith(".db") and not DB_URL.startswith("sqlite://"):
    DB_URL = f"sqlite:///{DB_URL}"

engine = create_engine(DB_URL, echo=True)
Base.metadata.create_all(bind=engine)
print("Tabelle create (se non esistevano). DB:", DB_URL)
