import sqlite3
from pathlib import Path

# ----------------------------------------
# Database Path
# ----------------------------------------

DB_FOLDER = Path("database")
DB_FOLDER.mkdir(exist_ok=True)

DB_PATH = DB_FOLDER / "recommendation.db"

# ----------------------------------------
# Database Connection
# ----------------------------------------

def connect():

    return sqlite3.connect(DB_PATH)


# ----------------------------------------
# Create Tables
# ----------------------------------------

def initialize_database():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS favorites(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        category TEXT,

        description TEXT,

        rating REAL,

        added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS search_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        category TEXT,

        query TEXT,

        searched_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS analytics(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        category TEXT,

        recommendation TEXT,

        score REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    conn.close()

    # ----------------------------------------
# Favorites
# ----------------------------------------

def add_favorite(
    title,
    category,
    description,
    rating
):

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO favorites(

        title,

        category,

        description,

        rating

    )

    VALUES(?,?,?,?)

    """,

    (

        title,

        category,

        description,

        rating

    ))

    conn.commit()

    conn.close()


def get_favorites():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM favorites

    ORDER BY added_on DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_favorite(item_id):

    conn = connect()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM favorites WHERE id=?",

        (item_id,)

    )

    conn.commit()

    conn.close()


def clear_favorites():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM favorites"

    )

    conn.commit()

    conn.close()

    # ----------------------------------------
# Search History
# ----------------------------------------

def add_history(

    category,

    query

):

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO search_history(

        category,

        query

    )

    VALUES(

        ?,?

    )

    """,

    (

        category,

        query

    ))

    conn.commit()

    conn.close()


def get_history():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM search_history

    ORDER BY searched_on DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def clear_history():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM search_history"

    )

    conn.commit()

    conn.close()


# ----------------------------------------
# Analytics
# ----------------------------------------

def add_analytics(

    category,

    recommendation,

    score

):

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO analytics(

        category,

        recommendation,

        score

    )

    VALUES(

        ?,?,?

    )

    """,

    (

        category,

        recommendation,

        score

    ))

    conn.commit()

    conn.close()


def analytics_count():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT COUNT(*) FROM analytics"

    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


# ----------------------------------------
# Initialize Automatically
# ----------------------------------------

initialize_database()