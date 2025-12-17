# utils.py
from db import get_session
from models import Event, Artist, Service, Format, Promoter, TourManager
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from typing import List, Optional

# -------------------------
# ARTISTI
# -------------------------
def list_artists() -> List[Artist]:
    db = get_session()
    try:
        return db.query(Artist).order_by(Artist.name).all()
    finally:
        db.close()

def list_artists_by_role(role: str) -> List[Artist]:
    db = get_session()
    try:
        return db.query(Artist).filter(Artist.role == role).order_by(Artist.name).all()
    finally:
        db.close()

def get_artist(artist_id: int) -> Optional[Artist]:
    db = get_session()
    try:
        return db.query(Artist).filter(Artist.id == artist_id).first()
    finally:
        db.close()

def add_artist(name: str, role: str = "artist", phone: str = "", email: str = "", notes: str = "") -> Artist:
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

def update_artist(artist_id: int, **fields) -> Optional[Artist]:
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

def delete_artist(artist_id: int) -> bool:
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
def list_services() -> List[Service]:
    db = get_session()
    try:
        return db.query(Service).order_by(Service.name).all()
    finally:
        db.close()

def get_service(service_id: int) -> Optional[Service]:
    db = get_session()
    try:
        return db.query(Service).filter(Service.id == service_id).first()
    finally:
        db.close()

def add_service(name: str, contact: str = "", phone: str = "", notes: str = "") -> Service:
    db = get_session()
    try:
        s = Service(name=name.strip(), contact=contact.strip(), phone=phone.strip(), notes=notes)
        db.add(s)
        db.commit()
        db.refresh(s)
        return s
    finally:
        db.close()

def update_service(service_id: int, **fields) -> Optional[Service]:
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

def delete_service(service_id: int) -> bool:
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
def list_formats() -> List[Format]:
    db = get_session()
    try:
        return db.query(Format).order_by(Format.name).all()
    finally:
        db.close()

def get_format(format_id: int) -> Optional[Format]:
    db = get_session()
    try:
        return db.query(Format).filter(Format.id == format_id).first()
    finally:
        db.close()

def add_format(name: str, description: str = "", notes: str = "") -> Format:
    db = get_session()
    try:
        f = Format(name=name.strip(), description=description, notes=notes)
        db.add(f)
        db.commit()
        db.refresh(f)
        return f
    finally:
        db.close()

def update_format(format_id: int, **fields) -> Optional[Format]:
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

def delete_format(format_id: int) -> bool:
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
def list_promoters() -> List[Promoter]:
    db = get_session()
    try:
        return db.query(Promoter).order_by(Promoter.name).all()
    finally:
        db.close()

def get_promoter(promoter_id: int) -> Optional[Promoter]:
    db = get_session()
    try:
        return db.query(Promoter).filter(Promoter.id == promoter_id).first()
    finally:
        db.close()

def add_promoter(name: str, contact: str = "", phone: str = "", email: str = "", notes: str = "") -> Promoter:
    db = get_session()
    try:
        p = Promoter(name=name.strip(), contact=contact.strip(), phone=phone.strip(), email=email.strip(), notes=notes)
        db.add(p)
        db.commit()
        db.refresh(p)
        return p
    finally:
        db.close()

def update_promoter(promoter_id: int, **fields) -> Optional[Promoter]:
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

def delete_promoter(promoter_id: int) -> bool:
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
def list_tour_managers() -> List[TourManager]:
    db = get_session()
    try:
        return db.query(TourManager).order_by(TourManager.name).all()
    finally:
        db.close()

def get_tour_manager(tm_id: int) -> Optional[TourManager]:
    db = get_session()
    try:
        return db.query(TourManager).filter(TourManager.id == tm_id).first()
    finally:
        db.close()

def add_tour_manager(name: str, contact: str = "", phone: str = "", email: str = "", notes: str = "") -> TourManager:
    db = get_session()
    try:
        t = TourManager(name=name.strip(), contact=contact.strip(), phone=phone.strip(), email=email.strip(), notes=notes)
        db.add(t)
        db.commit()
        db.refresh(t)
        return t
    finally:
        db.close()

def update_tour_manager(tm_id: int, **fields) -> Optional[TourManager]:
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

def delete_tour_manager(tm_id: int) -> bool:
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
def list_events_by_date(target_date: date) -> List[Event]:
    db = get_session()
    try:
        return db.query(Event).filter(Event.date == target_date).options(joinedload(Event.artists), joinedload(Event.services)).order_by(Event.id).all()
    finally:
        db.close()

def list_events_range(start_date: date, end_date: date) -> List[Event]:
    db = get_session()
    try:
        return db.query(Event).filter(Event.date >= start_date, Event.date <= end_date).options(joinedload(Event.artists), joinedload(Event.services)).order_by(Event.date).all()
    finally:
        db.close()

def get_event(event_id: int) -> Optional[Event]:
    if not event_id:
        return None
    db = get_session()
    try:
        return db.query(Event).options(joinedload(Event.artists), joinedload(Event.services)).filter(Event.id == event_id).first()
    finally:
        db.close()

def save_event(data: dict) -> Optional[Event]:
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
        if "title" in data:
            ev.title = data.get("title", ev.title)
        if "date" in data:
            ev.date = data.get("date", ev.date)
        if "location" in data:
            ev.location = data.get("location", ev.location)
        if "type" in data:
            ev.type = data.get("type", ev.type or "artist")
        if "format_id" in data:
            ev.format_id = data.get("format_id", ev.format_id)
        if "promoter_id" in data:
            ev.promoter_id = data.get("promoter_id", ev.promoter_id)
        if "tour_manager_id" in data:
            ev.tour_manager_id = data.get("tour_manager_id", ev.tour_manager_id)
        if "status" in data:
            ev.status = data.get("status", ev.status)
        if "notes" in data:
            ev.notes = data.get("notes", ev.notes)

        # campi estesi
        if "van" in data:
            ev.van = data.get("van", ev.van)
        if "travel" in data:
            ev.travel = data.get("travel", ev.travel)
        if "hotel" in data:
            ev.hotel = data.get("hotel", ev.hotel)
        if "allestimenti" in data:
            ev.allestimenti = data.get("allestimenti", ev.allestimenti)
        if "facchini" in data:
            ev.facchini = data.get("facchini", ev.facchini)

        if "payments_acconto" in data:
            acconto = data.get("payments_acconto")
            ev.payments_acconto = float(acconto) if acconto not in (None, "") else None
        if "payments_saldo" in data:
            saldo = data.get("payments_saldo")
            ev.payments_saldo = float(saldo) if saldo not in (None, "") else None

        # format-specific selections
        if "dj_id" in data:
            ev.dj_id = data.get("dj_id", ev.dj_id)
        if "vocalist_id" in data:
            ev.vocalist_id = data.get("vocalist_id", ev.vocalist_id)
        if "ballerine_ids" in data:
            ballerine = data.get("ballerine_ids", [])
            ev.ballerine_ids = ",".join(str(x) for x in ballerine) if ballerine else ""
        if "mascotte_ids" in data:
            mascotte = data.get("mascotte_ids", [])
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

def duplicate_event(event_id: int) -> Optional[Event]:
    db = get_session()
    try:
        ev = db.query(Event).get(event_id)
        if not ev:
            return None
        new = Event(
            date=ev.date,
            title=f"{ev.title} (Copia)",
            location=ev.location,
            type=ev.type,
            format_id=ev.format_id,
            promoter_id=ev.promoter_id,
            tour_manager_id=ev.tour_manager_id,
            status="bozza",
            notes=ev.notes,
            van=ev.van,
            travel=ev.travel,
            hotel=ev.hotel,
            allestimenti=ev.allestimenti,
            facchini=ev.facchini,
            payments_acconto=ev.payments_acconto,
            payments_saldo=ev.payments_saldo,
            dj_id=ev.dj_id,
            vocalist_id=ev.vocalist_id,
            ballerine_ids=ev.ballerine_ids,
            mascotte_ids=ev.mascotte_ids
        )
        for a in ev.artists:
            new.artists.append(a)
        for s in ev.services:
            new.services.append(s)
        db.add(new)
        db.commit()
        db.refresh(new)
        return new
    finally:
        db.close()

def delete_event(event_id: int) -> bool:
    db = get_session()
    try:
        ev = db.query(Event).get(event_id)
        if not ev:
            return False
        db.delete(ev)
        db.commit()
        return True
    finally:
        db.close()

# -------------------------
# UTILITY / FILTRI
# -------------------------
def filter_events_by_artist(events: List[Event], artist_id: int) -> List[Event]:
    return [e for e in events if any(a.id == artist_id for a in e.artists)]

def filter_events(events: List[Event], *, type_: Optional[str] = None, status: Optional[str] = None) -> List[Event]:
    res = events
    if type_:
        res = [e for e in res if e.type == type_]
    if status:
        res = [e for e in res if e.status == status]
    return res
