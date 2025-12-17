# components/kanban_board.py
import streamlit as st
from datetime import date, timedelta
from utils import list_events_range, save_event
from components.event_card import render_event_card

DEFAULT_STATES = ["bozza", "confermato", "cancellato"]

def render_kanban(start_date: date = None, days: int = 7, states: list = None):
    if start_date is None:
        start_date = date.today()
    if states is None:
        states = DEFAULT_STATES
    end_date = start_date + timedelta(days=days-1)
    st.markdown(f"### Kanban per stato — {start_date.isoformat()} → {end_date.isoformat()}")
    events = list_events_range(start_date, end_date)
    columns = st.columns(len(states))
    for idx, state in enumerate(states):
        with columns[idx]:
            st.markdown(f"**{state.upper()}**")
            col_events = [e for e in events if e.status == state]
            if not col_events:
                st.write("—")
            for ev in col_events:
                with st.container():
                    render_event_card(ev, compact=True)
                    # quick actions to move state
                    target_cols = st.columns([1,1,1])
                    with target_cols[0]:
                        if st.button("◀ Prev State", key=f"prev_state_{ev.id}_{state}"):
                            # move to previous state in list if exists
                            try:
                                i = states.index(state)
                                if i > 0:
                                    save_event({"id": ev.id, "status": states[i-1]})
                                    st.experimental_rerun()
                            except Exception:
                                pass
                    with target_cols[1]:
                        if st.button("Set Confirmed", key=f"confirm_state_{ev.id}"):
                            save_event({"id": ev.id, "status": "confermato"})
                            st.experimental_rerun()
                    with target_cols[2]:
                        if st.button("Next State ▶", key=f"next_state_{ev.id}_{state}"):
                            try:
                                i = states.index(state)
                                if i < len(states)-1:
                                    save_event({"id": ev.id, "status": states[i+1]})
                                    st.experimental_rerun()
                            except Exception:
                                pass
