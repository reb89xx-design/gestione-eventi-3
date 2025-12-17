# scripts/seed_full_example.py
from db import get_session, init_db, get_db_file_path
from models import Artist, Service, Format, Promoter, TourManager, Event, Task
from datetime import date, timedelta
import json
import os

# Inizializza DB (crea tabelle se necessario)
init_db()
db = get_session()

try:
    # Pulizia opzionale: evita duplicati per esecuzioni ripetute
    # (commenta se non vuoi cancellare)
    db.query(Task).delete()
    db.query(Event).delete()
    db.query(Artist).delete()
    db.query(Service).delete()
    db.query(Format).delete()
    db.query(Promoter).delete()
    db.query(TourManager).delete()
    db.commit()

    # Team members (creati anche come file users.json)
    team = ["ale", "marta", "luca", "giulia", "andrea"]

    # Artisti di esempio
    a_dj = Artist(name="DJ Example", role="dj", phone="333111000", email="dj@example.com")
    a_vocal = Artist(name="Vocal Example", role="vocalist", phone="333111001", email="vocal@example.com")
    a_ball1 = Artist(name="Ballerina One", role="ballerina", phone="333111002", email="b1@example.com")
    a_ball2 = Artist(name="Ballerina Two", role="ballerina", phone="333111003", email="b2@example.com")
    a_masc = Artist(name="Mascotte Fun", role="mascotte", phone="333111004", email="masc@example.com")
    a_head = Artist(name="Headliner Star", role="artist", phone="333111005", email="head@example.com")

    # Service, format, promoter, tour manager
    s1 = Service(name="Service Alpha", contact="Marco", phone="333444555", notes="Service demo")
    f1 = Format(name="Format Party", description="Format demo con DJ e ballerine", notes="Demo format")
    p1 = Promoter(name="Promoter Demo", contact="Luca", phone="333666777", email="promoter@example.com")
    t1 = TourManager(name="TM Demo", contact="Giulia", phone="333888999", email="tm@example.com")

    db.add_all([a_dj, a_vocal, a_ball1, a_ball2, a_masc, a_head, s1, f1, p1, t1])
    db.commit()

    # Evento format di esempio
    ev_format = Event(
        date=date.today() + timedelta(days=3),
        title="Format Demo Night",
        location="Teatro Centrale",
        type="format",
        format_id=f1.id,
        promoter_id=p1.id,
        tour_manager_id=t1.id,
        status="bozza",
        van="Van A",
        travel="Pullman",
        hotel="Hotel Demo",
        allestimenti="Palco 8x6, luci base",
        payments_acconto=300.0,
        payments_saldo=1200.0,
        dj_id=a_dj.id,
        vocalist_id=a_vocal.id,
        ballerine_ids="{},{}".format(a_ball1.id, a_ball2.id),
        mascotte_ids=str(a_masc.id)
    )
    ev_format.artists.append(a_dj)
    ev_format.services.append(s1)
    db.add(ev_format)
    db.commit()

    # Evento artista di esempio
    ev_artist = Event(
        date=date.today() + timedelta(days=7),
        title="Concerto Headliner",
        location="Club Underground",
        type="artist",
        promoter_id=p1.id,
        tour_manager_id=t1.id,
        status="bozza",
        van="Van B",
        travel="Auto",
        hotel="Hotel Rock",
        facchini="3",
        payments_acconto=200.0,
        payments_saldo=800.0
    )
    ev_artist.artists.append(a_head)
    ev_artist.services.append(s1)
    db.add(ev_artist)
    db.commit()

    # Task di esempio per evento format
    t1 = Task(event_id=ev_format.id, title="Confermare DJ", description="Contattare DJ Example per conferma set e rider", assignee="ale", due_date=date.today() + timedelta(days=2))
    t2 = Task(event_id=ev_format.id, title="Verificare hotel", description="Controllare prenotazioni e camere", assignee="marta", due_date=date.today() + timedelta(days=2))
    db.add_all([t1, t2])
    db.commit()

    # Task di esempio per evento artista
    t3 = Task(event_id=ev_artist.id, title="Inviare rider", description="Inviare rider tecnico all'organizzatore", assignee="luca", due_date=date.today() + timedelta(days=5))
    db.add(t3)
    db.commit()

    # Scrivi users.json in data
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    users_path = os.path.join(data_dir, "users.json")
    users_content = {u: {"email": f"{u}@example.com", "name": u.capitalize()} for u in team}
    with open(users_path, "w", encoding="utf-8") as f:
        json.dump(users_content, f, ensure_ascii=False, indent=2)

    # Esporta un sample JSON di backup
    sample_path = os.path.join(data_dir, "sample_export.json")
    export = {"events": [], "tasks": [], "artists": []}
    for e in db.query(Event).all():
        export["events"].append({"id": e.id, "title": e.title, "date": e.date.isoformat(), "type": e.type})
    for tk in db.query(Task).all():
        export["tasks"].append({"id": tk.id, "event_id": tk.event_id, "title": tk.title, "assignee": tk.assignee})
    for ar in db.query(Artist).all():
        export["artists"].append({"id": ar.id, "name": ar.name, "role": ar.role})
    with open(sample_path, "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=2)

    print("Seed completo creato nel DB:", get_db_file_path())
    print("Users saved to", users_path)
    print("Sample export saved to", sample_path)

finally:
    db.close()
