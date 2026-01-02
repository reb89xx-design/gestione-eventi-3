# pages/xx_create_event.py
import streamlit as st
from datetime import datetime, date, time
from utils import list_artists, list_services, list_promoters, list_tour_managers, save_event

st.set_page_config(page_title="Crea Evento", layout="wide")
st.title("Crea nuovo evento")

with st.form("create_event", clear_on_submit=False):
    c1, c2 = st.columns([2,1])
    with c1:
        title = st.text_input("Titolo", key="ev_title")
        ev_date = st.date_input("Data", value=date.today(), key="ev_date")
        ev_time = st.time_input("Ora", value=time(21,0), key="ev_time")
        duration = st.number_input("Durata (ore)", min_value=1, max_value=24, value=3, key="ev_duration")
        location = st.text_input("Luogo", key="ev_location")
        ev_type = st.selectbox("Tipo", ["artist","format"], key="ev_type")
    with c2:
        artists = list_artists()
        artist_map = {a.id: a.name for a in artists}
        selected_artists = st.multiselect("Artisti", options=list(artist_map.keys()), format_func=lambda x: artist_map[x], key="ev_artists")
        services = list_services()
        service_map = {s.id: s.name for s in services}
        selected_services = st.multiselect("Services", options=list(service_map.keys()), format_func=lambda x: service_map[x], key="ev_services")
        promoter = st.selectbox("Promoter", options=[None] + [p.id for p in list_promoters()], format_func=lambda x: "-" if x is None else next((p.name for p in list_promoters() if p.id==x), str(x)), key="ev_promoter")
        tm = st.selectbox("Tour Manager", options=[None] + [t.id for t in list_tour_managers()], format_func=lambda x: "-" if x is None else next((t.name for t in list_tour_managers() if t.id==x), str(x)), key="ev_tm")
        status = st.selectbox("Stato", ["bozza","confermato","cancellato"], index=0, key="ev_status")
    st.markdown("**Preview evento**")
    st.write(f"**{title}** — {ev_date} {ev_time} — {location} — {ev_type}")
    submitted = st.form_submit_button("Crea evento")
    if submitted:
        if not title.strip():
            st.error("Titolo obbligatorio")
        else:
            payload = {
                "title": title.strip(),
                "date": datetime.combine(ev_date, ev_time),
                "duration_hours": duration,
                "location": location.strip(),
                "type": ev_type,
                "artist_ids": selected_artists,
                "service_ids": selected_services,
                "promoter_id": promoter,
                "tour_manager_id": tm,
                "status": status,
                "notes": ""
            }
            try:
                ev = save_event(payload, user=st.session_state.get("user",""))
                st.success(f"Evento creato: {ev.title} ({ev.date})")
                st.session_state["open_event_id"] = ev.id
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Errore salvataggio: {e}")
