import streamlit as st


def render_footer():
    st.markdown("""
<div class="footer-wrap">
    🤖 <strong>AI Smart Recommendation Hub</strong> &nbsp;·&nbsp; v1.0.0
    &nbsp;·&nbsp; Built with ❤️ using Streamlit, Scikit-Learn &amp; Plotly
</div>
""", unsafe_allow_html=True)
