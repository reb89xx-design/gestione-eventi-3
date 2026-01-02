# pages/02_Calendar.py
import streamlit as st
from datetime import date
from components.calendar_advanced import render_month, show_day_panel
from components.event_card import render_event_card
from utils import list_events_range, upcoming_events
from utils import list_events_range, list_artists
import calendar
st.title("Calendario")
artists = list_artists()
artist_map = {0: "Tutti", **{a.id: a.name for a in artists}}
artist_choice = st.selectbox("Filtra per artista", options=list(artist_map.keys()), format_func=lambda x: artist_map[x], index=0, key="cal_artist")

start = st.date_input("Da", value=date.today().replace(day=1), key="cal_start")
end = st.date_input("A", value=date.today(), key="cal_end")
view = st.radio("Vista", ["Mensile","Lista"], index=0, key="cal_view")

events = list_events_range(start, end)
if artist_choice != 0:
    events = [e for e in events if artist_choice in getattr(e, "artist_ids", [])]

if view == "Lista":
    st.dataframe([{"date": e.date, "title": e.title, "artists": ", ".join([str(a) for a in getattr(e,"artist_ids",[])])} for e in events])
else:
    # semplice raggruppamento per giorno
    days = {}
    for e in events:
        days.setdefault(str(e.date), []).append(e)
    for day in sorted(days.keys()):
        with st.expander(day):
            for e in days[day]:
                st.markdown(f"**{e.title}** — {e.location} — {e.status}")
st.set_page_config(page_title="Calendario", layout="wide")
st.title("Calendario eventi")

today = date.today()
col_left, col_main = st.columns([1,3])

with col_left:
    year = st.number_input("Anno", min_value=2000, max_value=2100, value=today.year, step=1)
    month = st.selectbox("Mese", list(range(1,13)), index=today.month-1)
    tipo = st.selectbox("Tipo", options=["tutti","format","artist"], index=0)
    stato = st.selectbox("Stato", options=["tutti","bozza","confermato","cancellato"], index=0)
    quick_view = st.checkbox("Mostra eventi prossimi 7 giorni", value=False)

with col_main:
    filters = {"type": tipo, "status": stato}
    render_month(year, month, filters=filters)

    # apertura giorno selezionato
    if st.session_state.get("_cal_open_day"):
        sel = st.session_state.get("_cal_selected_day")
        if sel:
            from datetime import datetime
            d = datetime.fromisoformat(sel).date()
            show_day_panel(d)
        st.session_state["_cal_open_day"] = False

    # quick view eventi prossimi 7 giorni
    if quick_view:
        st.markdown("### Prossimi 7 giorni")
        evs = upcoming_events(7)
        if not evs:
            st.info("Nessun evento nei prossimi 7 giorni")
        else:
            for e in evs:
                render_event_card(e, compact=True)
