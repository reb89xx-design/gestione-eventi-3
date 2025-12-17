# pages/04_Event_Detail.py
import streamlit as st
from datetime import date
from utils import (
    get_event, save_event,
    list_artists, list_artists_by_role,
    list_formats, list_services, list_promoters, list_tour_managers
)

st.set_page_config(page_title="Scheda Evento", layout="wide")
st.header("Creazione / Modifica Evento")

# Se aperto da calendario, session_state contiene open_event_id
event_id = st.session_state.get("open_event_id", None)
ev = get_event(event_id) if event_id else None

# Tipo evento: format o artist
default_type = ev.type if ev else "format"
event_type = st.radio("Tipo evento", options=["format", "artist"], index=0 if default_type=="format" else 1, horizontal=True)

with st.form("event_form", clear_on_submit=False):
    col1, col2 = st.columns([2,1])

    with col1:
        title = st.text_input("Titolo evento", value=ev.title if ev else "")
        ev_date = st.date_input("Data", value=ev.date if ev else date.today())
        location = st.text_input("Luogo", value=ev.location if ev else "")
        services = list_services()
        service_options = {s.id: s.name for s in services}
        selected_services = st.multiselect("Service (seleziona uno o più)", options=list(service_options.keys()), format_func=lambda x: service_options[x], default=[s.id for s in ev.services] if ev and ev.services else [])

        # pagamenti
        st.markdown("**Pagamenti**")
        acconto = st.number_input("Acconto (€)", value=float(ev.payments_acconto) if ev and ev.payments_acconto is not None else 0.0, step=10.0, format="%.2f")
        saldo = st.number_input("Saldo (€)", value=float(ev.payments_saldo) if ev and ev.payments_saldo is not None else 0.0, step=10.0, format="%.2f")

        notes = st.text_area("Note evento", value=ev.notes if ev else "", height=140)

    with col2:
        st.markdown("**Dettagli logistici**")
        van = st.text_input("Van", value=ev.van if ev else "")
        travel = st.text_input("Viaggi", value=ev.travel if ev else "")
        hotel = st.text_input("Hotel", value=ev.hotel if ev else "")
        allestimenti = st.text_area("Allestimenti", value=ev.allestimenti if ev else "", height=80)

        st.markdown("**Selezioni rapide**")
        # common dropdowns
        formats = list_formats()
        format_map = {f.id: f.name for f in formats}
        format_default = ev.format_id if ev and ev.format_id else None
        format_choice = st.selectbox("Format (opzionale)", options=[None] + list(format_map.keys()), format_func=lambda x: format_map.get(x, "-"), index=0 if not format_default else list(format_map.keys()).index(format_default)+1)

        promoters = list_promoters()
        promoter_map = {p.id: p.name for p in promoters}
        promoter_choice = st.selectbox("Promoter", options=[None] + list(promoter_map.keys()), format_func=lambda x: promoter_map.get(x, "-"), index=0)

        tms = list_tour_managers()
        tm_map = {t.id: t.name for t in tms}
        tm_choice = st.selectbox("Tour Manager", options=[None] + list(tm_map.keys()), format_func=lambda x: tm_map.get(x, "-"), index=0)

    st.markdown("---")

    # Campi diversi per FORMAT vs ARTIST
    if event_type == "format":
        st.subheader("Campi specifici per FORMAT")
        # DJ (single)
        djs = list_artists_by_role("dj")
        dj_map = {d.id: d.name for d in djs}
        dj_choice = st.selectbox("DJ", options=[None] + list(dj_map.keys()), format_func=lambda x: dj_map.get(x, "-"), index=0)

        # Vocalist
        vocals = list_artists_by_role("vocalist")
        vocal_map = {v.id: v.name for v in vocals}
        vocalist_choice = st.selectbox("Vocalist", options=[None] + list(vocal_map.keys()), format_func=lambda x: vocal_map.get(x, "-"), index=0)

        # Ballerine (single or multiple depending on your model; here allow multiple)
        ballerine = list_artists_by_role("ballerina")
        ballerine_map = {b.id: b.name for b in ballerine}
        ballerine_choice = st.multiselect("Ballerine", options=list(ballerine_map.keys()), format_func=lambda x: ballerine_map[x], default=[])

        # Mascotte (multi)
        mascotte = list_artists_by_role("mascotte")
        mascotte_map = {m.id: m.name for m in mascotte}
        mascotte_choice = st.multiselect("Mascotte (più selezioni)", options=list(mascotte_map.keys()), format_func=lambda x: mascotte_map[x], default=[])

    else:
        st.subheader("Campi specifici per ARTISTA")
        facchini = st.text_input("Facchini", value=ev.facchini if ev else "")
        # per artista puoi associare singoli artisti (es. headliner)
        artists = list_artists()
        artist_map = {a.id: f"{a.name} ({a.role})" for a in artists}
        artist_choice = st.selectbox("Artista principale", options=[None] + list(artist_map.keys()), format_func=lambda x: artist_map.get(x, "-"), index=0)

    # Stato e azioni
    st.markdown("---")
    status = st.selectbox("Stato evento", options=["bozza", "confermato", "cancellato"], index=0 if not ev else ["bozza","confermato","cancellato"].index(ev.status if ev.status in ["bozza","confermato","cancellato"] else "bozza"))

    submitted = st.form_submit_button("Salva evento")

    if submitted:
        payload = {
            "id": ev.id if ev else None,
            "title": title,
            "date": ev_date,
            "location": location,
            "type": event_type,
            "format_id": format_choice,
            "promoter_id": promoter_choice,
            "tour_manager_id": tm_choice,
            "status": status,
            "notes": notes,
            "van": van,
            "travel": travel,
            "hotel": hotel,
            "allestimenti": allestimenti,
            "payments_acconto": acconto,
            "payments_saldo": saldo,
            "service_ids": selected_services
        }

        if event_type == "format":
            payload.update({
                "dj_id": dj_choice,
                "vocalist_id": vocalist_choice,
                "ballerine_ids": ballerine_choice,
                "mascotte_ids": mascotte_choice
            })
        else:
            payload.update({
                "facchini": facchini,
                "artist_ids": [artist_choice] if artist_choice else []
            })

        new_ev = save_event(payload)
        if new_ev:
            st.success("Evento salvato con successo")
            # pulizia stato e redirect
            if "open_event_id" in st.session_state:
                st.session_state.pop("open_event_id")
            st.experimental_rerun()
        else:
            st.error("Errore nel salvataggio evento")
