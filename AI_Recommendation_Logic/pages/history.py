import streamlit as st
import pandas as pd
from database import get_history, clear_history


def show_history():
    st.markdown('<div class="section-header">🕒 Search History</div>',
                unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = []

    # Sync from DB
    if len(st.session_state.history) == 0:
        try:
            rows = get_history()
            for r in rows:
                st.session_state.history.append({
                    "category": r[1],
                    "query":    r[2],
                    "time":     str(r[3]) if len(r) > 3 else ""
                })
        except Exception:
            pass

    if len(st.session_state.history) == 0:
        st.info("No searches yet. Head to the Dashboard and start exploring!")
        return

    st.markdown(f"**{len(st.session_state.history)} searches recorded**")
    st.divider()

    history_display = list(reversed(st.session_state.history))

    for i, item in enumerate(history_display):
        category = item.get("category", "")
        query    = item.get("query", item) if isinstance(item, dict) else str(item)
        time_str = item.get("time", "") if isinstance(item, dict) else ""

        st.markdown(f"""
<div class="rec-card" style="margin:6px 0;padding:14px 20px;">
    <div class="rec-header">
        <span class="rec-title">🔍 {query}</span>
        <span class="rec-badge">{category}</span>
    </div>
    {'<span style="font-size:0.8rem;opacity:0.5;">'+time_str+'</span>' if time_str else ''}
</div>
""", unsafe_allow_html=True)

    st.divider()

    df = pd.DataFrame(
        [{"Category": h.get("category", ""), "Query": h.get("query", str(h))}
         if isinstance(h, dict) else {"Category": "", "Query": str(h)}
         for h in st.session_state.history]
    )
    with st.expander("📄 View as Table"):
        st.dataframe(df, use_container_width=True)

    if st.button("🧹 Clear History", use_container_width=True):
        st.session_state.history = []
        try:
            clear_history()
        except Exception:
            pass
        st.success("History cleared.")
        st.rerun()
