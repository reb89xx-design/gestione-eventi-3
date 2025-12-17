# components/calendar.py
import streamlit as st
import calendar
from datetime import date, datetime
from utils import list_events_by_date

STATE_COLORS = {
    "bozza": "#f0ad4e",
    "confermato": "#5cb85c",
    "cancellato": "#d9534f"
}

def month_grid(year, month, events_by_date, key_prefix="cal"):
    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdayscalendar(year, month)
    header = ["Lun","Mar","Mer","Gio","Ven","Sab","Dom"]
    st.markdown("### Calendario Mensile")
    cols = st.columns(7)
    for i, h in enumerate(header):
        cols[i].markdown(f"**{h}**")
    for week in weeks:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")
            else:
                d = date(year, month, day)
                evs = events_by_date.get(d, [])
                if evs:
                    # mostra primo evento e count
                    first = evs[0]
                    color = STATE_COLORS.get(first.status, "#777")
                    label = f"{day}  • {len(evs)}"
                    if cols[i].button(label, key=f"{key_prefix}_{year}_{month}_{day}"):
                        st.session_state["_cal_selected_day"] = d.isoformat()
                        st.session_state["_cal_open_day"] = True
                else:
                    cols[i].write(day)

def show_day_modal(selected_date, events):
    st.markdown(f"### Eventi del giorno {selected_date}")
    if not events:
        st.info("Nessun evento per questa data")
    else:
        for ev in events:
            cols = st.columns([4,1,1])
            with cols[0]:
                st.markdown(f"**{ev.title}** — {ev.location}")
                st.write(f"Stato: **{ev.status}**  •  Tipo: **{ev.type}**")
            with cols[1]:
                if st.button("Apri", key=f"open_ev_{ev.id}"):
                    st.session_state["open_event_id"] = ev.id
                    st.experimental_rerun()
            with cols[2]:
                if st.button("Duplica", key=f"dup_ev_{ev.id}"):
                    st.session_state["_dup_event_id"] = ev.id
                    st.experimental_rerun()
