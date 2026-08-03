from pathlib import Path
import sqlite3


# ==========================================================
# Database Location
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "sms_history.db"


# ==========================================================
# Database Connection
# ==========================================================

def get_connection():
    """
    Create and return a SQLite connection.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================================
# Initialize Database
# ==========================================================

def initialize_database():
    """
    Create prediction history table if it does not exist.
    """

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prediction_history (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                message TEXT NOT NULL,

                prediction TEXT NOT NULL,

                confidence REAL NOT NULL,

                spam_probability REAL NOT NULL,

                ham_probability REAL NOT NULL,

                risk TEXT NOT NULL,

                keywords TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_prediction
            ON prediction_history(prediction)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at
            ON prediction_history(created_at)
        """)

        connection.commit()


# ==========================================================
# Save Prediction
# ==========================================================

def save_prediction(
    message,
    prediction,
    confidence,
    spam_probability,
    ham_probability,
    risk,
    keywords
):
    """
    Save prediction into SQLite database.
    """

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO prediction_history (

                message,
                prediction,
                confidence,
                spam_probability,
                ham_probability,
                risk,
                keywords

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                message,
                prediction,
                confidence,
                spam_probability,
                ham_probability,
                risk,
                ", ".join(keywords) if isinstance(keywords, list) else str(keywords)
            )
        )

        connection.commit()


# ==========================================================
# Prediction History
# ==========================================================

def get_history(limit=100):
    """
    Return the latest prediction history.
    """

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT

                id,
                created_at,
                message,
                prediction,
                confidence,
                spam_probability,
                ham_probability,
                risk,
                keywords

            FROM prediction_history

            ORDER BY id DESC

            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        history = []

        for row in rows:

            history.append(dict(row))

        return history


# ==========================================================
# Dashboard Statistics
# ==========================================================

def get_statistics():
    """
    Return dashboard statistics.
    """

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM prediction_history
        """)

        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM prediction_history
            WHERE prediction='Spam'
        """)

        spam = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM prediction_history
            WHERE prediction='Safe'
        """)

        safe = cursor.fetchone()[0]

        return {

            "total_predictions": total,

            "spam_messages": spam,

            "safe_messages": safe

        }


# ==========================================================
# Clear History (Optional)
# ==========================================================

def clear_history():
    """
    Delete all prediction history.
    """

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM prediction_history
        """)

        connection.commit()