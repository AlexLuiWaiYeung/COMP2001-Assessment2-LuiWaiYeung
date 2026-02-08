import os

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Database configuration
    DB_SERVER = os.getenv('DB_SERVER', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'TrailService')
    DB_USER = os.getenv('DB_USER', 'sa')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Authentication
    AUTH_API_URL = os.getenv('AUTH_API_URL')
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """Build database connection string"""
        return f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}/{self.DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"