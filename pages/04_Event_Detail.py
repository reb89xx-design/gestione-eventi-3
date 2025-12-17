# pages/04_Event_Detail.py
import streamlit as st
from datetime import date
from utils import (
    get_event, save_event, delete_event,
    list_artists, list_artists_by_role,
    list_formats, list_services, list_promoters, list_tour_managers
)

st.set_page_config(page_title="Scheda Evento", layout="wide")
st.header("Creazione / Modifica Evento")

# Carica evento aperto (se presente nello stato)
event_id = st.session_state.get("open_event_id", None)
ev = get_event(event_id) if event_id else None

# Tipo evento: format o artist
default_type = ev.type if ev else "format"
type_index = 0 if default_type == "format" else 1
event_type = st.radio("Tipo evento", options=["format", "artist"], index=type_index, horizontal=True)

# Layout form
with st.form("event_form", clear_on_submit=False):
    left, right = st.columns([2, 1])

    with left:
        title = st.text_input("Titolo evento", value=ev.title if ev else "")
        ev_date = st.date_input("Data", value=ev.date if ev else date.today())
        location = st.text_input("Luogo", value=ev.location if ev else "")

        # Services multiselect
        services = list_services()
        service_map = {s.id: s.name for s in services}
        default_services = [s.id for s in ev.services] if ev and ev.services else []
        selected_services = st.multiselect("Service", options=list(service_map.keys()), format_func=lambda x: service_map[x], default=default_services)

        st.markdown("### Pagamenti")
        acconto = st.number_input("Acconto (€)", value=float(ev.payments_acconto) if ev and ev.payments_acconto is not None else 0.0, step=10.0, format="%.2f")
        saldo = st.number_input("Saldo (€)", value=float(ev.payments_saldo) if ev and ev.payments_saldo is not None else 0.0, step=10.0, format="%.2f")

        notes = st.text_area("Note evento", value=ev.notes if ev else "", height=140)

    with right:
        st.markdown("### Logistica")
        van = st.text_input("Van", value=ev.van if ev else "")
        travel = st.text_input("Viaggi", value=ev.travel if ev else "")
        hotel = st.text_input("Hotel", value=ev.hotel if ev else "")
        allestimenti = st.text_area("Allestimenti", value=ev.allestimenti if ev else "", height=80)

        st.markdown("### Selezioni rapide")
        formats = list_formats()
        format_map = {f.id: f.name for f in formats}
        format_default = ev.format_id if ev and ev.format_id else None
        format_options = [None] + list(format_map.keys())
        format_index = 0
        if format_default:
            try:
                format_index = format_options.index(format_default)
            except ValueError:
                format_index = 0
        format_choice = st.selectbox("Format (opzionale)", options=format_options, format_func=lambda x: format_map.get(x, "-"), index=format_index)

        promoters = list_promoters()
        promoter_map = {p.id: p.name for p in promoters}
        promoter_choice = st.selectbox("Promoter", options=[None] + list(promoter_map.keys()), format_func=lambda x: promoter_map.get(x, "-"), index=0 if not ev or not ev.promoter_id else list(promoter_map.keys()).index(ev.promoter_id)+1)

        tms = list_tour_managers()
        tm_map = {t.id: t.name for t in tms}
        tm_choice = st.selectbox("Tour Manager", options=[None] + list(tm_map.keys()), format_func=lambda x: tm_map.get(x, "-"), index=0 if not ev or not ev.tour_manager_id else list(tm_map.keys()).index(ev.tour_manager_id)+1)

    st.markdown("---")

    # Campi specifici per tipo
    if event_type == "format":
        st.subheader("Campi specifici per FORMAT")
        djs = list_artists_by_role("dj")
        dj_map = {d.id: d.name for d in djs}
        dj_default = ev.dj_id if ev and getattr(ev, "dj_id", None) else None
        dj_choice = st.selectbox("DJ", options=[None] + list(dj_map.keys()), format_func=lambda x: dj_map.get(x, "-"), index=0 if not dj_default else list(dj_map.keys()).index(dj_default)+1)

        vocals = list_artists_by_role("vocalist")
        vocal_map = {v.id: v.name for v in vocals}
        vocalist_default = ev.vocalist_id if ev and getattr(ev, "vocalist_id", None) else None
        vocalist_choice = st.selectbox("Vocalist", options=[None] + list(vocal_map.keys()), format_func=lambda x: vocal_map.get(x, "-"), index=0 if not vocalist_default else list(vocal_map.keys()).index(vocalist_default)+1)

        ballerine = list_artists_by_role("ballerina")
        ballerine_map = {b.id: b.name for b in ballerine}
        default_ballerine = ev.ballerine_ids.split(",") if ev and ev.ballerine_ids else []
        default_ballerine = [int(x) for x in default_ballerine if x]
        ballerine_choice = st.multiselect("Ballerine", options=list(ballerine_map.keys()), format_func=lambda x: ballerine_map[x], default=default_ballerine)

        mascotte = list_artists_by_role("mascotte")
        mascotte_map = {m.id: m.name for m in mascotte}
        default_mascotte = ev.mascotte_ids.split(",") if ev and ev.mascotte_ids else []
        default_mascotte = [int(x) for x in default_mascotte if x]
        mascotte_choice = st.multiselect("Mascotte", options=list(mascotte_map.keys()), format_func=lambda x: mascotte_map[x], default=default_mascotte)

    else:
        st.subheader("Campi specifici per ARTISTA")
        facchini = st.text_input("Facchini", value=ev.facchini if ev else "")
        artists = list_artists()
        artist_map = {a.id: f"{a.name} ({a.role})" for a in artists}
        default_artist = ev.artists[0].id if ev and ev.artists else None
        artist_choice = st.selectbox("Artista principale", options=[None] + list(artist_map.keys()), format_func=lambda x: artist_map.get(x, "-"), index=0 if not default_artist else list(artist_map.keys()).index(default_artist)+1)

    st.markdown("---")
    status = st.selectbox("Stato evento", options=["bozza", "confermato", "cancellato"], index=0 if not ev else ["bozza", "confermato", "cancellato"].index(ev.status if ev.status in ["bozza", "confermato", "cancellato"] else "bozza"))

    # Azioni inline
    col_save, col_delete, col_cancel = st.columns([1,1,1])
    with col_save:
        save_btn = st.form_submit_button("Salva evento")
    with col_delete:
        delete_btn = st.form_submit_button("Elimina evento")
    with col_cancel:
        cancel_btn = st.form_submit_button("Annulla")

    # Gestione submit
    if save_btn:
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

        try:
            new_ev = save_event(payload)
            if new_ev:
                st.success("Evento salvato")
                # pulizia stato e ritorno al calendario
                if "open_event_id" in st.session_state:
                    st.session_state.pop("open_event_id")
                st.experimental_rerun()
            else:
                st.error("Errore nel salvataggio")
        except Exception as e:
            st.error(f"Errore: {e}")

    if delete_btn and ev:
        try:
            ok = delete_event(ev.id)
            if ok:
                st.success("Evento eliminato")
                if "open_event_id" in st.session_state:
                    st.session_state.pop("open_event_id")
                st.experimental_rerun()
            else:
                st.error("Impossibile eliminare l'evento")
        except Exception as e:
            st.error(f"Errore: {e}")

    if cancel_btn:
        if "open_event_id" in st.session_state:
            st.session_state.pop("open_event_id")
        st.experimental_rerun()

# Se non siamo nel form ma l'utente è loggato e ha aperto un evento, mostriamo un riepilogo
if not st.session_state.get("open_event_id") and ev:
    st.info("Evento caricato. Usa il form per modificare o crea un nuovo evento dal calendario.")
