import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "admin")
    DB_PASSWORD = os.getenv("DB_PASSWORD") # Will fail if not set

    # Application Secret Key
    SECRET_KEY = os.getenv("APP_SECRET_KEY")

    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")