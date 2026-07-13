import streamlit as st
from analytics import Analytics


_analytics = Analytics()


def show_analytics():
    st.markdown('<div class="section-header">📊 Analytics Dashboard</div>',
                unsafe_allow_html=True)

    if "results" not in st.session_state or st.session_state.results.empty:
        st.info("No recommendations yet. Go to the Dashboard and generate some first!")
        return

    df = st.session_state.results

    # ── Summary metrics ────────────────────────────────────────────────────────
    summary = _analytics.summary(df)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("📚 Items",           summary["items"])
    with c2: st.metric("⭐ Avg Rating",       summary["average_rating"])
    with c3: st.metric("🏆 Highest Rating",   summary["highest_rating"])
    with c4: st.metric("📂 Categories",       summary["categories"])

    st.divider()

    # ── Charts ─────────────────────────────────────────────────────────────────
    dark = st.session_state.get("theme", "Dark") == "Dark"
    template = "plotly_dark" if dark else "plotly_white"
    bg = "rgba(0,0,0,0)"

    def _apply_theme(fig):
        fig.update_layout(
            paper_bgcolor=bg, plot_bgcolor=bg,
            template=template, height=420
        )
        return fig

    col1, col2 = st.columns(2)

    with col1:
        fig = _analytics.rating_distribution(df)
        if fig:
            st.subheader("⭐ Rating Distribution")
            st.plotly_chart(_apply_theme(fig), use_container_width=True)

    with col2:
        fig = _analytics.match_score_distribution(df)
        if fig:
            st.subheader("🎯 Match Score Distribution")
            st.plotly_chart(_apply_theme(fig), use_container_width=True)

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        fig = _analytics.top_rated_chart(df)
        if fig:
            st.subheader("🏆 Top Rated")
            st.plotly_chart(_apply_theme(fig), use_container_width=True)

    with col4:
        fig = _analytics.category_distribution(df)
        if fig:
            st.subheader("🥧 Category Split")
            st.plotly_chart(_apply_theme(fig), use_container_width=True)

    st.divider()
    st.subheader("📄 Full Dataset")
    st.dataframe(df, use_container_width=True)
