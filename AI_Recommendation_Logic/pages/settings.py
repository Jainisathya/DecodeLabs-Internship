import streamlit as st
import pandas as pd
from styles import THEMES
from database import clear_favorites, clear_history


def show_settings():
    st.markdown('<div class="section-header">⚙️ Settings</div>',
                unsafe_allow_html=True)

    # ── Appearance ────────────────────────────────────────────────────────────
    st.subheader("🎨 Appearance")

    current_theme = st.session_state.get("theme", "Dark")
    theme_keys    = list(THEMES.keys())
    theme_idx     = theme_keys.index(current_theme) if current_theme in theme_keys else 0

    new_theme = st.selectbox("Theme", theme_keys, index=theme_idx)

    if st.button("Apply Theme", use_container_width=False):
        st.session_state.theme = new_theme
        st.success(f"Theme switched to **{new_theme}**!")
        st.rerun()

    st.divider()

    # ── Recommendation defaults ───────────────────────────────────────────────
    st.subheader("🤖 Recommendation Defaults")

    rec_count   = st.slider("Default Results",         5,  20, 10)
    min_rating  = st.slider("Minimum Rating",         0.0, 10.0, 5.0, 0.5)
    sim_thresh  = st.slider("Similarity Threshold",   0.0,  1.0, 0.3, 0.05)

    st.info(f"Results: **{rec_count}** · Min Rating: **{min_rating}** · "
            f"Similarity: **{sim_thresh}**")

    st.divider()

    # ── Data management ───────────────────────────────────────────────────────
    st.subheader("🗄 Data Management")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🗑 Clear Favorites", use_container_width=True):
            st.session_state.favorites = []
            try: clear_favorites()
            except Exception: pass
            st.success("Favorites cleared.")

    with col2:
        if st.button("🧹 Clear History", use_container_width=True):
            st.session_state.history = []
            try: clear_history()
            except Exception: pass
            st.success("History cleared.")

    with col3:
        if st.button("♻ Reset Everything", use_container_width=True):
            st.session_state.results   = pd.DataFrame()
            st.session_state.history   = []
            st.session_state.favorites = []
            try:
                clear_favorites()
                clear_history()
            except Exception:
                pass
            st.success("Application fully reset.")

    st.divider()

    # ── Feature list ──────────────────────────────────────────────────────────
    st.subheader("ℹ️ Active Features")
    features = [
        ("🎨", "Theme Switching",            True),
        ("🤖", "TF-IDF Recommendation Engine", True),
        ("❤️", "Favorites (SQLite)",          True),
        ("🕒", "Search History (SQLite)",     True),
        ("📊", "Analytics Dashboard",         True),
        ("🎲", "Surprise Me",                 True),
        ("📂", "8 Content Categories",        True),
        ("🎯", "Filters & Sorting",           True),
    ]
    for icon, name, active in features:
        status = "✅ Active" if active else "🔒 Coming Soon"
        st.markdown(f"{icon} **{name}** — {status}")
