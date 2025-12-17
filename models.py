from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

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

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    title = Column(String, nullable=False)
    location = Column(String, default="")
    format_id = Column(Integer, ForeignKey("formats.id"), nullable=True)
    promoter_id = Column(Integer, ForeignKey("promoters.id"), nullable=True)
    tour_manager_id = Column(Integer, ForeignKey("tour_managers.id"), nullable=True)
    status = Column(String, default="bozza")  # bozza, confermato, cancellato
    notes = Column(Text, default="")

    artists = relationship("Artist", secondary=event_artist, back_populates="events")
    services = relationship("Service", secondary=event_service, back_populates="events")
    format = relationship("Format", back_populates="events")
    promoter = relationship("Promoter", back_populates="events")
    tour_manager = relationship("TourManager", back_populates="events")

class Artist(Base):
    __tablename__ = "artists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    contact = Column(String, default="")
    notes = Column(Text, default="")
    events = relationship("Event", secondary=event_artist, back_populates="artists")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    notes = Column(Text, default="")
    events = relationship("Event", secondary=event_service, back_populates="services")

class Format(Base):
    __tablename__ = "formats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    notes = Column(Text, default="")
    events = relationship("Event", back_populates="format")

class Promoter(Base):
    __tablename__ = "promoters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    contact = Column(String, default="")
    events = relationship("Event", back_populates="promoter")

class TourManager(Base):
    __tablename__ = "tour_managers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    contact = Column(String, default="")
    events = relationship("Event", back_populates="tour_manager")
