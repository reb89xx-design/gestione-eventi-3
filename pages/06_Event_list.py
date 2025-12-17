# pages/06_Event_list.py
import streamlit as st
from datetime import date
import csv
import io

from utils import (
    list_events_range, export_data_json, list_artists, list_services,
    events_without_dj, events_without_promoter, save_event, duplicate_event
)

st.set_page_config(page_title="Event List", layout="wide")
st.title("Lista Eventi e gestione")

# --- Filtri e azioni globali
col_filters, col_actions = st.columns([3,1])

with col_filters:
    start = st.date_input("Da", value=date.today(), key="events_list_start")
    end = st.date_input("A", value=date.today(), key="events_list_end")
    if start > end:
        st.error("La data 'Da' non può essere successiva alla data 'A'")
    status = st.selectbox("Stato", options=["tutti","bozza","confermato","cancellato"], index=0, key="events_list_status")
    q_artist = st.selectbox("Mostra eventi senza DJ / senza promoter", options=["tutti","senza_dj","senza_promoter"], index=0, key="events_list_qartist")

with col_actions:
    if st.button("Esporta JSON", key="export_json_btn"):
        path = "data/export_events.json"
        try:
            export_data_json(path)
            st.success(f"Export salvato in {path}")
        except Exception as e:
            st.error(f"Errore export: {e}")

    if st.button("Esporta CSV (eventi)", key="export_csv_btn"):
        evs = list_events_range(start, end)
        if status != "tutti":
            evs = [e for e in evs if e.status == status]
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id","date","title","location","type","status","promoter_id","tour_manager_id"])
        for e in evs:
            writer.writerow([e.id, e.date.isoformat() if e.date else "", e.title, e.location, e.type, e.status, e.promoter_id, e.tour_manager_id])
        st.download_button("Download CSV", data=output.getvalue(), file_name="events.csv", mime="text/csv", key="download_csv_events")

st.markdown("---")

# --- Sezione: aggiungi nuovo evento (form)
st.markdown("## Aggiungi nuovo evento")
with st.form("add_event_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2,2,1])
    with c1:
        new_title = st.text_input("Titolo", key="new_event_title")
        new_date = st.date_input("Data", value=date.today(), key="new_event_date")
        new_location = st.text_input("Luogo", key="new_event_location")
    with c2:
        new_type = st.selectbox("Tipo", options=["artist","format"], index=0, key="new_event_type")
        artists = list_artists()
        artist_map = {a.id: a.name for a in artists}
        new_artist_ids = st.multiselect("Artisti", options=list(artist_map.keys()), format_func=lambda x: artist_map[x], key="new_event_artists")
        services = list_services()
        service_map = {s.id: s.name for s in services}
        new_service_ids = st.multiselect("Services", options=list(service_map.keys()), format_func=lambda x: service_map[x], key="new_event_services")
    with c3:
        promoter_opts = ["Nessuno"]
        try:
            from utils import list_promoters
            promoter_list = list_promoters()
            promoter_map = {p.id: p.name for p in promoter_list}
            promoter_opts = [None] + list(promoter_map.keys())
        except Exception:
            promoter_map = {}
            promoter_opts = [None]
        promoter_choice = st.selectbox("Promoter", options=promoter_opts, format_func=lambda x: promoter_map.get(x, "-"), index=0, key="new_event_promoter")
        tm_opts = ["Nessuno"]
        try:
            from utils import list_tour_managers
            tm_list = list_tour_managers()
            tm_map = {t.id: t.name for t in tm_list}
            tm_opts = [None] + list(tm_map.keys())
        except Exception:
            tm_map = {}
            tm_opts = [None]
        tm_choice = st.selectbox("Tour Manager", options=tm_opts, format_func=lambda x: tm_map.get(x, "-"), index=0, key="new_event_tm")
        status_choice = st.selectbox("Stato", options=["bozza","confermato","cancellato"], index=0, key="new_event_status")

    submitted = st.form_submit_button("Crea evento")
    if submitted:
        if not new_title.strip():
            st.error("Inserisci il titolo dell'evento")
        else:
            payload = {
                "title": new_title.strip(),
                "date": new_date,
                "location": new_location.strip(),
                "type": new_type,
                "artist_ids": new_artist_ids,
                "service_ids": new_service_ids,
                "promoter_id": promoter_choice,
                "tour_manager_id": tm_choice,
                "status": status_choice,
                "notes": f"Creato manualmente da interfaccia"
            }
            try:
                ev = save_event(payload, user=st.session_state.get("user",""))
                if ev:
                    st.success(f"Evento creato: {ev.title} ({ev.date})")
                    st.session_state["open_event_id"] = ev.id
                    st.experimental_rerun()
                else:
                    st.error("Errore creazione evento")
            except Exception as e:
                st.error(f"Errore creazione evento: {e}")

st.markdown("---")

# --- Mostra lista eventi filtrata
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
            try:
                duplicate_event(e.id, user=st.session_state.get("user",""))
                st.success("Evento duplicato")
                st.experimental_rerun()
            except Exception as ex:
                st.error(f"Errore duplicazione: {ex}")
    with cols[3]:
        if st.button("Task", key=f"task_list_{e.id}"):
            st.session_state["open_event_id"] = e.id
            st.session_state["open_task_for_event"] = True
            st.experimental_rerun()

# --- Segnalazioni rapide (controlli senza DJ / senza promoter)
st.markdown("---")
st.markdown("### Segnalazioni rapide")
col1, col2 = st.columns(2)

with col1:
    sd = st.date_input("Controlla eventi senza DJ da", value=date.today(), key="no_dj_from")
    ed = st.date_input("a (senza DJ)", value=date.today(), key="no_dj_to")
    if st.button("Mostra eventi senza DJ", key="btn_show_no_dj"):
        try:
            res = events_without_dj(sd, ed)
            st.write(f"Trovati: {len(res)}")
            for r in res:
                st.write(f"{r.date} — {r.title} — {r.location}")
        except Exception as ex:
            st.error(f"Errore: {ex}")

with col2:
    sd2 = st.date_input("Controlla eventi senza promoter da", value=date.today(), key="no_prom_from")
    ed2 = st.date_input("a (senza promoter)", value=date.today(), key="no_prom_to")
    if st.button("Mostra eventi senza promoter", key="btn_show_no_prom"):
        try:
            res2 = events_without_promoter(sd2, ed2)
            st.write(f"Trovati: {len(res2)}")
            for r in res2:
                st.write(f"{r.date} — {r.title} — {r.location}")
        except Exception as ex:
            st.error(f"Errore: {ex}")
