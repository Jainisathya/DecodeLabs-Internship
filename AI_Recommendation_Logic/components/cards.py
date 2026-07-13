import streamlit as st

CATEGORIES = [
    {"icon": "🎬", "title": "Movies",  "description": "Discover blockbuster movies tailored to your taste."},
    {"icon": "📚", "title": "Books",   "description": "Find your next favourite book from thousands of titles."},
    {"icon": "🎵", "title": "Music",   "description": "Explore songs, albums and playlists you'll love."},
    {"icon": "🍔", "title": "Food",    "description": "Healthy meals and food recommendations."},
    {"icon": "🏋️", "title": "Fitness", "description": "Workout plans and exercise suggestions."},
    {"icon": "💻", "title": "Courses", "description": "Learn new skills and technologies."},
    {"icon": "👨‍🍳","title": "Recipes", "description": "Cook delicious recipes from around the world."},
    {"icon": "💼", "title": "Careers", "description": "Discover career opportunities that suit you."},
]


def render_cards():
    st.markdown('<div class="section-header">🔥 Explore Categories</div>',
                unsafe_allow_html=True)
    cols = st.columns(4)
    for i, item in enumerate(CATEGORIES):
        with cols[i % 4]:
            st.markdown(f"""
<div class="cat-card">
    <span class="cat-icon">{item["icon"]}</span>
    <div class="cat-title">{item["title"]}</div>
    <div class="cat-desc">{item["description"]}</div>
</div>
""", unsafe_allow_html=True)
