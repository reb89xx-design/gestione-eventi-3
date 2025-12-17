# scripts/seed_from_json.py
import json, os
from db import get_session
from models import Artist, Format, TourManager

DATA_FILE = os.environ.get("DATA_JSON", "data/people.json")

def seed():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    db = get_session()
    try:
        # solo se tabella vuota (evita duplicati)
        if db.query(Artist).count() == 0:
            for a in data.get("artists", []):
                db.add(Artist(name=a["name"], role=a.get("role","artist"), phone=a.get("phone",""), email=a.get("email",""), notes=a.get("notes","")))
        if db.query(Format).count() == 0:
            for fm in data.get("formats", []):
                db.add(Format(name=fm["name"], description=fm.get("description",""), notes=fm.get("notes","")))
        if db.query(TourManager).count() == 0:
            for tm in data.get("tour_managers", []):
                db.add(TourManager(name=tm["name"], contact=tm.get("contact",""), phone=tm.get("phone",""), email=tm.get("email",""), notes=tm.get("notes","")))
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
