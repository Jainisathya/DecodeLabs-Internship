import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class Analytics:

    def __init__(self):
        pass

    # ----------------------------------------
    # Rating Distribution
    # ----------------------------------------

    def rating_distribution(self, dataframe):

        if dataframe.empty:
            return None

        if "rating" not in dataframe.columns:
            return None

        fig = px.histogram(
            dataframe,
            x="rating",
            nbins=10,
            title="⭐ Rating Distribution"
        )

        fig.update_layout(
            template="plotly_white",
            height=450
        )

        return fig

    # ----------------------------------------
    # Match Score
    # ----------------------------------------

    def match_score_distribution(self, dataframe):

        if dataframe.empty:
            return None

        if "match_score" not in dataframe.columns:
            return None

        fig = px.histogram(
            dataframe,
            x="match_score",
            nbins=20,
            title="🎯 Match Score Distribution"
        )

        fig.update_layout(
            template="plotly_white",
            height=450
        )

        return fig

    # ----------------------------------------
    # Top Rated
    # ----------------------------------------

    def top_rated_chart(self, dataframe):

        if dataframe.empty:
            return None

        if "rating" not in dataframe.columns:
            return None

        top = dataframe.sort_values(
            "rating",
            ascending=False
        ).head(10)

        fig = px.bar(
            top,
            x="title",
            y="rating",
            color="rating",
            title="🏆 Top Rated Recommendations"
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Title",
            yaxis_title="Rating",
            height=500
        )

        return fig
    
        # ----------------------------------------
    # Category Distribution
    # ----------------------------------------

    def category_distribution(self, dataframe):

        if dataframe.empty:
            return None

        category_count = (
            dataframe["category"]
            .value_counts()
            .reset_index()
        )

        category_count.columns = [
            "Category",
            "Count"
        ]

        fig = px.pie(
            category_count,
            names="Category",
            values="Count",
            hole=0.45,
            title="📂 Category Distribution"
        )

        fig.update_layout(
            template="plotly_white",
            height=500
        )

        return fig

    # ----------------------------------------
    # Dashboard Summary
    # ----------------------------------------

    def summary(self, dataframe):

        if dataframe.empty:

            return {
                "items": 0,
                "average_rating": 0,
                "highest_rating": 0,
                "categories": 0
            }

        return {

            "items": len(dataframe),

            "average_rating":
                round(dataframe["rating"].mean(), 2),

            "highest_rating":
                round(dataframe["rating"].max(), 2),

            "categories":
                dataframe["category"].nunique()

        }

    # ----------------------------------------
    # Dashboard Metrics
    # ----------------------------------------

    def metrics(self, dataframe):

        summary = self.summary(dataframe)

        return [

            ("📚 Total Items",
             summary["items"]),

            ("⭐ Avg Rating",
             summary["average_rating"]),

            ("🏆 Highest Rating",
             summary["highest_rating"]),

            ("📂 Categories",
             summary["categories"])

        ]