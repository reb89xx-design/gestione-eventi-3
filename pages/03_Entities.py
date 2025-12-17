import streamlit as st
st.header("Gestione entità")
tab = st.tabs(["Artisti","Format","Service","Promoter","Tour Manager"])
with tab[0]:
    st.subheader("Artisti")
    st.text_input("Nuovo artista")
    st.button("Aggiungi")
