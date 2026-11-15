from app.database.connection import test_database_connection


if test_database_connection():
    print("Database connected successfully!")
else:
    print("Database connection unsuccessful!")