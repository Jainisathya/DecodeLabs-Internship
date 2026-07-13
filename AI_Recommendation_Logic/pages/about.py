import streamlit as st


def show_about():

    st.title("ℹ️ About AI Smart Recommendation Hub")

    st.markdown("""
Welcome to the **AI Smart Recommendation Hub**, an intelligent recommendation platform
designed to help users discover personalized content across multiple domains using
Artificial Intelligence.

The system utilizes Natural Language Processing (NLP) and Machine Learning techniques
to understand user interests and recommend the most relevant content.
""")

    st.divider()

    # ---------------------------------------------
    # Features
    # ---------------------------------------------

    st.subheader("🚀 Features")

    col1, col2 = st.columns(2)

    with col1:

        st.success("🎬 Movie Recommendations")
        st.success("📚 Book Recommendations")
        st.success("🎵 Music Recommendations")
        st.success("🍔 Food Recommendations")
        st.success("🏋️ Fitness Suggestions")

    with col2:

        st.success("💻 Course Recommendations")
        st.success("👨‍🍳 Recipe Suggestions")
        st.success("💼 Career Guidance")
        st.success("📊 Analytics Dashboard")
        st.success("❤️ Favorites & History")

    st.divider()

    # ---------------------------------------------
    # Technology Stack
    # ---------------------------------------------

    st.subheader("🛠️ Technology Stack")

    technologies = [
        "Python",
        "Streamlit",
        "Pandas",
        "Scikit-Learn",
        "Plotly",
        "SQLite",
        "TF-IDF Vectorizer",
        "Cosine Similarity",
        "Git & GitHub"
    ]

    for tech in technologies:
        st.write("✅", tech)

    st.divider()

    # ---------------------------------------------
    # Recommendation Categories
    # ---------------------------------------------

    st.subheader("📂 Supported Categories")

    categories = [
        "🎬 Movies",
        "📚 Books",
        "🎵 Music",
        "🍔 Food",
        "🏋️ Fitness",
        "💻 Courses",
        "👨‍🍳 Recipes",
        "💼 Careers"
    ]

    cols = st.columns(4)

    for i, category in enumerate(categories):

        with cols[i % 4]:
            st.info(category)

    st.divider()

    # ---------------------------------------------
    # AI Recommendation Process
    # ---------------------------------------------

    st.subheader("🤖 How It Works")

    st.markdown("""
1. User selects a category.
2. User enters a search query.
3. Dataset is loaded.
4. Text is converted into TF-IDF vectors.
5. Cosine Similarity calculates similarity scores.
6. Top matching recommendations are displayed.
7. User can save favorites and view analytics.
""")

    st.divider()

    # ---------------------------------------------
    # Future Enhancements
    # ---------------------------------------------

    st.subheader("🚀 Future Enhancements")

    future = [
        "🌐 Multi-language support",
        "🤖 LLM-based recommendations",
        "👤 User Login & Authentication",
        "☁️ Cloud Database",
        "📱 Mobile App",
        "🎙️ Voice Search",
        "🖼️ Image-based Recommendations",
        "🔔 Smart Notifications"
    ]

    for feature in future:
        st.write(feature)

    st.divider()

    # ---------------------------------------------
    # Developer
    # ---------------------------------------------

    st.subheader("👨‍💻 Developer")

    st.info("""
Project: AI Smart Recommendation Hub

Developed using Python and Streamlit

Recommendation Engine:
TF-IDF + Cosine Similarity

Database:
SQLite

Version:
1.0.0
""")

    st.divider()

    st.caption("© 2026 AI Smart Recommendation Hub. All Rights Reserved.")