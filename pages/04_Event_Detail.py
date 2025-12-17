import streamlit as st
st.header("Scheda Evento")
event_id = st.text_input("ID evento (nuovo lascia vuoto)")
title = st.text_input("Titolo")
date = st.date_input("Data")
location = st.text_input("Luogo")
artists = st.multiselect("Artisti", options=["Artista A","Artista B"])
status = st.selectbox("Stato", ["bozza","confermato","cancellato"])
st.text_area("Note")
if st.button("Salva"):
    st.success("Evento salvato")
