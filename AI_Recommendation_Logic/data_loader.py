import pandas as pd
from pathlib import Path

# ------------------------------------------------
# DATA DIRECTORY
# ------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# ------------------------------------------------
# DATASET PATHS
# ------------------------------------------------

DATASETS = {

    "🎬 Movies": DATA_DIR / "movies.csv",

    "📚 Books": DATA_DIR / "books.csv",

    "🎵 Music": DATA_DIR / "music.csv",

    "🍔 Food": DATA_DIR / "food.csv",

    "🏋 Fitness": DATA_DIR / "fitness.csv",

    "💻 Courses": DATA_DIR / "courses.csv",

    "👨‍🍳 Recipes": DATA_DIR / "recipes.csv",

    "💼 Careers": DATA_DIR / "careers.csv"

}

# ------------------------------------------------
# REQUIRED COLUMNS
# ------------------------------------------------

REQUIRED_COLUMNS = [

    "title",

    "category",

    "description",

    "rating"

]

# ------------------------------------------------
# VALIDATE DATASET
# ------------------------------------------------

def validate_dataset(df):

    for column in REQUIRED_COLUMNS:

        if column not in df.columns:

            raise ValueError(
                f"Missing required column: {column}"
            )

    return True

# ------------------------------------------------
# LOAD DATASET
# ------------------------------------------------

def load_dataset(category):

    if category not in DATASETS:

        raise ValueError(
            f"Unknown category: {category}"
        )

    path = DATASETS[category]

    df = pd.read_csv(path)

    validate_dataset(df)

    df.fillna("", inplace=True)

    return df

    # ------------------------------------------------
# DATASET STATISTICS
# ------------------------------------------------

def dataset_statistics():

    stats = {}

    for category, path in DATASETS.items():

        try:

            df = pd.read_csv(path)

            stats[category] = {

                "items": len(df),

                "columns": len(df.columns)

            }

        except Exception:

            stats[category] = {

                "items": 0,

                "columns": 0

            }

    return stats

# ------------------------------------------------
# SEARCH DATASET
# ------------------------------------------------

def search_dataset(df, keyword):

    keyword = keyword.lower()

    mask = (

        df["title"].str.lower().str.contains(keyword)

        |

        df["description"].str.lower().str.contains(keyword)

        |

        df["category"].str.lower().str.contains(keyword)

    )

    return df[mask]

# ------------------------------------------------
# TOP RATED
# ------------------------------------------------

def top_rated(df, limit=10):

    if "rating" not in df.columns:

        return df

    return df.sort_values(

        by="rating",

        ascending=False

    ).head(limit)

# ------------------------------------------------
# RANDOM ITEMS
# ------------------------------------------------

def random_items(df, limit=5):

    return df.sample(

        min(limit, len(df))

    )

# ------------------------------------------------
# GET CATEGORY LIST
# ------------------------------------------------

def get_categories():

    return list(DATASETS.keys())