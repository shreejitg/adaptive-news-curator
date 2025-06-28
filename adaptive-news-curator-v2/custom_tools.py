# file: custom_tools.py
import sqlite3
from langchain.tools import tool

def _get_db_connection():
    """Helper function to connect to the database."""
    return sqlite3.connect('news_curator.db')

@tool
def read_past_feedback(limit: int = 10) -> str:
    """
    Reads the most recent 'liked' and 'disliked' article summaries from the database
    to understand the user's preferences. Returns a summary of preferences.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    
    # Get liked articles
    cursor.execute("SELECT summary FROM news_feedback WHERE rating = 1 ORDER BY timestamp DESC LIMIT ?", (limit,))
    liked_summaries = [row[0] for row in cursor.fetchall()]
    
    # Get disliked articles
    cursor.execute("SELECT summary FROM news_feedback WHERE rating = -1 ORDER BY timestamp DESC LIMIT ?", (limit,))
    disliked_summaries = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    if not liked_summaries and not disliked_summaries:
        return "No feedback history found. The user is interested in 'breakthroughs in artificial intelligence'."

    return f"""
    User's Liked Articles (summaries):
    {liked_summaries}

    User's Disliked Articles (summaries):
    {disliked_summaries}
    """

@tool
def get_previously_recommended_urls() -> list[str]:
    """
    Gets the URLs of all articles that have already been recommended to the user
    to avoid showing the same article twice.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM news_feedback")
    urls = [row[0] for row in cursor.fetchall()]
    conn.close()
    return urls

def save_feedback_to_db(title: str, url: str, summary: str, rating: int):
    """A helper function to be used outside the agent, to save the final feedback."""
    conn = _get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO news_feedback (title, url, summary, rating) VALUES (?, ?, ?, ?)",
            (title, url, summary, rating)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # This can happen if the agent finds the same URL twice in a rare case.
        print(f"URL already exists: {url}")
    finally:
        conn.close()