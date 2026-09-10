import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'emergency.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEMO_MODE = os.environ.get("DEMO_MODE", "True").lower() in {"1", "true", "yes", "on"}
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
    APP_NAME = "AI Emergency Medical Assistance"


config = Config()
