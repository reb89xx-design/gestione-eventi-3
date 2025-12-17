# scripts/seed_demo.py
from db import get_session
from utils import add_artist, add_format, add_service

# usa funzioni utils per avere audit automatico
add_artist("Demo Artist", role="artist", phone="", email="", notes="seed")
add_format("Demo Format", description="seed")
add_service("Demo Service", contact="info", phone="123")
print("Seed completato")
