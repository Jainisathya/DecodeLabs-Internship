<<<<<<< HEAD
import streamlit as st
import pandas as pd
import plotly.express as px

from styles import load_css, THEMES
from data_loader import load_dataset
from recommender import RecommendationEngine

from database import (
    add_favorite,
    get_favorites,
    delete_favorite,
    clear_favorites,
    add_history,
    get_history,
    clear_history,
    add_analytics
)

from components.sidebar import render_sidebar
from components.hero import render_hero
from components.cards import render_cards
from components.stats import render_stats
from components.footer import render_footer
from components.recommendation_card import recommendation_card

from pages.favorites import show_favorites
from pages.history import show_history

# (These will be created later)
try:
    from pages.analytics_page import show_analytics
except:
    def show_analytics():
        st.info("Analytics page coming soon.")

try:
    from pages.settings import show_settings
except:
    def show_settings():
        st.info("Settings page coming soon.")

try:
    from pages.about import show_about
except:
    def show_about():
        st.info("About page coming soon.")

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="AI Smart Recommendation Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "history" not in st.session_state:
    st.session_state.history = []

if "results" not in st.session_state:
    st.session_state.results = pd.DataFrame()

# ------------------------------------------------
# LOAD CSS
# ------------------------------------------------

st.markdown(
    load_css(st.session_state.theme),
    unsafe_allow_html=True
)

# ------------------------------------------------
# LOAD AI ENGINE
# ------------------------------------------------

engine = RecommendationEngine()

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

page, theme = render_sidebar()

st.session_state.theme = theme

# Reload CSS after changing theme

st.markdown(
    load_css(st.session_state.theme),
    unsafe_allow_html=True
)

# ------------------------------------------------
# PAGE ROUTING
# ------------------------------------------------

if page == "Dashboard":

    render_hero()

    st.write("")

    render_stats()

    st.write("")

    st.subheader("🔍 AI Recommendation Search")

    category = st.selectbox(
        "Select Category",
        [
            "🎬 Movies",
            "📚 Books",
            "🎵 Music",
            "🍔 Food",
            "🏋 Fitness",
            "💻 Courses",
            "👨‍🍳 Recipes",
            "💼 Careers"
        ]
    )

    query = st.text_input(
        "Describe what you're looking for",
        placeholder="Example: Space adventure movies, Healthy breakfast, Python course..."
    )

    col1, col2 = st.columns(2)

    with col1:

        recommend_btn = st.button(
            "🚀 Generate Recommendations",
            use_container_width=True
        )

    with col2:

        surprise_btn = st.button(
            "🎲 Surprise Me",
            use_container_width=True
        )

            # ------------------------------------------------
    # SURPRISE ME
    # ------------------------------------------------

    if surprise_btn:

        surprise_queries = {
            "🎬 Movies": "Adventure",
            "📚 Books": "Self Improvement",
            "🎵 Music": "Relaxing",
            "🍔 Food": "Healthy",
            "🏋 Fitness": "Weight Loss",
            "💻 Courses": "Artificial Intelligence",
            "👨‍🍳 Recipes": "Quick Dinner",
            "💼 Careers": "Software Engineer"
        }

        query = surprise_queries.get(category, "")

        st.success(f"🎉 Surprise Recommendation: **{query}**")

    # ------------------------------------------------
    # GENERATE RECOMMENDATIONS
    # ------------------------------------------------

    if recommend_btn:

        if query.strip() == "":

            st.warning("⚠ Please enter something to search.")

        else:

            with st.spinner("🤖 AI is finding the best recommendations..."):

                try:

                    dataset = load_dataset(category)

                    recommendations = engine.recommend(
                        dataframe=dataset,
                        query=query,
                        top_n=8
                    )

                    st.session_state.results = recommendations
                    for _, row in recommendations.iterrows():

                        add_analytics(
                        category,
                        row["title"],
                        float(row["match_score"])
    )                        
                    add_history(category, query)
                except Exception as e:

                    st.error(f"Error: {e}")

    # ------------------------------------------------
    # DISPLAY RESULTS
    # ------------------------------------------------

    if not st.session_state.results.empty:

        st.divider()

        st.subheader("✨ Recommended For You")

        for index, row in st.session_state.results.iterrows():

            recommendation_card(row)

    else:

        st.info("Search something to get AI-powered recommendations.")

    st.divider()

    # ------------------------------------------------
    # CATEGORY CARDS
    # ------------------------------------------------

    render_cards()

    st.write("")

    # ------------------------------------------------
    # TRENDING
    # ------------------------------------------------

    st.subheader("🔥 Trending Searches")

    trending = [
        "Interstellar",
        "Atomic Habits",
        "Python Course",
        "Healthy Breakfast",
        "Workout Plan",
        "Data Scientist",
        "Italian Pasta",
        "Jazz Music"
    ]

    trend_cols = st.columns(4)

    for i, item in enumerate(trending):

        with trend_cols[i % 4]:

            st.button(
                item,
                key=f"trend_{i}",
                use_container_width=True
            )

    st.write("")

        # ------------------------------------------------
    # FILTERS
    # ------------------------------------------------

    st.divider()

    st.subheader("🎯 Recommendation Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:

        min_rating = st.slider(
            "⭐ Minimum Rating",
            min_value=0.0,
            max_value=10.0,
            value=5.0,
            step=0.5
        )

    with filter_col2:

        sort_by = st.selectbox(
            "📊 Sort By",
            [
                "Match Score",
                "Rating",
                "Title"
            ]
        )

    with filter_col3:

        max_results = st.selectbox(
            "📄 Results",
            [5, 10, 15, 20],
            index=0
        )

    # ------------------------------------------------
    # APPLY FILTERS
    # ------------------------------------------------

    if not st.session_state.results.empty:

        filtered = st.session_state.results.copy()

        if "rating" in filtered.columns:

            filtered = filtered[
                filtered["rating"] >= min_rating
            ]

        if sort_by == "Rating":

            if "rating" in filtered.columns:

                filtered = filtered.sort_values(
                    "rating",
                    ascending=False
                )

        elif sort_by == "Title":

            filtered = filtered.sort_values(
                "title"
            )

        else:

            filtered = filtered.sort_values(
                "match_score",
                ascending=False
            )

        filtered = filtered.head(max_results)

        st.divider()

        st.subheader("🏆 Top Recommendations")

        for _, row in filtered.iterrows():

            recommendation_card(row)

    # ------------------------------------------------
    # AI INSIGHTS
    # ------------------------------------------------

    st.divider()

    st.subheader("🤖 AI Insights")

    insight1, insight2, insight3 = st.columns(3)

    with insight1:

        st.metric(
            "Recommendations Generated",
            len(st.session_state.results)
        )

    with insight2:

        st.metric(
            "Searches Performed",
            len(st.session_state.history)
        )

    with insight3:

        st.metric(
            "Favorites Saved",
            len(st.session_state.favorites)
        )

    # ------------------------------------------------
    # QUICK ACTIONS
    # ------------------------------------------------

    st.divider()

    st.subheader("⚡ Quick Actions")

    q1, q2, q3 = st.columns(3)

    with q1:

        if st.button(
            "🧹 Clear Search History",
            use_container_width=True
        ):

            st.session_state.history = []

            st.success("History cleared.")

    with q2:

        if st.button(
            "❤️ Clear Favorites",
            use_container_width=True
        ):

            st.session_state.favorites = []

            st.success("Favorites cleared.")

    with q3:

        if st.button(
            "♻ Reset Recommendations",
            use_container_width=True
        ):

            st.session_state.results = pd.DataFrame()

            st.success("Recommendations reset.")

            # ------------------------------------------------
# RECOMMENDATION ANALYTICS
# ------------------------------------------------

    if not st.session_state.results.empty:

        st.divider()

        st.subheader("📊 Recommendation Analytics")

        analytics_df = st.session_state.results.copy()

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            if "rating" in analytics_df.columns:

                fig = px.bar(
                analytics_df,
                x="title",
                y="rating",
                color="rating",
                title="⭐ Ratings"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with chart_col2:

            fig = px.bar(
            analytics_df,
            x="title",
            y="match_score",
            color="match_score",
            title="🎯 Match Score"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ------------------------------------------------
# RECOMMENDATION TABLE
# ------------------------------------------------

    st.divider()

    with st.expander("📄 View Recommendation Table"):

        if not st.session_state.results.empty:

            st.dataframe(
            st.session_state.results,
            use_container_width=True
        )

        else:

            st.info("No recommendations available.")

# ------------------------------------------------
# RECENT SEARCHES
# ------------------------------------------------

            st.divider()

            st.subheader("🕒 Recent Searches")

            if len(st.session_state.history) == 0:

                st.info("No search history.")

            else:

                history_df = pd.DataFrame(
                st.session_state.history
    )

                st.dataframe(
        history_df,
        use_container_width=True
    )
# ------------------------------------------------
# FAVORITES PREVIEW
# ------------------------------------------------

    st.divider()

    st.subheader("❤️ Favorites Preview")

# Always create favorite_df first
    favorite_df = pd.DataFrame(st.session_state.favorites)

    if favorite_df.empty:

        st.info("No favorites yet.")

    else:

        st.dataframe(
        favorite_df,
        use_container_width=True
    )

# ------------------------------------------------
# POPULAR CATEGORIES
# ------------------------------------------------

    st.divider()

    st.subheader("🔥 Popular Categories")

    popular = {
    "Movies": 95,
    "Books": 82,
    "Music": 76,
    "Food": 65,
    "Fitness": 60,
    "Courses": 88,
    "Recipes": 71,
    "Careers": 54
}

    popular_df = pd.DataFrame({

    "Category": list(popular.keys()),

    "Popularity": list(popular.values())

})

    fig = px.pie(

    popular_df,

    names="Category",

    values="Popularity",

    hole=.45,

    title="Category Popularity"

)

    st.plotly_chart(

        fig,

        use_container_width=True

)

# ------------------------------------------------
# RECOMMENDATION SUMMARY
# ------------------------------------------------

    st.divider()

    st.subheader("📝 Recommendation Summary")

    if not st.session_state.results.empty:

        highest = st.session_state.results.iloc[0]["title"]

        total = len(st.session_state.results)

        st.success(

            f"""

            AI analyzed your query and generated

            **{total} personalized recommendations.**

            🏆 Best Recommendation:

            **{highest}**

            """

    )

    else:

        st.info(

        "Generate recommendations to see the AI summary."

    )

    # ------------------------------------------------
# PAGE ROUTING
# ------------------------------------------------

elif page == "Favorites":

    show_favorites()

elif page == "History":

    show_history()

elif page == "Analytics":

    show_analytics()

elif page == "Settings":

    show_settings()

elif page == "About":

    show_about()

# ------------------------------------------------
# SIDEBAR QUICK INFO
# ------------------------------------------------

with st.sidebar:

    st.markdown("---")

    st.subheader("📌 Quick Info")

    st.metric(
        "Categories",
        "8"
    )

    st.metric(
        "Favorites",
        len(st.session_state.favorites)
    )

    st.metric(
        "Searches",
        len(st.session_state.history)
    )

    if not st.session_state.results.empty:

        st.metric(
            "Recommendations",
            len(st.session_state.results)
        )

# ------------------------------------------------
# FOOTER
# ------------------------------------------------

render_footer()

# ------------------------------------------------
# VERSION INFORMATION
# ------------------------------------------------

st.markdown(
    """
<div style='text-align:center;
padding:15px;
color:gray;
font-size:14px;'>

AI Smart Recommendation Hub

Version 1.0.0

Built with ❤️ using Streamlit, Pandas,
Scikit-Learn and Plotly

</div>
""",
    unsafe_allow_html=True
)

# ------------------------------------------------
# DEBUG INFORMATION
# ------------------------------------------------

with st.expander("⚙ Debug Information"):

    st.write("Current Theme:", st.session_state.theme)

    st.write(
        "Favorites:",
        len(st.session_state.favorites)
    )

    st.write(
        "History:",
        len(st.session_state.history)
    )

    if not st.session_state.results.empty:

        st.write(
            "Recommendation Count:",
            len(st.session_state.results)
        )

        st.write(
            st.session_state.results.head()
        )

# ------------------------------------------------
# END OF APPLICATION
# ------------------------------------------------
=======

>>>>>>> 0b900ebd19f3b23c1af6f8063cd9f7098feb507b
