from sqlalchemy import create_engine, Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine("sqlite:///agency.db", connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

event_artist = Table('event_artist', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('artist_id', Integer, ForeignKey('artists.id'))
)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    title = Column(String)
    location = Column(String)
    status = Column(String, default="bozza")

class Artist(Base):
    __tablename__ = "artists"
    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(engine)
