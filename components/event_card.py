# components/event_card.py
import streamlit as st
from datetime import date
from utils import get_event, duplicate_event, create_tasks_from_template, save_event
from components.styles import status_badge

def render_event_card(ev, compact: bool = True):
    """
    Render a compact event card with quick actions.
    ev: Event ORM object (must have id, title, date, location, status, payments)
    """
    cols = st.columns([4,1,1])
    with cols[0]:
        st.markdown(f"**{ev.title or 'Untitled'}**")
        st.write(f"{ev.date}  •  {ev.location or '—'}")
        # artists summary
        if getattr(ev, "artists", None):
            names = ", ".join([a.name for a in ev.artists][:3])
            st.write(f"Artisti: {names}" + ("" if len(ev.artists) <= 3 else " …"))
        # payments quick
        pa = ev.payments_acconto if getattr(ev, "payments_acconto", None) is not None else "-"
        ps = ev.payments_saldo if getattr(ev, "payments_saldo", None) is not None else "-"
        st.write(f"Acconto: **{pa}**  •  Saldo: **{ps}**")
    with cols[1]:
        # status badge
        st.markdown(status_badge(ev.status), unsafe_allow_html=True)
        # small info icons
        icons = []
        if ev.dj_id:
            icons.append("🎧")
        if ev.hotel:
            icons.append("🏨")
        if ev.van:
            icons.append("🚐")
        st.write(" ".join(icons))
    with cols[2]:
        if st.button("Apri", key=f"open_{ev.id}"):
            st.session_state["open_event_id"] = ev.id
            st.experimental_rerun()
        if st.button("Duplica", key=f"dup_{ev.id}"):
            new_ev = duplicate_event(ev.id)
            if new_ev:
                st.success("Evento duplicato")
                st.experimental_rerun()
    # footer quick actions
    with st.expander("Azioni rapide", expanded=False):
        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            if st.button("Checklist format", key=f"tpl_{ev.id}"):
                create_tasks_from_template(ev.id, "format_checklist", assignee="", due_date=date.today())
                st.success("Checklist aggiunta")
                st.experimental_rerun()
        with c2:
            if st.button("Segna confermato", key=f"confirm_{ev.id}"):
                save_event({"id": ev.id, "status": "confermato"})
                st.success("Stato aggiornato")
                st.experimental_rerun()
        with c3:
            if st.button("Segna cancellato", key=f"cancel_{ev.id}"):
                save_event({"id": ev.id, "status": "cancellato"})
                st.success("Stato aggiornato")
                st.experimental_rerun()
