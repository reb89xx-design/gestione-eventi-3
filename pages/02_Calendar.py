import streamlit as st
import pandas as pd
from datetime import date
st.header("Calendario globale")
d = st.date_input("Seleziona giorno", value=date.today())
st.write("Eventi del giorno selezionato")
# Qui carichi dal DB gli eventi per la data e li mostri in lista o card
