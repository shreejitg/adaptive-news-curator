# file: database_setup.py
import sqlite3

def setup_database():
    """Creates the database and the feedback table if they don't exist."""
    conn = sqlite3.connect('news_curator.db')
    cursor = conn.cursor()
    
    # Create table to store feedback
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS news_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        summary TEXT NOT NULL,
        rating INTEGER NOT NULL, -- 1 for thumbs up, -1 for thumbs down
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == '__main__':
    setup_database()