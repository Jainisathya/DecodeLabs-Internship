import streamlit as st
from database import add_favorite


def recommendation_card(row):
    """Render a single recommendation result card."""

    title       = row.get("title", "Unknown")
    category    = row.get("category", "")
    description = row.get("description", "")
    rating      = row.get("rating", 0)
    match_score = row.get("match_score", 0)

    rating_str = f"{float(rating):.1f} ⭐" if rating else "N/A"
    score_pct  = f"{float(match_score)*100:.0f}%" if match_score else "0%"

    st.markdown(f"""
<div class="rec-card">
    <div class="rec-header">
        <span class="rec-title">{title}</span>
        <span class="rec-badge">{category}</span>
    </div>
    <p class="rec-desc">{description}</p>
    <div class="rec-meta">
        <span class="rec-rating">⭐ {rating_str}</span>
        <span class="rec-score">🎯 Match: {score_pct}</span>
    </div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("❤️ Save", key=f"fav_{title}_{match_score}",
                     use_container_width=True):
            item = {
                "title":       title,
                "category":    category,
                "description": description,
                "rating":      rating
            }
            if "favorites" not in st.session_state:
                st.session_state.favorites = []

            titles = [f["title"] for f in st.session_state.favorites]
            if title not in titles:
                st.session_state.favorites.append(item)
                try:
                    add_favorite(title, category, description, float(rating))
                except Exception:
                    pass
                st.success(f"✅ '{title}' added to favorites!")
            else:
                st.info(f"'{title}' is already in favorites.")
