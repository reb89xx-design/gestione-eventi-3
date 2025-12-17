# pages/05_Tasklist.py
import streamlit as st
from datetime import date
from utils import (
    list_events_by_date, list_tasks_by_date, list_tasks_for_event,
    add_task, update_task, delete_task, toggle_task_done,
    get_event, save_event,
    list_artists_by_role, list_promoters, list_tour_managers, list_services, create_tasks_from_template, get_user_tasks
)
import json
from pathlib import Path

st.set_page_config(page_title="TaskList", layout="wide")
st.header("TaskList giornaliera")

selected_date = st.date_input("Seleziona data", value=date.today())

ROOT = Path(__file__).resolve().parents[1]
users_file = ROOT / "users.json"
team_members = []
if users_file.exists():
    try:
        data = json.loads(users_file.read_text(encoding="utf-8"))
        team_members = [u for u in data.keys()]
    except Exception:
        team_members = []
if not team_members:
    team_members = ["ale", "marta", "luca"]

events = list_events_by_date(selected_date)

st.markdown(f"### Eventi del {selected_date} — {len(events)} trovati")

for ev in events:
    with st.expander(f"{ev.title or 'Untitled'} — {ev.location}  •  Stato: {ev.status}", expanded=False):
        cols = st.columns([3,1])
        with cols[0]:
            st.markdown("**Modifica rapida evento**")
            title = st.text_input("Titolo", value=ev.title or "", key=f"title_ev_{ev.id}")
            location = st.text_input("Luogo", value=ev.location or "", key=f"loc_ev_{ev.id}")

            djs = list_artists_by_role("dj")
            dj_map = {d.id: d.name for d in djs}
            current_dj = getattr(ev, "dj_id", None)
            dj_choice = st.selectbox("DJ", options=[None] + list(dj_map.keys()), format_func=lambda x: dj_map.get(x, "-"), index=0 if not current_dj else list(dj_map.keys()).index(current_dj)+1, key=f"dj_ev_{ev.id}")

            promoters = list_promoters()
            promoter_map = {p.id: p.name for p in promoters}
            promoter_choice = st.selectbox("Promoter", options=[None] + list(promoter_map.keys()), format_func=lambda x: promoter_map.get(x, "-"), index=0 if not ev.promoter_id else list(promoter_map.keys()).index(ev.promoter_id)+1, key=f"prom_ev_{ev.id}")

            hotel_notes = st.text_area("Note hotel / logistica", value=ev.allestimenti or "", key=f"hotel_ev_{ev.id}")

            if st.button("Salva modifiche evento", key=f"save_ev_inline_{ev.id}"):
                payload = {
                    "id": ev.id,
                    "title": title,
                    "location": location,
                    "allestimenti": hotel_notes,
                    "dj_id": dj_choice,
                    "promoter_id": promoter_choice
                }
                try:
                    save_event(payload)
                    st.success("Evento aggiornato")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Errore salvataggio: {e}")

        with cols[1]:
            st.markdown("**Task per questo evento**")
            tasks = list_tasks_for_event(ev.id)
            for t in tasks:
                tcols = st.columns([4,1,1])
                with tcols[0]:
                    done_label = "✅ " if t.done else ""
                    st.markdown(f"**{done_label}{t.title}**")
                    st.write(t.description or "")
                    st.write(f"Assignee: {t.assignee or '—'}  •  Due: {t.due_date or '—'}")
                with tcols[1]:
                    if st.button("Toggle done", key=f"toggle_{t.id}"):
                        toggle_task_done(t.id)
                        st.experimental_rerun()
                with tcols[2]:
                    if st.button("Elimina", key=f"deltask_{t.id}"):
                        delete_task(t.id)
                        st.experimental_rerun()

            st.markdown("---")
            st.markdown("**Aggiungi nuova task**")
            with st.form(f"add_task_form_{ev.id}", clear_on_submit=True):
                t_title = st.text_input("Titolo task")
                t_desc = st.text_area("Descrizione")
                t_assignee = st.selectbox("Assegna a", options=[""] + team_members)
                t_due = st.date_input("Due date", value=selected_date)
                submitted = st.form_submit_button("Aggiungi task")
                if submitted:
                    if not t_title.strip():
                        st.error("Inserisci un titolo per la task")
                    else:
                        add_task(event_id=ev.id, title=t_title, description=t_desc, assignee=t_assignee, due_date=t_due)
                        st.success("Task aggiunta")
                        st.experimental_rerun()

            st.markdown("---")
            st.markdown("**Aggiungi checklist standard**")
            if st.button("Aggiungi checklist format", key=f"tpl_format_{ev.id}"):
                create_tasks_from_template(ev.id, "format_checklist", assignee="", due_date=selected_date)
                st.success("Checklist aggiunta")
                st.experimental_rerun()

        st.markdown("---")
        if st.button("Apri scheda evento completa", key=f"open_full_{ev.id}"):
            st.session_state["open_event_id"] = ev.id
            st.experimental_rerun()

if not events:
    st.info("Nessun evento per la data selezionata. Puoi creare eventi dal calendario o dalla pagina di creazione evento.")
