from pathlib import Path
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "sms_history.db"


def get_connection():
    """
    Create a SQLite connection.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """
    Create the prediction history table.
    """

    with get_connection() as connection:

        cursor = connection.cursor()

    cursor.execute(
        """
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
        """
    )

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_prediction
    ON prediction_history(prediction)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_created_at
    ON prediction_history(created_at)
    """)

    connection.commit()

    

def save_prediction(result, message):

    with get_connection() as connection:

        cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO prediction_history(

            message,

            prediction,

            confidence,

            spam_probability,

            ham_probability,

            risk,

            keywords

        )

        VALUES(?,?,?,?,?,?,?)

        """,
        (
            message,

            result["prediction"],

            result["confidence"],

            result["spam_probability"],

            result["ham_probability"],

            result["risk"],

            ", ".join(result["keywords"])

        )
    )

    connection.commit()



def get_history(limit=100):

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

    
    return [dict(row) for row in rows]
def get_statistics():

    with get_connection() as connection:

        cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM prediction_history
        """
    )

    total = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS spam
        FROM prediction_history
        WHERE prediction='Spam'
        """
    )

    spam = cursor.fetchone()["spam"]

    cursor.execute(
        """
        SELECT COUNT(*) AS safe
        FROM prediction_history
        WHERE prediction='Safe'
        """
    )

    safe = cursor.fetchone()["safe"]

    connection.close()

    return {

        "total_predictions": total,

        "spam_messages": spam,

        "safe_messages": safe

    }