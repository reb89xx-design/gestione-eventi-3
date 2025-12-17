# components/calendar_advanced.py
import streamlit as st
import calendar
from datetime import date, datetime
from collections import defaultdict
from utils import list_events_by_date, list_events_range, save_event
from components.event_card import render_event_card

STATE_COLORS = {
    "bozza": "#f0ad4e",
    "confermato": "#5cb85c",
    "cancellato": "#d9534f"
}

def _group_events_by_date(events):
    grouped = defaultdict(list)
    for e in events:
        if e.date:
            grouped[e.date].append(e)
    return grouped

def render_month(year: int, month: int, filters: dict = None):
    """
    Disegna il calendario mensile. Cliccando su un giorno si apre il pannello con gli eventi.
    filters: dict con chiavi opzionali 'type' e 'status'
    """
    if filters is None:
        filters = {}
    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdayscalendar(year, month)
    header = ["Lun","Mar","Mer","Gio","Ven","Sab","Dom"]
    st.markdown("### Calendario Mensile")
    cols = st.columns(7)
    for i, h in enumerate(header):
        cols[i].markdown(f"**{h}**")
    # prefetch events for month range
    _, last_day = calendar.monthrange(year, month)
    start = date(year, month, 1)
    end = date(year, month, last_day)
    events = list_events_range(start, end)
    events_by_date = _group_events_by_date(events)
    for week in weeks:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")
            else:
                d = date(year, month, day)
                evs = events_by_date.get(d, [])
                # applica filtri
                if filters.get("type") and filters["type"] != "tutti":
                    evs = [e for e in evs if e.type == filters["type"]]
                if filters.get("status") and filters["status"] != "tutti":
                    evs = [e for e in evs if e.status == filters["status"]]
                if evs:
                    first = evs[0]
                    color = STATE_COLORS.get(first.status, "#777")
                    label = f"{day}  • {len(evs)}"
                    if cols[i].button(label, key=f"cal_{year}_{month}_{day}"):
                        st.session_state["_cal_selected_day"] = d.isoformat()
                        st.session_state["_cal_open_day"] = True
                else:
                    if cols[i].button(str(day), key=f"cal_empty_{year}_{month}_{day}"):
                        st.session_state["_cal_selected_day"] = d.isoformat()
                        st.session_state["_cal_open_day"] = True

def show_day_panel(selected_date: date):
    st.markdown(f"## Eventi del giorno {selected_date.isoformat()}")
    events = list_events_by_date(selected_date)
    if not events:
        st.info("Nessun evento per questa data")
    else:
        for ev in events:
            with st.container():
                render_event_card(ev, compact=True)

    st.markdown("---")
    st.markdown("### Crea nuovo evento rapido")
    with st.form(f"quick_create_{selected_date.isoformat()}", clear_on_submit=True):
        title = st.text_input("Titolo")
        location = st.text_input("Luogo")
        typ = st.selectbox("Tipo", options=["format","artist"], index=0)
        promoter = st.text_input("Promoter (nome)")
        submit = st.form_submit_button("Crea evento")
        if submit:
            payload = {
                "title": title or f"Evento {selected_date.isoformat()}",
                "date": selected_date,
                "location": location,
                "type": typ,
                "status": "bozza",
                "notes": f"Creato rapidamente da calendario. Promoter: {promoter}" if promoter else ""
            }
            try:
                ev = save_event(payload)
                st.success("Evento creato")
                # apri la scheda evento completa
                st.session_state["open_event_id"] = ev.id
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Errore creazione evento: {e}")
