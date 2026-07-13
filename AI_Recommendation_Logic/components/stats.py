import streamlit as st


STATS = [
    ("8",    "Categories"),
    ("80+",  "Dataset Items"),
    ("AI",   "NLP Engine"),
    ("<1s",  "Response Time"),
]


def render_stats():
    cols = st.columns(4)
    for col, (value, label) in zip(cols, STATS):
        with col:
            st.markdown(f"""
<div class="stat-card">
    <span class="stat-value">{value}</span>
    <span class="stat-label">{label}</span>
</div>
""", unsafe_allow_html=True)
    st.write("")
