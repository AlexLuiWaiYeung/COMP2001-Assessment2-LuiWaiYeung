import pyodbc
from flask import g, current_app
import os


def get_db():
    """
    Get a database connection for the current request
    """
    if 'db' not in g:
        try:
            # Connection string for university SQL Server
            connection_string = (
                "DRIVER={ODBC Driver 18 for SQL Server};"
                "SERVER=DIST-6-505.uopnet.plymouth.ac.uk;"
                "DATABASE=COMP2001_HK_WLui;"
                "UID=HK_WLui;"
                "PWD=wiHR0U3a;"
                "Encrypt=yes;"
                "TrustServerCertificate=yes;"
                "Connection Timeout=30;"
            )

            print(f"🔗 Connecting to: {current_app.config.get('DB_SERVER')}")
            print(f"📁 Database: {current_app.config.get('DB_NAME')}")

            g.db = pyodbc.connect(connection_string)
            print("✅ Database connection successful!")

        except pyodbc.Error as e:
            print(f"❌ Database connection failed: {e}")
            # Return None instead of raising, so API can handle gracefully
            g.db = None

    return g.db


def close_db(e=None):
    """
    Close the database connection
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    """
    Initialize database for the Flask app
    """
    # Add config from environment variables
    app.config['DB_SERVER'] = os.getenv('DB_SERVER', 'localhost')
    app.config['DB_NAME'] = os.getenv('DB_NAME', 'TrailService')
    app.config['DB_USER'] = os.getenv('DB_USER', 'sa')
    app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD', '')

    # Register teardown
    app.teardown_appcontext(close_db)