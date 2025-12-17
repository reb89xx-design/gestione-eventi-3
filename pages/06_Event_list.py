# pages/06_Events_List.py
import streamlit as st
from datetime import date
from utils import list_events_range, export_data_json, list_artists, events_without_dj, events_without_promoter
import csv
import io

st.set_page_config(page_title="Lista Eventi", layout="wide")
st.title("Lista eventi e gestione")

col_filters, col_actions = st.columns([3,1])

with col_filters:
    start = st.date_input("Da", value=date.today())
    end = st.date_input("A", value=date.today())
    if start > end:
        st.error("La data 'Da' non può essere successiva alla data 'A'")
    status = st.selectbox("Stato", options=["tutti","bozza","confermato","cancellato"], index=0)
    q_artist = st.selectbox("Mostra eventi senza DJ / senza promoter", options=["tutti","senza_dj","senza_promoter"], index=0)

with col_actions:
    if st.button("Esporta JSON"):
        path = "data/export_events.json"
        try:
            export_data_json(path)
            st.success(f"Export salvato in {path}")
        except Exception as e:
            st.error(f"Errore export: {e}")
    if st.button("Esporta CSV (eventi)"):
        evs = list_events_range(start, end)
        # applica filtri
        if status != "tutti":
            evs = [e for e in evs if e.status == status]
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id","date","title","location","type","status","promoter_id","tour_manager_id"])
        for e in evs:
            writer.writerow([e.id, e.date.isoformat() if e.date else "", e.title, e.location, e.type, e.status, e.promoter_id, e.tour_manager_id])
        st.download_button("Download CSV", data=output.getvalue(), file_name="events.csv", mime="text/csv")

# mostra lista
events = list_events_range(start, end)
if status != "tutti":
    events = [e for e in events if e.status == status]
if q_artist == "senza_dj":
    events = [e for e in events if not e.dj_id]
if q_artist == "senza_promoter":
    events = [e for e in events if not e.promoter_id]

st.markdown(f"### Eventi trovati: {len(events)}")
for e in events:
    cols = st.columns([4,1,1,1])
    with cols[0]:
        st.markdown(f"**{e.title}** — {e.date} — {e.location}")
        st.write(f"Tipo: {e.type}  •  Stato: {e.status}")
    with cols[1]:
        if st.button("Apri", key=f"open_list_{e.id}"):
            st.session_state["open_event_id"] = e.id
            st.experimental_rerun()
    with cols[2]:
        if st.button("Duplica", key=f"dup_list_{e.id}"):
            from utils import duplicate_event
            duplicate_event(e.id)
            st.success("Evento duplicato")
            st.experimental_rerun()
    with cols[3]:
        if st.button("Task", key=f"task_list_{e.id}"):
            st.session_state["open_event_id"] = e.id
            st.session_state["open_task_for_event"] = True
            st.experimental_rerun()

# segnalazioni rapide
st.markdown("---")
st.markdown("### Segnalazioni rapide")
col1, col2 = st.columns(2)
with col1:
    sd = st.date_input("Controlla eventi senza DJ da", value=date.today())
    ed = st.date_input("a", value=date.today())
    if st.button("Mostra eventi senza DJ"):
        res = events_without_dj(sd, ed)
        st.write(f"Trovati: {len(res)}")
        for r in res:
            st.write(f"{r.date} — {r.title} — {r.location}")
with col2:
    sd2 = st.date_input("Controlla eventi senza promoter da", value=date.today())
    ed2 = st.date_input("a", value=date.today())
    if st.button("Mostra eventi senza promoter"):
        res2 = events_without_promoter(sd2, ed2)
        st.write(f"Trovati: {len(res2)}")
        for r in res2:
            st.write(f"{r.date} — {r.title} — {r.location}")
