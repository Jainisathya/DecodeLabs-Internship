import streamlit as st
from utils import greeting


def render_hero():
    msg = greeting()
    st.markdown(f"""
<div class="hero-wrap">
    <h1>🤖 AI Smart Recommendation Hub</h1>
    <p>{msg} &nbsp;·&nbsp; Discover personalized recommendations powered by AI across 8 categories.</p>
</div>
""", unsafe_allow_html=True)
