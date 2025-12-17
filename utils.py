# utils.py
from db import get_session
from models import (
    Event, Artist, Service, Format, Promoter, TourManager,
    Task, AuditLog, ServiceAssignment, ExternalAccount,
    EventTemplate, TaskTemplate
)
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, datetime, timedelta
from typing import List, Optional, Dict, Any
import json
import os
# debug wrapper (temporaneo)
def add_artist_debug(name: str, role: str = "artist", phone: str = "", email: str = "", notes: str = ""):
    from sqlalchemy.exc import SQLAlchemyError
    try:
        return add_artist(name=name, role=role, phone=phone, email=email, notes=notes)
    except SQLAlchemyError as e:
        # stampa l'errore DBAPI sottostante
        print("SQLAlchemyError:", e)
        if hasattr(e, "orig"):
            print("DBAPI error:", e.orig)
        raise
# -------------------------
# HELPERS GENERICI
# -------------------------
def _commit_and_refresh(db, obj):
    try:
        db.commit()
        db.refresh(obj)
        return obj
    except Exception:
        db.rollback()
        raise

def record_audit(entity: str, entity_id: int, action: str, payload: Dict[str, Any], user: str = ""):
    db = get_session()
    try:
        a = AuditLog(entity=entity, entity_id=entity_id, action=action, payload=json.dumps(payload, default=str), user=user, ts=datetime.utcnow())
        db.add(a)
        db.commit()
    finally:
        db.close()

def get_audit_logs(entity: str = None, entity_id: int = None, limit: int = 100) -> List[AuditLog]:
    db = get_session()
    try:
        q = db.query(AuditLog).order_by(AuditLog.ts.desc())
        if entity:
            q = q.filter(AuditLog.entity == entity)
        if entity_id:
            q = q.filter(AuditLog.entity_id == entity_id)
        return q.limit(limit).all()
    finally:
        db.close()

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

def add_artist(name: str, role: str = "artist", phone: str = "", email: str = "", notes: str = "") -> Artist:
    db = get_session()
    try:
        a = Artist(name=name.strip(), role=role, phone=phone.strip(), email=email.strip(), notes=notes)
        db.add(a)
        db.commit()
        db.refresh(a)
        record_audit("artist", a.id, "create", {"name": a.name})
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
        before = {k: getattr(a, k) for k in fields.keys() if hasattr(a, k)}
        for k, v in fields.items():
            if hasattr(a, k):
                setattr(a, k, v)
        db.commit()
        db.refresh(a)
        record_audit("artist", artist_id, "update", {"before": before, "after": fields})
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
        record_audit("artist", artist_id, "delete", {"id": artist_id})
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
        record_audit("service", s.id, "create", {"name": s.name})
        return s
    finally:
        db.close()

def update_service(service_id: int, **fields) -> Optional[Service]:
    db = get_session()
    try:
        s = db.query(Service).get(service_id)
        if not s:
            return None
        before = {k: getattr(s, k) for k in fields.keys() if hasattr(s, k)}
        for k, v in fields.items():
            if hasattr(s, k):
                setattr(s, k, v)
        db.commit()
        db.refresh(s)
        record_audit("service", service_id, "update", {"before": before, "after": fields})
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
        record_audit("service", service_id, "delete", {"id": service_id})
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

def add_format(name: str, description: str = "", notes: str = "") -> Format:
    db = get_session()
    try:
        f = Format(name=name.strip(), description=description, notes=notes)
        db.add(f)
        db.commit()
        db.refresh(f)
        record_audit("format", f.id, "create", {"name": f.name})
        return f
    finally:
        db.close()

def update_format(format_id: int, **fields) -> Optional[Format]:
    db = get_session()
    try:
        f = db.query(Format).get(format_id)
        if not f:
            return None
        before = {k: getattr(f, k) for k in fields.keys() if hasattr(f, k)}
        for k, v in fields.items():
            if hasattr(f, k):
                setattr(f, k, v)
        db.commit()
        db.refresh(f)
        record_audit("format", format_id, "update", {"before": before, "after": fields})
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
        record_audit("format", format_id, "delete", {"id": format_id})
        return True
    finally:
        db.close()

# -------------------------
# PROMOTER / TOUR MANAGER
# -------------------------
def list_promoters() -> List[Promoter]:
    db = get_session()
    try:
        return db.query(Promoter).order_by(Promoter.name).all()
    finally:
        db.close()

def list_tour_managers() -> List[TourManager]:
    db = get_session()
    try:
        return db.query(TourManager).order_by(TourManager.name).all()
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

def upcoming_events(days: int = 7) -> List[Event]:
    db = get_session()
    try:
        today = date.today()
        end = today + timedelta(days=days)
        return db.query(Event).filter(Event.date >= today, Event.date <= end).order_by(Event.date).all()
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

# -------------------------
# SERVICE AVAILABILITY (conflitti)
# -------------------------
def check_services_availability(date_obj: date, service_ids: List[int], exclude_event_id: Optional[int] = None) -> List[int]:
    """
    Restituisce gli id dei service in conflitto per la data specificata.
    """
    db = get_session()
    try:
        conflicts = []
        for sid in service_ids:
            q = db.query(ServiceAssignment).filter(
                ServiceAssignment.service_id == sid,
                ServiceAssignment.date == date_obj
            )
            if exclude_event_id:
                q = q.filter(ServiceAssignment.event_id != exclude_event_id)
            if q.first():
                conflicts.append(sid)
        return conflicts
    finally:
        db.close()

def assign_services_to_event(db, event_obj: Event, service_ids: List[int]):
    """
    Usa la sessione db passata per aggiornare le assegnazioni service per l'evento.
    Non esegue commit.
    """
    # rimuovi assegnazioni esistenti per questo evento
    db.query(ServiceAssignment).filter(ServiceAssignment.event_id == event_obj.id).delete()
    for sid in service_ids:
        sa = ServiceAssignment(event_id=event_obj.id, service_id=sid, date=event_obj.date)
        db.add(sa)

# -------------------------
# SAVE / DUPLICATE / DELETE EVENT con controllo service
# -------------------------
def save_event(data: dict, user: str = "") -> Optional[Event]:
    """
    Salva o aggiorna un evento. Se viene passato 'service_ids' controlla conflitti e aggiorna ServiceAssignment.
    """
    db = get_session()
    try:
        if data.get("id"):
            ev = db.query(Event).get(data["id"])
            if not ev:
                return None
            before = {k: getattr(ev, k) for k in data.keys() if hasattr(ev, k)}
        else:
            ev = Event()
            db.add(ev)
            before = {}

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

        # campi logistici
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

        # format-specific
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

        # services many-to-many + ServiceAssignment check
        if "service_ids" in data:
            service_ids = data.get("service_ids", [])
            # controlla conflitti
            conflicts = check_services_availability(ev.date, service_ids, exclude_event_id=ev.id if data.get("id") else None)
            if conflicts:
                raise ValueError(f"Service in conflitto per la data {ev.date}: {conflicts}")
            # aggiorna relazione many-to-many (per compatibilità) e le assegnazioni esplicite
            ev.services = []
            for sid in service_ids:
                s = db.query(Service).get(sid)
                if s:
                    ev.services.append(s)
            # assegna usando la sessione corrente
            assign_services_to_event(db, ev, service_ids)

        db.commit()
        db.refresh(ev)
        record_audit("event", ev.id, "create" if not data.get("id") else "update", {"before": before, "after": data}, user=user)

        # se richiesto, pubblica su calendar esterno (opzionale)
        if data.get("publish_calendar_account_id") and data.get("status") == "confermato":
            try:
                from integrations.calendar_sync import push_event_to_calendar
                push_event_to_calendar(data.get("publish_calendar_account_id"), ev)
            except Exception as e:
                record_audit("event", ev.id, "calendar_push_failed", {"error": str(e)}, user=user)

        return ev
    except SQLAlchemyError:
        db.rollback()
        raise
    finally:
        db.close()

def duplicate_event(event_id: int, user: str = "") -> Optional[Event]:
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
        # copia assegnazioni service se presenti (rispettando vincoli)
        for sa in ev.service_assignments:
            try:
                new_sa = ServiceAssignment(event_id=new.id, service_id=sa.service_id, date=new.date)
                db.add(new_sa)
            except Exception:
                # se vincolo unique fallisce, ignora
                pass
        db.commit()
        db.refresh(new)
        record_audit("event", new.id, "create", {"source_event": ev.id}, user=user)
        return new
    finally:
        db.close()

def delete_event(event_id: int, user: str = "") -> bool:
    db = get_session()
    try:
        ev = db.query(Event).get(event_id)
        if not ev:
            return False
        # elimina task e service assignments legate
        db.query(Task).filter(Task.event_id == event_id).delete()
        db.query(ServiceAssignment).filter(ServiceAssignment.event_id == event_id).delete()
        db.delete(ev)
        db.commit()
        record_audit("event", event_id, "delete", {"id": event_id}, user=user)
        return True
    finally:
        db.close()

def move_event_date(event_id: int, new_date: date, user: str = "") -> Optional[Event]:
    db = get_session()
    try:
        ev = db.query(Event).get(event_id)
        if not ev:
            return None
        before = {"date": ev.date.isoformat() if ev.date else None}
        # controlla conflitti per service assegnati
        service_ids = [sa.service_id for sa in ev.service_assignments]
        conflicts = check_services_availability(new_date, service_ids, exclude_event_id=ev.id)
        if conflicts:
            raise ValueError(f"Conflitto service per la nuova data {new_date}: {conflicts}")
        ev.date = new_date
        # aggiorna service assignments date
        for sa in ev.service_assignments:
            sa.date = new_date
        db.commit()
        db.refresh(ev)
        record_audit("event", event_id, "move_date", {"before": before, "after": {"date": new_date.isoformat()}}, user=user)
        return ev
    finally:
        db.close()

# -------------------------
# TASKS
# -------------------------
def list_tasks_by_date(target_date: date) -> List[Task]:
    db = get_session()
    try:
        return db.query(Task).filter(Task.due_date == target_date).order_by(Task.done, Task.created_at).all()
    finally:
        db.close()

def list_tasks_for_event(event_id: int) -> List[Task]:
    db = get_session()
    try:
        return db.query(Task).filter(Task.event_id == event_id).order_by(Task.done, Task.created_at).all()
    finally:
        db.close()

def add_task(event_id: int, title: str, description: str = "", assignee: str = "", due_date: Optional[date] = None, user: str = "") -> Task:
    db = get_session()
    try:
        t = Task(event_id=event_id, title=title.strip(), description=description, assignee=assignee, due_date=due_date)
        db.add(t)
        db.commit()
        db.refresh(t)
        record_audit("task", t.id, "create", {"title": t.title, "event_id": event_id}, user=user)
        return t
    finally:
        db.close()

def update_task(task_id: int, **fields) -> Optional[Task]:
    db = get_session()
    try:
        t = db.query(Task).get(task_id)
        if not t:
            return None
        before = {k: getattr(t, k) for k in fields.keys() if hasattr(t, k)}
        for k, v in fields.items():
            if hasattr(t, k):
                setattr(t, k, v)
        db.commit()
        db.refresh(t)
        record_audit("task", task_id, "update", {"before": before, "after": fields})
        return t
    finally:
        db.close()

def delete_task(task_id: int, user: str = "") -> bool:
    db = get_session()
    try:
        t = db.query(Task).get(task_id)
        if not t:
            return False
        db.delete(t)
        db.commit()
        record_audit("task", task_id, "delete", {"id": task_id}, user=user)
        return True
    finally:
        db.close()

def toggle_task_done(task_id: int, user: str = "") -> Optional[Task]:
    db = get_session()
    try:
        t = db.query(Task).get(task_id)
        if not t:
            return None
        t.done = not bool(t.done)
        db.commit()
        db.refresh(t)
        record_audit("task", task_id, "toggle_done", {"done": t.done}, user=user)
        return t
    finally:
        db.close()

def get_user_tasks(username: str, only_open: bool = True) -> List[Task]:
    """
    Restituisce le task assegnate a un utente.
    - username: stringa che identifica l'assignee (es. username o email).
    - only_open: se True ritorna solo le task non completate.
    """
    db = get_session()
    try:
        q = db.query(Task).filter(Task.assignee == username)
        if only_open:
            q = q.filter(Task.done == False)
        return q.order_by(Task.due_date, Task.created_at).all()
    finally:
        db.close()

# -------------------------
# TEMPLATES E CHECKLIST
# -------------------------
def list_event_templates() -> List[EventTemplate]:
    db = get_session()
    try:
        return db.query(EventTemplate).order_by(EventTemplate.name).all()
    finally:
        db.close()

def list_task_templates_for(template_name: str) -> List[TaskTemplate]:
    db = get_session()
    try:
        return db.query(TaskTemplate).filter(TaskTemplate.template_name == template_name).order_by(TaskTemplate.offset_days).all()
    finally:
        db.close()

def apply_template_to_event(event_id: int, template_name: str, user: str = ""):
    db = get_session()
    try:
        ev = db.query(Event).get(event_id)
        if not ev:
            return None
        tasks = list_task_templates_for(template_name)
        created = []
        for t in tasks:
            due = ev.date + timedelta(days=t.offset_days)
            task = Task(event_id=ev.id, title=t.title, description=t.description, assignee="", due_date=due)
            db.add(task)
            created.append(task)
        db.commit()
        for c in created:
            db.refresh(c)
            record_audit("task", c.id, "create_from_template", {"template": template_name, "event_id": event_id}, user=user)
        return created
    finally:
        db.close()

# compatibilità: create_tasks_from_template wrapper
def create_tasks_from_template(event_id: int, template_name: str, assignee: str = "", due_date: Optional[date] = None, user: str = "") -> List[Task]:
    """
    Wrapper compatibile con chiamate esistenti.
    - Se esistono TaskTemplate per template_name usa apply_template_to_event.
    - Altrimenti crea tasks da un fallback minimale.
    """
    try:
        templates = list_task_templates_for(template_name)
    except Exception:
        templates = []

    if templates:
        return apply_template_to_event(event_id, template_name, user=user)

    FALLBACK_TEMPLATES = {
        "format_checklist": [
            {"title": "Confermare DJ", "description": "Verificare disponibilità e rider", "offset_days": -7},
            {"title": "Confermare Vocalist", "description": "Contattare vocalist e confermare set", "offset_days": -7},
            {"title": "Allestimenti", "description": "Verificare palco e luci", "offset_days": -3},
            {"title": "Hotel", "description": "Controllare prenotazioni hotel", "offset_days": -3}
        ],
        "artist_checklist": [
            {"title": "Rider tecnico", "description": "Inviare e confermare rider", "offset_days": -7},
            {"title": "Facchini", "description": "Confermare numero facchini", "offset_days": -3},
            {"title": "Trasporti", "description": "Organizzare van e viaggi", "offset_days": -2}
        ]
    }

    items = FALLBACK_TEMPLATES.get(template_name, [])
    db = get_session()
    created = []
    try:
        ev = db.query(Event).get(event_id)
        if not ev:
            return []
        for it in items:
            offset = it.get("offset_days", 0)
            due = (ev.date + timedelta(days=offset)) if ev.date else due_date
            t = Task(event_id=event_id, title=it["title"], description=it.get("description",""), assignee=assignee, due_date=due)
            db.add(t)
            created.append(t)
        db.commit()
        for t in created:
            db.refresh(t)
            record_audit("task", t.id, "create_from_fallback_template", {"template": template_name, "event_id": event_id}, user=user)
        return created
    finally:
        db.close()

# -------------------------
# EXPORT / IMPORT JSON
# -------------------------
def export_data_json(path: str) -> None:
    db = get_session()
    try:
        data = {"artists": [], "services": [], "formats": [], "promoters": [], "tour_managers": [], "events": [], "tasks": [], "audit_logs": []}
        for a in db.query(Artist).all():
            data["artists"].append({"id": a.id, "name": a.name, "role": a.role, "phone": a.phone, "email": a.email, "notes": a.notes})
        for s in db.query(Service).all():
            data["services"].append({"id": s.id, "name": s.name, "contact": s.contact, "phone": s.phone, "notes": s.notes})
        for f in db.query(Format).all():
            data["formats"].append({"id": f.id, "name": f.name, "description": f.description, "notes": f.notes})
        for p in db.query(Promoter).all():
            data["promoters"].append({"id": p.id, "name": p.name, "contact": p.contact, "phone": p.phone, "email": p.email, "notes": p.notes})
        for t in db.query(TourManager).all():
            data["tour_managers"].append({"id": t.id, "name": t.name, "contact": t.contact, "phone": t.phone, "email": t.email, "notes": t.notes})
        for e in db.query(Event).all():
            data["events"].append({
                "id": e.id, "date": e.date.isoformat() if e.date else None, "title": e.title, "location": e.location,
                "type": e.type, "format_id": e.format_id, "promoter_id": e.promoter_id, "tour_manager_id": e.tour_manager_id,
                "status": e.status, "notes": e.notes, "van": e.van, "travel": e.travel, "hotel": e.hotel,
                "allestimenti": e.allestimenti, "facchini": e.facchini, "payments_acconto": e.payments_acconto,
                "payments_saldo": e.payments_saldo, "dj_id": e.dj_id, "vocalist_id": e.vocalist_id,
                "ballerine_ids": e.ballerine_ids, "mascotte_ids": e.mascotte_ids,
                "artist_ids": [a.id for a in e.artists], "service_ids": [s.id for s in e.services]
            })
        for tk in db.query(Task).all():
            data["tasks"].append({
                "id": tk.id, "event_id": tk.event_id, "title": tk.title, "description": tk.description,
                "assignee": tk.assignee, "due_date": tk.due_date.isoformat() if tk.due_date else None, "done": bool(tk.done)
            })
        for al in db.query(AuditLog).order_by(AuditLog.ts.asc()).all():
            data["audit_logs"].append({"id": al.id, "entity": al.entity, "entity_id": al.entity_id, "action": al.action, "payload": al.payload, "user": al.user, "ts": al.ts.isoformat()})
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    finally:
        db.close()

def import_data_json(path: str, clear_existing: bool = False) -> None:
    db = get_session()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if clear_existing:
            db.query(AuditLog).delete()
            db.query(Task).delete()
            db.query(ServiceAssignment).delete()
            db.query(Event).delete()
            db.query(Artist).delete()
            db.query(Service).delete()
            db.query(Format).delete()
            db.query(Promoter).delete()
            db.query(TourManager).delete()
            db.commit()
        # import base entities (no id preservation)
        for a in data.get("artists", []):
            db.add(Artist(name=a.get("name",""), role=a.get("role",""), phone=a.get("phone",""), email=a.get("email",""), notes=a.get("notes","")))
        for s in data.get("services", []):
            db.add(Service(name=s.get("name",""), contact=s.get("contact",""), phone=s.get("phone",""), notes=s.get("notes","")))
        for f in data.get("formats", []):
            db.add(Format(name=f.get("name",""), description=f.get("description",""), notes=f.get("notes","")))
        for p in data.get("promoters", []):
            db.add(Promoter(name=p.get("name",""), contact=p.get("contact",""), phone=p.get("phone",""), email=p.get("email",""), notes=p.get("notes","")))
        for t in data.get("tour_managers", []):
            db.add(TourManager(name=t.get("name",""), contact=t.get("contact",""), phone=t.get("phone",""), email=t.get("email",""), notes=t.get("notes","")))
        db.commit()
    finally:
        db.close()

# -------------------------
# PLACEHOLDERS INTEGRAZIONI (Calendar / Notifications)
# -------------------------
def push_event_to_calendar_stub(account_id: int, event_obj: Event):
    """
    Placeholder: implementare integrazione reale in integrations/calendar_sync.py
    Questo stub registra un audit e solleva NotImplementedError per ricordare l'implementazione.
    """
    record_audit("integration", None, "calendar_push_stub", {"account_id": account_id, "event_id": event_obj.id})
    raise NotImplementedError("push_event_to_calendar non implementato. Vedi integrations/calendar_sync.py")

def send_email_stub(to_email: str, subject: str, body: str):
    """
    Placeholder per invio email. Implementare in integrations/notifications.py
    """
    record_audit("integration", None, "email_stub", {"to": to_email, "subject": subject})

def send_slack_stub(webhook_url: str, text: str):
    record_audit("integration", None, "slack_stub", {"webhook": webhook_url, "text": text})

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

def events_without_dj(start_date: date, end_date: date) -> List[Event]:
    db = get_session()
    try:
        return db.query(Event).filter(Event.date >= start_date, Event.date <= end_date, (Event.dj_id == None)).order_by(Event.date).all()
    finally:
        db.close()

def events_without_promoter(start_date: date, end_date: date) -> List[Event]:
    db = get_session()
    try:
        return db.query(Event).filter(Event.date >= start_date, Event.date <= end_date, (Event.promoter_id == None)).order_by(Event.date).all()
    finally:
        db.close()
# PROMOTER / TOUR MANAGER - funzioni CRUD per promoter (aggiungi in utils.py)
def add_promoter(name: str, contact: str = "", phone: str = "", email: str = "", notes: str = "") -> Promoter:
    """
    Crea un nuovo promoter e registra l'audit.
    """
    db = get_session()
    try:
        p = Promoter(name=name.strip(), contact=contact.strip(), phone=phone.strip(), email=email.strip(), notes=notes)
        db.add(p)
        db.commit()
        db.refresh(p)
        record_audit("promoter", p.id, "create", {"name": p.name})
        return p
    except SQLAlchemyError:
        db.rollback()
        raise
    finally:
        db.close()

def update_promoter(promoter_id: int, **fields) -> Optional[Promoter]:
    """
    Aggiorna un promoter esistente. Restituisce l'oggetto aggiornato o None se non trovato.
    """
    db = get_session()
    try:
        p = db.query(Promoter).get(promoter_id)
        if not p:
            return None
        before = {k: getattr(p, k) for k in fields.keys() if hasattr(p, k)}
        for k, v in fields.items():
            if hasattr(p, k):
                setattr(p, k, v)
        db.commit()
        db.refresh(p)
        record_audit("promoter", promoter_id, "update", {"before": before, "after": fields})
        return p
    finally:
        db.close()

def delete_promoter(promoter_id: int) -> bool:
    """
    Elimina un promoter e registra l'audit. Restituisce True se eliminato, False se non trovato.
    """
    db = get_session()
    try:
        p = db.query(Promoter).get(promoter_id)
        if not p:
            return False
        # opzionale: verificare referenze (eventi) prima di cancellare
        db.delete(p)
        db.commit()
        record_audit("promoter", promoter_id, "delete", {"id": promoter_id})
        return True
    finally:
        db.close()
# TOUR MANAGER - funzioni CRUD (aggiungi in utils.py)
def add_tour_manager(name: str, contact: str = "", phone: str = "", email: str = "", notes: str = "") -> TourManager:
    """
    Crea un nuovo tour manager e registra l'audit.
    """
    db = get_session()
    try:
        t = TourManager(name=name.strip(), contact=contact.strip(), phone=phone.strip(), email=email.strip(), notes=notes)
        db.add(t)
        db.commit()
        db.refresh(t)
        record_audit("tour_manager", t.id, "create", {"name": t.name})
        return t
    except SQLAlchemyError:
        db.rollback()
        raise
    finally:
        db.close()

def update_tour_manager(tour_manager_id: int, **fields) -> Optional[TourManager]:
    """
    Aggiorna un tour manager esistente. Restituisce l'oggetto aggiornato o None se non trovato.
    """
    db = get_session()
    try:
        t = db.query(TourManager).get(tour_manager_id)
        if not t:
            return None
        before = {k: getattr(t, k) for k in fields.keys() if hasattr(t, k)}
        for k, v in fields.items():
            if hasattr(t, k):
                setattr(t, k, v)
        db.commit()
        db.refresh(t)
        record_audit("tour_manager", tour_manager_id, "update", {"before": before, "after": fields})
        return t
    finally:
        db.close()

def delete_tour_manager(tour_manager_id: int) -> bool:
    """
    Elimina un tour manager e registra l'audit. Restituisce True se eliminato, False se non trovato.
    """
    db = get_session()
    try:
        t = db.query(TourManager).get(tour_manager_id)
        if not t:
            return False
        # opzionale: verificare referenze (eventi) prima di cancellare
        db.delete(t)
        db.commit()
        record_audit("tour_manager", tour_manager_id, "delete", {"id": tour_manager_id})
        return True
    finally:
        db.close()
