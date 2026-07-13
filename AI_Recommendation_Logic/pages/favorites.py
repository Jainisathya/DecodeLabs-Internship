import streamlit as st
from database import get_favorites, delete_favorite, clear_favorites


def show_favorites():
    st.markdown('<div class="section-header">❤️ My Favorites</div>',
                unsafe_allow_html=True)

    if "favorites" not in st.session_state:
        st.session_state.favorites = []

    # Sync from DB on first load
    if len(st.session_state.favorites) == 0:
        try:
            rows = get_favorites()
            for r in rows:
                st.session_state.favorites.append({
                    "id": r[0], "title": r[1], "category": r[2],
                    "description": r[3], "rating": r[4]
                })
        except Exception:
            pass

    if len(st.session_state.favorites) == 0:
        st.info("No favorites yet. Go to Dashboard and save recommendations you like!")
        return

    st.markdown(f"**{len(st.session_state.favorites)} saved items**")
    st.divider()

    to_remove = None

    for i, item in enumerate(st.session_state.favorites):
        title       = item.get("title", "Unknown")
        category    = item.get("category", "")
        description = item.get("description", "")
        rating      = item.get("rating", 0)

        st.markdown(f"""
<div class="rec-card">
    <div class="rec-header">
        <span class="rec-title">{title}</span>
        <span class="rec-badge">{category}</span>
    </div>
    <p class="rec-desc">{description}</p>
    <div class="rec-meta">
        <span class="rec-rating">⭐ {float(rating):.1f}/10</span>
    </div>
</div>
""", unsafe_allow_html=True)

        if st.button(f"🗑 Remove", key=f"remove_fav_{i}_{title}"):
            to_remove = i
            try:
                if "id" in item:
                    delete_favorite(item["id"])
            except Exception:
                pass

    if to_remove is not None:
        st.session_state.favorites.pop(to_remove)
        st.rerun()

    st.divider()
    if st.button("🗑 Clear All Favorites", use_container_width=True):
        st.session_state.favorites = []
        try:
            clear_favorites()
        except Exception:
            pass
        st.success("All favorites cleared.")
        st.rerun()
