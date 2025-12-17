# pages/04_Event_Detail.py
import streamlit as st
from datetime import date
from utils import (
    get_event, save_event, delete_event, list_artists_by_role,
    list_formats, list_services, list_promoters, list_tour_managers,
    get_audit_logs, record_audit
)

st.set_page_config(page_title="Scheda Evento", layout="wide")
st.header("Scheda Evento")

event_id = st.session_state.get("open_event_id", None)
ev = get_event(event_id) if event_id else None

if not ev:
    st.info("Nessun evento selezionato. Apri un evento dal calendario o dalla lista.")
else:
    st.markdown(f"## Evento: {ev.title}  •  {ev.date}")
    # form principale
    with st.form("event_form", clear_on_submit=False):
        left, right = st.columns([2,1])
        with left:
            title = st.text_input("Titolo", value=ev.title or "")
            ev_date = st.date_input("Data", value=ev.date or date.today())
            location = st.text_input("Luogo", value=ev.location or "")
            notes = st.text_area("Note", value=ev.notes or "", height=140)
            services = list_services()
            service_map = {s.id: s.name for s in services}
            default_services = [s.id for s in ev.services] if ev.services else []
            selected_services = st.multiselect("Service", options=list(service_map.keys()), format_func=lambda x: service_map[x], default=default_services)
        with right:
            st.markdown("### Logistica")
            van = st.text_input("Van", value=ev.van or "")
            travel = st.text_input("Viaggi", value=ev.travel or "")
            hotel = st.text_input("Hotel", value=ev.hotel or "")
            allestimenti = st.text_area("Allestimenti", value=ev.allestimenti or "", height=80)
            st.markdown("### Selezioni rapide")
            formats = list_formats()
            format_map = {f.id: f.name for f in formats}
            format_choice = st.selectbox("Format", options=[None] + list(format_map.keys()), format_func=lambda x: format_map.get(x, "-"), index=0 if not ev.format_id else list(format_map.keys()).index(ev.format_id)+1)
            promoters = list_promoters()
            promoter_map = {p.id: p.name for p in promoters}
            promoter_choice = st.selectbox("Promoter", options=[None] + list(promoter_map.keys()), format_func=lambda x: promoter_map.get(x, "-"), index=0 if not ev.promoter_id else list(promoter_map.keys()).index(ev.promoter_id)+1)
            tms = list_tour_managers()
            tm_map = {t.id: t.name for t in tms}
            tm_choice = st.selectbox("Tour Manager", options=[None] + list(tm_map.keys()), format_func=lambda x: tm_map.get(x, "-"), index=0 if not ev.tour_manager_id else list(tm_map.keys()).index(ev.tour_manager_id)+1)

        st.markdown("---")
        status = st.selectbox("Stato evento", options=["bozza","confermato","cancellato"], index=["bozza","confermato","cancellato"].index(ev.status if ev.status in ["bozza","confermato","cancellato"] else "bozza"))
        col_save, col_delete, col_cancel = st.columns([1,1,1])
        with col_save:
            save_btn = st.form_submit_button("Salva")
        with col_delete:
            delete_btn = st.form_submit_button("Elimina")
        with col_cancel:
            cancel_btn = st.form_submit_button("Annulla")

        if save_btn:
            payload = {
                "id": ev.id,
                "title": title,
                "date": ev_date,
                "location": location,
                "notes": notes,
                "van": van,
                "travel": travel,
                "hotel": hotel,
                "allestimenti": allestimenti,
                "format_id": format_choice,
                "promoter_id": promoter_choice,
                "tour_manager_id": tm_choice,
                "service_ids": selected_services,
                "status": status
            }
            try:
                new_ev = save_event(payload, user=st.session_state.get("user",""))
                if new_ev:
                    st.success("Evento salvato")
                    st.session_state.pop("open_event_id", None)
                    st.experimental_rerun()
                else:
                    st.error("Errore salvataggio")
            except Exception as e:
                st.error(f"Errore: {e}")

        if delete_btn:
            try:
                ok = delete_event(ev.id, user=st.session_state.get("user",""))
                if ok:
                    st.success("Evento eliminato")
                    st.session_state.pop("open_event_id", None)
                    st.experimental_rerun()
                else:
                    st.error("Impossibile eliminare")
            except Exception as e:
                st.error(f"Errore: {e}")

        if cancel_btn:
            st.session_state.pop("open_event_id", None)
            st.experimental_rerun()

    # sezione Audit e Activity
    st.markdown("---")
    st.markdown("## Activity Audit")
    logs = get_audit_logs(entity="event", entity_id=ev.id, limit=200)
    if not logs:
        st.info("Nessuna attività registrata per questo evento")
    else:
        for log in logs:
            with st.expander(f"{log.ts.isoformat()}  •  {log.action}  •  user: {log.user or '—'}", expanded=False):
                try:
                    payload = json.loads(log.payload)
                except Exception:
                    payload = log.payload
                st.write(payload)
                # offri revert se payload contiene snapshot 'after'
                if isinstance(payload, dict) and payload.get("after"):
                    if st.button("Ripristina snapshot", key=f"revert_{log.id}"):
                        try:
                            # payload['after'] dovrebbe contenere i campi da ripristinare
                            after = payload.get("after")
                            # assicurati di passare solo campi validi per save_event
                            save_event(after, user=st.session_state.get("user",""))
                            st.success("Snapshot ripristinato")
                            st.experimental_rerun()
                        except Exception as e:
                            st.error(f"Errore ripristino: {e}")

    # link rapido per aprire TaskList per questo evento
    st.markdown("---")
    if st.button("Apri TaskList per questo evento"):
        st.session_state["open_task_for_event"] = True
        st.session_state["open_event_id"] = ev.id
        st.experimental_rerun()
