import random
import pandas as pd
from datetime import datetime


# ----------------------------------------
# Clean Text
# ----------------------------------------

def clean_text(text):

    if pd.isna(text):
        return ""

    text = str(text)

    text = text.strip()

    text = text.replace("\n", " ")

    text = text.replace("\t", " ")

    return text


# ----------------------------------------
# Format Rating
# ----------------------------------------

def format_rating(rating):

    try:

        return f"{float(rating):.1f}/10 ⭐"

    except:

        return "N/A"


# ----------------------------------------
# Current Date & Time
# ----------------------------------------

def current_datetime():

    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


# ----------------------------------------
# Random Recommendation
# ----------------------------------------

def random_recommendation(df):

    if len(df) == 0:

        return None

    return df.sample(1).iloc[0]

# ----------------------------------------
# Export Recommendations
# ----------------------------------------

def export_csv(df, filename="recommendations.csv"):

    df.to_csv(
        filename,
        index=False
    )

    return filename


# ----------------------------------------
# Search Suggestions
# ----------------------------------------

def search_suggestions():

    return [

        "Science Fiction Movies",

        "Romantic Books",

        "Python Course",

        "Healthy Breakfast",

        "Weight Loss Workout",

        "Italian Recipes",

        "Artificial Intelligence",

        "Machine Learning",

        "Career Guidance",

        "Jazz Music"

    ]


# ----------------------------------------
# Dataset Summary
# ----------------------------------------

def dataset_summary(df):

    return {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Missing Values":

            int(df.isnull().sum().sum())

    }


# ----------------------------------------
# Greeting Message
# ----------------------------------------

def greeting():

    hour = datetime.now().hour

    if hour < 12:

        return "Good Morning ☀"

    elif hour < 17:

        return "Good Afternoon 🌤"

    else:

        return "Good Evening 🌙"


# ----------------------------------------
# Welcome Message
# ----------------------------------------

def welcome():

    return (
        "Welcome to AI Smart Recommendation Hub! "
        "Discover personalized recommendations "
        "across Movies, Books, Music, Food, "
        "Fitness, Courses, Recipes, and Careers."
    )