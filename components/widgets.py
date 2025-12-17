import streamlit as st
from datetime import date
import calendar
import pandas as pd

def month_grid(year, month, events_by_date):
    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdayscalendar(year, month)
    cols = st.columns(7)
    header = ["Lun","Mar","Mer","Gio","Ven","Sab","Dom"]
    with st.container():
        st.markdown("**Calendario Mensile**")
        # header
        cols = st.columns(7)
        for i, h in enumerate(header):
            cols[i].markdown(f"**{h}**")
        # grid
        for week in weeks:
            cols = st.columns(7)
            for i, day in enumerate(week):
                if day == 0:
                    cols[i].write("")
                else:
                    d = date(year, month, day)
                    ev_count = len(events_by_date.get(d, []))
                    if ev_count:
                        cols[i].button(f"{day}  • {ev_count}", key=f"day_{year}_{month}_{day}")
                    else:
                        cols[i].write(day)
