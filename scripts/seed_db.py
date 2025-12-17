# scripts/seed_db.py
from db import get_session, init_db
from models import Artist, Service, Format, Promoter, TourManager, Event
from datetime import date

# Crea tabelle se non esistono
init_db()

db = get_session()
try:
    # Esempi artisti
    a1 = Artist(name="DJ Test", role="dj", phone="333111222", email="dj@test.com")
    a2 = Artist(name="Vocal Test", role="vocalist", phone="333111333", email="vocal@test.com")
    a3 = Artist(name="Ballerina Uno", role="ballerina", phone="333222444", email="b1@test.com")
    a4 = Artist(name="Mascotte X", role="mascotte", phone="333333444", email="m1@test.com")

    # Service, format, promoter, tour manager
    s1 = Service(name="Service A", contact="Marco", phone="333444555")
    f1 = Format(name="Format Demo", description="Demo format per test")
    p1 = Promoter(name="Promoter X", phone="333666777", email="promoter@test.com")
    t1 = TourManager(name="TM Y", phone="333888999", email="tm@test.com")

    db.add_all([a1, a2, a3, a4, s1, f1, p1, t1])
    db.commit()

    # Evento demo (format)
    ev = Event(
        date=date.today(),
        title="Demo Format Show",
        location="Teatro Test",
        type="format",
        format_id=f1.id,
        promoter_id=p1.id,
        tour_manager_id=t1.id,
        status="bozza",
        van="Van 1",
        travel="Bus",
        hotel="Hotel Test",
        payments_acconto=500.0,
        payments_saldo=1500.0,
        allestimenti="Palco, luci"
    )
    ev.artists.append(a1)   # DJ
    ev.services.append(s1)
    db.add(ev)
    db.commit()

    # Evento demo (artist)
    ev2 = Event(
        date=date.today(),
        title="Concerto Test Artista",
        location="Club Test",
        type="artist",
        promoter_id=p1.id,
        tour_manager_id=t1.id,
        status="bozza",
        van="Van 2",
        travel="Auto",
        hotel="Hotel Test 2",
        facchini="2",
        payments_acconto=200.0,
        payments_saldo=800.0
    )
    ev2.artists.append(a2)
    ev2.services.append(s1)
    db.add(ev2)
    db.commit()

    print("Seed completato: artisti, service, format, promoter, tour manager, eventi demo")
finally:
    db.close()
