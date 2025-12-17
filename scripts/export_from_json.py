# scripts/export_to_json.py
import json, os
from db import get_session
from models import Artist, Format, TourManager

OUT = os.environ.get("DATA_JSON_OUT", "data/people_export.json")

def export_all():
    db = get_session()
    try:
        data = {
            "artists": [{"id": a.id, "name": a.name, "role": a.role, "phone": a.phone, "email": a.email, "notes": a.notes} for a in db.query(Artist).all()],
            "formats": [{"id": f.id, "name": f.name, "description": f.description, "notes": f.notes} for f in db.query(Format).all()],
            "tour_managers": [{"id": t.id, "name": t.name, "contact": t.contact, "phone": t.phone, "email": t.email, "notes": t.notes} for t in db.query(TourManager).all()]
        }
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
    finally:
        db.close()

if __name__ == "__main__":
    export_all()
