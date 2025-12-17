# utils.py
from db import get_session
from models import Event, Artist, Service, Format, Promoter, TourManager
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

def list_artists():
    db = get_session()
    try:
        items = db.query(Artist).order_by(Artist.name).all()
        return items
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
    except SQLAlchemyError as e:
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

# Services
def list_services():
    db = get_session()
    try:
        return db.query(Service).order_by(Service.name).all()
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

# Formats
def list_formats():
    db = get_session()
    try:
        return db.query(Format).order_by(Format.name).all()
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

# Promoters
def list_promoters():
    db = get_session()
    try:
        return db.query(Promoter).order_by(Promoter.name).all()
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

# Tour managers
def list_tour_managers():
    db = get_session()
    try:
        return db.query(TourManager).order_by(TourManager.name).all()
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
