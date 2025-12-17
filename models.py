# models.py
from sqlalchemy import (
    Column, Integer, String, Date, Table, ForeignKey, Text, Float,
    DateTime, Boolean, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

# association tables many-to-many
event_artist = Table(
    "event_artist",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id")),
    Column("artist_id", Integer, ForeignKey("artists.id"))
)

event_service = Table(
    "event_service",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id")),
    Column("service_id", Integer, ForeignKey("services.id"))
)

# -------------------------
# CORE ENTITIES
# -------------------------
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    title = Column(String, nullable=False, default="")
    location = Column(String, default="")
    type = Column(String, default="artist")  # "artist" or "format"
    format_id = Column(Integer, ForeignKey("formats.id"), nullable=True)
    promoter_id = Column(Integer, ForeignKey("promoters.id"), nullable=True)
    tour_manager_id = Column(Integer, ForeignKey("tour_managers.id"), nullable=True)
    status = Column(String, default="bozza")
    notes = Column(Text, default="")

    van = Column(String, default="")
    travel = Column(String, default="")
    hotel = Column(String, default="")
    allestimenti = Column(Text, default="")
    facchini = Column(String, default="")
    payments_acconto = Column(Float, nullable=True)
    payments_saldo = Column(Float, nullable=True)

    dj_id = Column(Integer, nullable=True)
    vocalist_id = Column(Integer, nullable=True)
    ballerine_ids = Column(String, default="")   # comma separated ids
    mascotte_ids = Column(String, default="")    # comma separated ids

    # relations
    artists = relationship("Artist", secondary=event_artist, back_populates="events")
    services = relationship("Service", secondary=event_service, back_populates="events")
    format = relationship("Format", back_populates="events")
    promoter = relationship("Promoter", back_populates="events")
    tour_manager = relationship("TourManager", back_populates="events")

class Artist(Base):
    __tablename__ = "artists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    role = Column(String, default="artist")
    phone = Column(String, default="")
    email = Column(String, default="")
    notes = Column(Text, default="")
    events = relationship("Event", secondary=event_artist, back_populates="artists")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    contact = Column(String, default="")
    phone = Column(String, default="")
    notes = Column(Text, default="")
    events = relationship("Event", secondary=event_service, back_populates="services")
    assignments = relationship("ServiceAssignment", back_populates="service")

class Format(Base):
    __tablename__ = "formats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, default="")
    notes = Column(Text, default="")
    events = relationship("Event", back_populates="format")

class Promoter(Base):
    __tablename__ = "promoters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    contact = Column(String, default="")
    phone = Column(String, default="")
    email = Column(String, default="")
    notes = Column(Text, default="")
    events = relationship("Event", back_populates="promoter")

class TourManager(Base):
    __tablename__ = "tour_managers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    contact = Column(String, default="")
    phone = Column(String, default="")
    email = Column(String, default="")
    notes = Column(Text, default="")
    events = relationship("Event", back_populates="tour_manager")

# -------------------------
# TASKS, AUDIT, ASSIGNMENTS
# -------------------------
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    assignee = Column(String, default="")
    due_date = Column(Date, nullable=True)
    done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", backref="tasks")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    entity = Column(String, nullable=False)         # "event","task","service",...
    entity_id = Column(Integer, nullable=True)
    action = Column(String, nullable=False)         # "create","update","delete","move_date",...
    payload = Column(Text, default="")              # json snapshot
    user = Column(String, default="")
    ts = Column(DateTime, default=datetime.utcnow)

class ServiceAssignment(Base):
    __tablename__ = "service_assignments"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    __table_args__ = (UniqueConstraint('service_id', 'date', name='uq_service_date'),)

    event = relationship("Event", backref="service_assignments")
    service = relationship("Service", back_populates="assignments")

# -------------------------
# EXTERNAL INTEGRATIONS
# -------------------------
class ExternalAccount(Base):
    __tablename__ = "external_accounts"
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, nullable=False)           # "google" or "microsoft"
    user = Column(String, default="")                   # username interno che ha collegato l'account
    account_id = Column(String, default="")             # id account provider
    access_token = Column(Text)
    refresh_token = Column(Text)
    token_expires_at = Column(DateTime, nullable=True)
    scopes = Column(Text, default="")

# -------------------------
# TEMPLATES
# -------------------------
class EventTemplate(Base):
    __tablename__ = "event_templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, default="artist")
    description = Column(Text, default="")
    required_fields = Column(Text, default="")   # JSON list of required field names
    notes = Column(Text, default="")

class TaskTemplate(Base):
    __tablename__ = "task_templates"
    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    offset_days = Column(Integer, default=0)   # offset relative alla data evento (es. -7)
    # template_name può essere collegato a EventTemplate.name
