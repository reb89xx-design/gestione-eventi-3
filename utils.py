# utils.py
from db import get_session
from models import Event, Artist, Service, Format, Promoter, TourManager
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

def list_artists():
    db = get_session()
    try:
        return db.query(Artist).order_by(Artist.name).all()
    finally:
        db.close()

def list_artists_by_role(role):
    db = get_session()
    try:
        return db.query(Artist).filter(Artist.role == role).order_by(Artist.name).all()
    finally:
        db.close()

def get_event(event_id):
    db = get_session()
    try:
        return db.query(Event).options(joinedload(Event.artists), joinedload(Event.services)).filter(Event.id == event_id).first()
    finally:
        db.close()

def list_events_by_date(target_date):
    db = get_session()
    try:
        return db.query(Event).filter(Event.date == target_date).order_by(Event.id).all()
    finally:
        db.close()

def save_event(data):
    """
    data: dict con campi:
      id (opz), date (datetime.date), title, location, type,
      format_id, promoter_id, tour_manager_id, status, notes,
      van, travel, hotel, allestimenti, facchini,
      payments_acconto (float), payments_saldo (float),
      dj_id, vocalist_id, ballerine_ids (list), mascotte_ids (list),
      artist_ids (list), service_ids (list)
    """
    db = get_session()
    try:
        if data.get("id"):
            ev = db.query(Event).get(data["id"])
            if not ev:
                return None
        else:
            ev = Event()
            db.add(ev)

        # campi base
        ev.title = data.get("title", ev.title)
        ev.date = data.get("date", ev.date)
        ev.location = data.get("location", ev.location)
        ev.type = data.get("type", ev.type or "artist")
        ev.format_id = data.get("format_id", ev.format_id)
        ev.promoter_id = data.get("promoter_id", ev.promoter_id)
        ev.tour_manager_id = data.get("tour_manager_id", ev.tour_manager_id)
        ev.status = data.get("status", ev.status)
        ev.notes = data.get("notes", ev.notes)

        # campi estesi
        ev.van = data.get("van", ev.van)
        ev.travel = data.get("travel", ev.travel)
        ev.hotel = data.get("hotel", ev.hotel)
        ev.allestimenti = data.get("allestimenti", ev.allestimenti)
        ev.facchini = data.get("facchini", ev.facchini)
        acconto = data.get("payments_acconto")
        saldo = data.get("payments_saldo")
        ev.payments_acconto = float(acconto) if acconto not in (None, "") else None
        ev.payments_saldo = float(saldo) if saldo not in (None, "") else None

        # format-specific selections
        ev.dj_id = data.get("dj_id", ev.dj_id)
        ev.vocalist_id = data.get("vocalist_id", ev.vocalist_id)
        # store lists as comma-separated ids
        ballerine = data.get("ballerine_ids", [])
        mascotte = data.get("mascotte_ids", [])
        ev.ballerine_ids = ",".join(str(x) for x in ballerine) if ballerine else ""
        ev.mascotte_ids = ",".join(str(x) for x in mascotte) if mascotte else ""

        # artists many-to-many
        if "artist_ids" in data:
            ev.artists = []
            for aid in data.get("artist_ids", []):
                a = db.query(Artist).get(aid)
                if a:
                    ev.artists.append(a)

        # services many-to-many
        if "service_ids" in data:
            ev.services = []
            for sid in data.get("service_ids", []):
                s = db.query(Service).get(sid)
                if s:
                    ev.services.append(s)

        db.commit()
        db.refresh(ev)
        return ev
    except SQLAlchemyError as e:
        db.rollback()
        raise
    finally:
        db.close()
