import mysql.connector

# Change this password to your own MySQL password before running the app.
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "YOUR PASSWORD",
    "database": "student_management_db",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
