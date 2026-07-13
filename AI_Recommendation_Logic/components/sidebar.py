import streamlit as st
from streamlit_option_menu import option_menu
from styles import THEMES


def render_sidebar():
    with st.sidebar:
        st.markdown("""
<div style="text-align:center;padding:12px 0 4px;">
    <span style="font-size:3rem;">🤖</span>
    <div style="font-size:1.3rem;font-weight:800;margin-top:6px;
                font-family:'Space Grotesk',sans-serif;">AI Hub</div>
    <div style="font-size:0.78rem;opacity:0.6;margin-top:2px;">
        Smart Recommendation Engine
    </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")

        page = option_menu(
            menu_title=None,
            options=["Dashboard", "Favorites", "History",
                     "Analytics", "Settings", "About"],
            icons=["house-fill", "heart-fill", "clock-history",
                   "bar-chart-fill", "gear-fill", "info-circle-fill"],
            default_index=0,
            styles={
                "container":       {"padding": "0", "background": "transparent"},
                "icon":            {"font-size": "1rem"},
                "nav-link":        {"font-size": "0.92rem", "font-weight": "500",
                                    "border-radius": "10px", "margin": "3px 0"},
                "nav-link-selected": {"font-weight": "700"},
            }
        )

        st.markdown("---")

        theme = st.selectbox(
            "🎨 Theme",
            list(THEMES.keys()),
            index=list(THEMES.keys()).index(
                st.session_state.get("theme", "Dark")
            )
        )

    return page, theme
