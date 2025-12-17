# utils.py
from db import get_session
from models import Event, Artist, Service, Format, Promoter, TourManager
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

# -------------------------
# ARTISTI
# -------------------------
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

def get_artist(artist_id):
    db = get_session()
    try:
        return db.query(Artist).filter(Artist.id == artist_id).first()
    finally:
        db.close()

def add_artist(name, role="artist", phone="", email="", notes=""):
    db = get_session()
    try:
        a = Artist(name=name.strip(), role=role, phone=phone.strip(), email=email.strip(), notes=notes)
        db.add(a)
        db.commit()
        db.refresh(a)
        return a
    except SQLAlchemyError:
        db.rollback()
        raise
    finally:
        db.close()

def update_artist(artist_id, **fields):
    db = get_session()
    try:
        a = db.query(Artist).get(artist_id)
        if not a:
            return None
        for k, v in fields.items():
            if hasattr(a, k):
                setattr(a, k, v)
        db.commit()
        db.refresh(a)
        return a
    finally:
        db.close()

def delete_artist(artist_id):
    db = get_session()
    try:
        a = db.query(Artist).get(artist_id)
        if not a:
            return False
        db.delete(a)
        db.commit()
        return True
    finally:
        db.close()

# -------------------------
# SERVICES
# -------------------------
def list_services():
    db = get_session()
    try:
        return db.query(Service).order_by(Service.name).all()
    finally:
        db.close()

def get_service(service_id):
    db = get_session()
    try:
        return db.query(Service).filter(Service.id == service_id).first()
    finally:
        db.close()

def add_service(name, contact="", phone="", notes=""):
    db = get_session()
    try:
        s = Service(name=name.strip(), contact=contact.strip(), phone=phone.strip(), notes=notes)
        db.add(s)
        db.commit()
        db.refresh(s)
        return s
    finally:
        db.close()

def update_service(service_id, **fields):
    db = get_session()
    try:
        s = db.query(Service).get(service_id)
        if not s:
            return None
        for k, v in fields.items():
            if hasattr(s, k):
                setattr(s, k, v)
        db.commit()
        db.refresh(s)
        return s
    finally:
        db.close()

def delete_service(service_id):
    db = get_session()
    try:
        s = db.query(Service).get(service_id)
        if not s:
            return False
        db.delete(s)
        db.commit()
        return True
    finally:
        db.close()

# -------------------------
# FORMATS
# -------------------------
def list_formats():
    db = get_session()
    try:
        return db.query(Format).order_by(Format.name).all()
    finally:
        db.close()

def get_format(format_id):
    db = get_session()
    try:
        return db.query(Format).filter(Format.id == format_id).first()
    finally:
        db.close()

def add_format(name, description="", notes=""):
    db = get_session()
    try:
        f = Format(name=name.strip(), description=description, notes=notes)
        db.add(f)
        db.commit()
        db.refresh(f)
        return f
    finally:
        db.close()

def update_format(format_id, **fields):
    db = get_session()
    try:
        f = db.query(Format).get(format_id)
        if not f:
            return None
        for k, v in fields.items():
            if hasattr(f, k):
                setattr(f, k, v)
        db.commit()
        db.refresh(f)
        return f
    finally:
        db.close()

def delete_format(format_id):
    db = get_session()
    try:
        f = db.query(Format).get(format_id)
        if not f:
            return False
        db.delete(f)
        db.commit()
        return True
    finally:
        db.close()

# -------------------------
# PROMOTER
# -------------------------
def list_promoters():
    db = get_session()
    try:
        return db.query(Promoter).order_by(Promoter.name).all()
    finally:
        db.close()

def get_promoter(promoter_id):
    db = get_session()
    try:
        return db.query(Promoter).filter(Promoter.id == promoter_id).first()
    finally:
        db.close()

def add_promoter(name, contact="", phone="", email="", notes=""):
    db = get_session()
    try:
        p = Promoter(name=name.strip(), contact=contact.strip(), phone=phone.strip(), email=email.strip(), notes=notes)
        db.add(p)
        db.commit()
        db.refresh(p)
        return p
    finally:
        db.close()

def update_promoter(promoter_id, **fields):
    db = get_session()
    try:
        p = db.query(Promoter).get(promoter_id)
        if not p:
            return None
        for k, v in fields.items():
            if hasattr(p, k):
                setattr(p, k, v)
        db.commit()
        db.refresh(p)
        return p
    finally:
        db.close()

def delete_promoter(promoter_id):
    db = get_session()
    try:
        p = db.query(Promoter).get(promoter_id)
        if not p:
            return False
        db.delete(p)
        db.commit()
        return True
    finally:
        db.close()

# -------------------------
# TOUR MANAGER
# -------------------------
def list_tour_managers():
    db = get_session()
    try:
        return db.query(TourManager).order_by(TourManager.name).all()
    finally:
        db.close()

def get_tour_manager(tm_id):
    db = get_session()
    try:
        return db.query(TourManager).filter(TourManager.id == tm_id).first()
    finally:
        db.close()

def add_tour_manager(name, contact="", phone="", email="", notes=""):
    db = get_session()
    try:
        t = TourManager(name=name.strip(), contact=contact.strip(), phone=phone.strip(), email=email.strip(), notes=notes)
        db.add(t)
        db.commit()
        db.refresh(t)
        return t
    finally:
        db.close()

def update_tour_manager(tm_id, **fields):
    db = get_session()
    try:
        t = db.query(TourManager).get(tm_id)
        if not t:
            return None
        for k, v in fields.items():
            if hasattr(t, k):
                setattr(t, k, v)
        db.commit()
        db.refresh(t)
        return t
    finally:
        db.close()

def delete_tour_manager(tm_id):
    db = get_session()
    try:
        t = db.query(TourManager).get(tm_id)
        if not t:
            return False
        db.delete(t)
        db.commit()
        return True
    finally:
        db.close()

# -------------------------
# EVENTI
# -------------------------
def list_events_by_date(target_date):
    db = get_session()
    try:
        return db.query(Event).filter(Event.date == target_date).options(joinedload(Event.artists), joinedload(Event.services)).order_by(Event.id).all()
    finally:
        db.close()

def get_event(event_id):
    db = get_session()
    try:
        return db.query(Event).options(joinedload(Event.artists), joinedload(Event.services)).filter(Event.id == event_id).first()
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
    except SQLAlchemyError:
        db.rollback()
        raise
    finally:
        db.close()
