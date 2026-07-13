import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationEngine:

    def __init__(self):

        self.vectorizer = TfidfVectorizer(

            stop_words="english",

            max_features=5000,

            ngram_range=(1,2)

        )

    # ---------------------------------------
    # Prepare Dataset
    # ---------------------------------------

    def prepare(self, dataframe):

        dataframe = dataframe.copy()

        dataframe.fillna("", inplace=True)

        dataframe["combined"] = (

            dataframe["title"].astype(str)

            + " "

            + dataframe["category"].astype(str)

            + " "

            + dataframe["description"].astype(str)

        )

        return dataframe

    # ---------------------------------------
    # Generate Recommendations
    # ---------------------------------------

    def recommend(

        self,

        dataframe,

        query,

        top_n=10

    ):

        dataframe = self.prepare(dataframe)

        documents = dataframe["combined"].tolist()

        documents.append(query)

        vectors = self.vectorizer.fit_transform(documents)

        similarities = cosine_similarity(

            vectors[-1],

            vectors[:-1]

        ).flatten()

        dataframe["match_score"] = similarities

        dataframe = dataframe.sort_values(

            by="match_score",

            ascending=False

        )

        return dataframe.head(top_n)
    
        # ---------------------------------------
    # Similar Items
    # ---------------------------------------

    def similar_items(

        self,

        dataframe,

        title,

        top_n=5

    ):

        dataframe = self.prepare(dataframe)

        tfidf = self.vectorizer.fit_transform(

            dataframe["combined"]

        )

        similarity = cosine_similarity(tfidf)

        titles = dataframe["title"].tolist()

        if title not in titles:

            return pd.DataFrame()

        index = titles.index(title)

        scores = list(

            enumerate(similarity[index])

        )

        scores = sorted(

            scores,

            key=lambda x: x[1],

            reverse=True

        )[1:top_n+1]

        indices = [

            item[0]

            for item in scores

        ]

        result = dataframe.iloc[indices].copy()

        result["match_score"] = [

            score[1]

            for score in scores

        ]

        return result

    # ---------------------------------------
    # Search
    # ---------------------------------------

    def keyword_search(

        self,

        dataframe,

        keyword

    ):

        keyword = keyword.lower()

        mask = (

            dataframe["title"]

            .str.lower()

            .str.contains(keyword)

            |

            dataframe["description"]

            .str.lower()

            .str.contains(keyword)

            |

            dataframe["category"]

            .str.lower()

            .str.contains(keyword)

        )

        return dataframe[mask]

    # ---------------------------------------
    # Trending
    # ---------------------------------------

    def trending(

        self,

        dataframe,

        limit=10

    ):

        if "rating" not in dataframe.columns:

            return dataframe.head(limit)

        return dataframe.sort_values(

            by="rating",

            ascending=False

        ).head(limit)

    # ---------------------------------------
    # Surprise Me
    # ---------------------------------------

    def surprise(

        self,

        dataframe

    ):

        return dataframe.sample(1)