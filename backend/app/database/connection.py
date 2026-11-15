from sqlalchemy import text

from app.database.database import engine


def test_database_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except Exception as error:
        print(f"Database connection failed: {error}")
        return False