from db import SessionLocal
from models import Event, Artist, Service, Format, Promoter, TourManager
from datetime import date
from sqlalchemy.orm import joinedload

def get_session():
    return SessionLocal()

def list_events_by_date(target_date):
    db = get_session()
    events = db.query(Event).filter(Event.date == target_date).options(joinedload(Event.artists)).all()
    db.close()
    return events

def get_event(event_id):
    db = get_session()
    ev = db.query(Event).filter(Event.id == event_id).options(joinedload(Event.artists), joinedload(Event.services)).first()
    db.close()
    return ev

def save_event(data):
    db = get_session()
    if data.get("id"):
        ev = db.query(Event).get(data["id"])
        ev.title = data["title"]
        ev.date = data["date"]
        ev.location = data["location"]
        ev.status = data["status"]
        ev.notes = data["notes"]
    else:
        ev = Event(title=data["title"], date=data["date"], location=data["location"], status=data["status"], notes=data["notes"])
        db.add(ev)
    db.commit()
    db.refresh(ev)
    db.close()
    return ev

# Funzioni CRUD semplificate per entità
def list_artists():
    db = get_session()
    items = db.query(Artist).all()
    db.close()
    return items

def add_artist(name, contact=""):
    db = get_session()
    a = Artist(name=name, contact=contact)
    db.add(a)
    db.commit()
    db.refresh(a)
    db.close()
    return a
