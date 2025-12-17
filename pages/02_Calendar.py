# pages/02_Calendar.py
import streamlit as st
from datetime import date
from components.calendar import month_grid, show_day_modal
from utils import list_events_by_date, list_events_range, duplicate_event
import calendar

st.set_page_config(page_title="Calendario", layout="wide")
st.header("Calendario globale")

today = date.today()
col1, col2 = st.columns([1,3])
with col1:
    year = st.number_input("Anno", min_value=2000, max_value=2100, value=today.year, step=1)
    month = st.selectbox("Mese", list(range(1,13)), index=today.month-1)
    # filtri
    tipo = st.selectbox("Tipo", options=["tutti","format","artist"], index=0)
    stato = st.selectbox("Stato", options=["tutti","bozza","confermato","cancellato"], index=0)

with col2:
    # prepara mapping date -> eventi
    _, last_day = calendar.monthrange(year, month)
    events_by_date = {}
    for d in range(1, last_day+1):
        dt = date(year, month, d)
        evs = list_events_by_date(dt)
        # applica filtri semplici
        if tipo != "tutti":
            evs = [e for e in evs if e.type == tipo]
        if stato != "tutti":
            evs = [e for e in evs if e.status == stato]
        if evs:
            events_by_date[dt] = evs

    month_grid(year, month, events_by_date)

# gestione apertura giorno
if st.session_state.get("_cal_open_day"):
    sel = st.session_state.get("_cal_selected_day")
    if sel:
        from datetime import datetime
        d = datetime.fromisoformat(sel).date()
        events = list_events_by_date(d)
        show_day_modal(d, events)
    # reset apertura
    st.session_state["_cal_open_day"] = False

# duplicazione evento quick action
if st.session_state.get("_dup_event_id"):
    try:
        new_ev = duplicate_event(st.session_state["_dup_event_id"])
        st.success(f"Evento duplicato: ID {new_ev.id}")
    finally:
        del st.session_state["_dup_event_id"]
