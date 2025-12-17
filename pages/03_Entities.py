# pages/03_Entities.py
import streamlit as st
from utils import (
    list_artists, add_artist, update_artist, delete_artist,
    list_formats, add_format, update_format, delete_format,
    list_services, add_service, update_service, delete_service,
    list_promoters, add_promoter, update_promoter, delete_promoter,
    list_tour_managers, add_tour_manager, update_tour_manager, delete_tour_manager
)

st.set_page_config(page_title="Entità - Agency Planner", layout="wide")
st.header("Gestione entità")

tabs = st.tabs(["Artisti","Format","Service","Promoter","Tour Manager"])

#### ARTISTI
with tabs[0]:
    st.subheader("Artisti e performer")
    with st.expander("Aggiungi nuovo artista / performer"):
        with st.form("add_artist_form"):
            name = st.text_input("Nome")
            role = st.selectbox("Ruolo", ["artist","mascotte","vocalist","ballerina","dancer","other"])
            phone = st.text_input("Telefono")
            email = st.text_input("Email")
            notes = st.text_area("Note")
            submitted = st.form_submit_button("Aggiungi artista")
            if submitted:
                if not name.strip():
                    st.error("Inserisci il nome")
                else:
                    add_artist(name=name, role=role, phone=phone, email=email, notes=notes)
                    st.success("Artista aggiunto")
    st.markdown("---")
    st.subheader("Lista artisti")
    artists = list_artists()
    for a in artists:
        cols = st.columns([3,1,1,1])
        with cols[0]:
            st.markdown(f"**{a.name}**  —  _{a.role}_")
            st.write(f"Email: {a.email}  •  Tel: {a.phone}")
            st.write(a.notes or "")
        with cols[1]:
            if st.button("Modifica", key=f"edit_artist_{a.id}"):
                st.session_state["edit_artist_id"] = a.id
                st.experimental_rerun()
        with cols[2]:
            if st.button("Elimina", key=f"del_artist_{a.id}"):
                delete_artist(a.id)
                st.success("Artista eliminato")
                st.experimental_rerun()
        with cols[3]:
            if st.button("Apri eventi", key=f"open_ev_artist_{a.id}"):
                st.session_state["filter_artist"] = a.id
                st.info(f"Filtro eventi per artista {a.name}")

    # Modifica artista (se selezionato)
    if st.session_state.get("edit_artist_id"):
        aid = st.session_state["edit_artist_id"]
        artist = None
        for x in artists:
            if x.id == aid:
                artist = x
                break
        if artist:
            st.markdown("---")
            st.subheader(f"Modifica artista: {artist.name}")
            with st.form("edit_artist_form"):
                name = st.text_input("Nome", value=artist.name)
                role = st.selectbox("Ruolo", ["artist","mascotte","vocalist","ballerina","dancer","other"], index=["artist","mascotte","vocalist","ballerina","dancer","other"].index(artist.role if artist.role in ["artist","mascotte","vocalist","ballerina","dancer","other"] else "other"))
                phone = st.text_input("Telefono", value=artist.phone)
                email = st.text_input("Email", value=artist.email)
                notes = st.text_area("Note", value=artist.notes)
                submitted = st.form_submit_button("Salva modifiche")
                if submitted:
                    update_artist(artist.id, name=name, role=role, phone=phone, email=email, notes=notes)
                    st.success("Artista aggiornato")
                    del st.session_state["edit_artist_id"]
                    st.experimental_rerun()

#### FORMAT
with tabs[1]:
    st.subheader("Format")
    with st.expander("Aggiungi nuovo format"):
        with st.form("add_format_form"):
            name = st.text_input("Nome format")
            description = st.text_area("Descrizione")
            notes = st.text_area("Note (interne)")
            submitted = st.form_submit_button("Aggiungi format")
            if submitted:
                if not name.strip():
                    st.error("Inserisci il nome del format")
                else:
                    add_format(name=name, description=description, notes=notes)
                    st.success("Format aggiunto")
    st.markdown("---")
    st.subheader("Lista format")
    formats = list_formats()
    for f in formats:
        cols = st.columns([3,1,1])
        with cols[0]:
            st.markdown(f"**{f.name}**")
            st.write(f.description or "")
            st.write(f.notes or "")
        with cols[1]:
            if st.button("Modifica", key=f"edit_format_{f.id}"):
                st.session_state["edit_format_id"] = f.id
                st.experimental_rerun()
        with cols[2]:
            if st.button("Elimina", key=f"del_format_{f.id}"):
                delete_format(f.id)
                st.success("Format eliminato")
                st.experimental_rerun()

    if st.session_state.get("edit_format_id"):
        fid = st.session_state["edit_format_id"]
        fmt = next((x for x in formats if x.id == fid), None)
        if fmt:
            st.markdown("---")
            st.subheader(f"Modifica format: {fmt.name}")
            with st.form("edit_format_form"):
                name = st.text_input("Nome", value=fmt.name)
                description = st.text_area("Descrizione", value=fmt.description)
                notes = st.text_area("Note", value=fmt.notes)
                submitted = st.form_submit_button("Salva format")
                if submitted:
                    update_format(fmt.id, name=name, description=description, notes=notes)
                    st.success("Format aggiornato")
                    del st.session_state["edit_format_id"]
                    st.experimental_rerun()

#### SERVICE
with tabs[2]:
    st.subheader("Service impianti")
    with st.expander("Aggiungi nuovo service"):
        with st.form("add_service_form"):
            name = st.text_input("Nome service")
            contact = st.text_input("Contatto")
            phone = st.text_input("Telefono")
            notes = st.text_area("Note")
            submitted = st.form_submit_button("Aggiungi service")
            if submitted:
                if not name.strip():
                    st.error("Inserisci il nome del service")
                else:
                    add_service(name=name, contact=contact, phone=phone, notes=notes)
                    st.success("Service aggiunto")
    st.markdown("---")
    st.subheader("Lista service")
    services = list_services()
    for s in services:
        cols = st.columns([3,1,1])
        with cols[0]:
            st.markdown(f"**{s.name}**")
            st.write(f"Contatto: {s.contact}  •  Tel: {s.phone}")
            st.write(s.notes or "")
        with cols[1]:
            if st.button("Modifica", key=f"edit_service_{s.id}"):
                st.session_state["edit_service_id"] = s.id
                st.experimental_rerun()
        with cols[2]:
            if st.button("Elimina", key=f"del_service_{s.id}"):
                delete_service(s.id)
                st.success("Service eliminato")
                st.experimental_rerun()

    if st.session_state.get("edit_service_id"):
        sid = st.session_state["edit_service_id"]
        svc = next((x for x in services if x.id == sid), None)
        if svc:
            st.markdown("---")
            st.subheader(f"Modifica service: {svc.name}")
            with st.form("edit_service_form"):
                name = st.text_input("Nome", value=svc.name)
                contact = st.text_input("Contatto", value=svc.contact)
                phone = st.text_input("Telefono", value=svc.phone)
                notes = st.text_area("Note", value=svc.notes)
                submitted = st.form_submit_button("Salva service")
                if submitted:
                    update_service(svc.id, name=name, contact=contact, phone=phone, notes=notes)
                    st.success("Service aggiornato")
                    del st.session_state["edit_service_id"]
                    st.experimental_rerun()

#### PROMOTER
with tabs[3]:
    st.subheader("Promoter")
    with st.expander("Aggiungi nuovo promoter"):
        with st.form("add_promoter_form"):
            name = st.text_input("Nome promoter")
            contact = st.text_input("Contatto")
            phone = st.text_input("Telefono")
            email = st.text_input("Email")
            notes = st.text_area("Note")
            submitted = st.form_submit_button("Aggiungi promoter")
            if submitted:
                if not name.strip():
                    st.error("Inserisci il nome del promoter")
                else:
                    add_promoter(name=name, contact=contact, phone=phone, email=email, notes=notes)
                    st.success("Promoter aggiunto")
    st.markdown("---")
    st.subheader("Lista promoter")
    promoters = list_promoters()
    for p in promoters:
        cols = st.columns([3,1,1])
        with cols[0]:
            st.markdown(f"**{p.name}**")
            st.write(f"Contatto: {p.contact}  •  Tel: {p.phone}  •  Email: {p.email}")
            st.write(p.notes or "")
        with cols[1]:
            if st.button("Modifica", key=f"edit_promoter_{p.id}"):
                st.session_state["edit_promoter_id"] = p.id
                st.experimental_rerun()
        with cols[2]:
            if st.button("Elimina", key=f"del_promoter_{p.id}"):
                delete_promoter(p.id)
                st.success("Promoter eliminato")
                st.experimental_rerun()

    if st.session_state.get("edit_promoter_id"):
        pid = st.session_state["edit_promoter_id"]
        prm = next((x for x in promoters if x.id == pid), None)
        if prm:
            st.markdown("---")
            st.subheader(f"Modifica promoter: {prm.name}")
            with st.form("edit_promoter_form"):
                name = st.text_input("Nome", value=prm.name)
                contact = st.text_input("Contatto", value=prm.contact)
                phone = st.text_input("Telefono", value=prm.phone)
                email = st.text_input("Email", value=prm.email)
                notes = st.text_area("Note", value=prm.notes)
                submitted = st.form_submit_button("Salva promoter")
                if submitted:
                    update_promoter(prm.id, name=name, contact=contact, phone=phone, email=email, notes=notes)
                    st.success("Promoter aggiornato")
                    del st.session_state["edit_promoter_id"]
                    st.experimental_rerun()

#### TOUR MANAGER
with tabs[4]:
    st.subheader("Tour Manager")
    with st.expander("Aggiungi nuovo tour manager"):
        with st.form("add_tm_form"):
            name = st.text_input("Nome")
            contact = st.text_input("Contatto")
            phone = st.text_input("Telefono")
            email = st.text_input("Email")
            notes = st.text_area("Note")
            submitted = st.form_submit_button("Aggiungi tour manager")
            if submitted:
