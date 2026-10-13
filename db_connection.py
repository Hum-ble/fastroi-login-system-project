"""Database settings are supplied through local environment variables."""
import os
import mysql.connector


def create_connection():
    return mysql.connector.connect(
        host=os.environ.get("FASTROI_DB_HOST", "localhost"),
        user=os.environ.get("FASTROI_DB_USER", "fastroi_app"),
        password=os.environ.get("FASTROI_DB_PASSWORD", ""),
        port=int(os.environ.get("FASTROI_DB_PORT", "3306")),
        database=os.environ.get("FASTROI_DB_NAME", "fastroi_db"),
    )
