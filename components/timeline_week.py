# components/timeline_week.py
import streamlit as st
from datetime import date, timedelta
from utils import list_events_range, move_event_date, save_event
from components.event_card import render_event_card

def _week_range(center_date: date):
    # restituisce lun-dom della settimana contenente center_date (Lun=0)
    start = center_date - timedelta(days=(center_date.weekday()))
    return [start + timedelta(days=i) for i in range(7)]

def render_week(center_date: date = None):
    if center_date is None:
        center_date = date.today()
    days = _week_range(center_date)
    st.markdown(f"### Timeline settimanale ({days[0].isoformat()} — {days[-1].isoformat()})")
    cols = st.columns(7)
    # prefetch events per range
    evs = list_events_range(days[0], days[-1])
    events_by_day = {d: [e for e in evs if e.date == d] for d in days}
    for i, d in enumerate(days):
        with cols[i]:
            st.markdown(f"**{d.strftime('%a %d %b')}**")
            day_events = events_by_day.get(d, [])
            if not day_events:
                st.write("—")
            for ev in day_events:
                with st.container():
                    render_event_card(ev, compact=True)
                    # quick move controls
                    move_cols = st.columns([1,1,1])
                    with move_cols[0]:
                        if st.button("◀", key=f"move_prev_{ev.id}"):
                            new_date = ev.date - timedelta(days=1)
                            move_event_date(ev.id, new_date)
                            st.experimental_rerun()
                    with move_cols[1]:
                        if st.button("↺", key=f"move_today_{ev.id}"):
                            move_event_date(ev.id, date.today())
                            st.experimental_rerun()
                    with move_cols[2]:
                        if st.button("▶", key=f"move_next_{ev.id}"):
                            new_date = ev.date + timedelta(days=1)
                            move_event_date(ev.id, new_date)
                            st.experimental_rerun()

def render_week_with_controls():
    st.sidebar.markdown("### Controlli Timeline")
    center = st.sidebar.date_input("Settimana centrata su", value=date.today())
    st.sidebar.markdown("Usa le frecce nelle card per spostare gli eventi di un giorno")
    render_week(center)
