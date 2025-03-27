"""
Configuration for the API server.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Development mode flag
DEV_MODE = os.getenv("DEV_MODE", "True").lower() in ("true", "1", "t")

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/vbm_db")

# Session settings
SESSION_SECRET = os.getenv("SESSION_SECRET", "default_secret_key_for_development_only")

# Google OAuth settings
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/google/callback")

# API Base URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# CORS origins
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
] 