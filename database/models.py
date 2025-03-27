"""
Database models for the web-ui application.
"""
import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ARRAY, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class GoogleCredentials(Base):
    """Model for storing Google OAuth credentials."""
    
    __tablename__ = "google_credentials"
    
    id = Column(Integer, primary_key=True)
    user_email = Column(String, unique=True, nullable=False)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=False)
    token_uri = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
    scopes = Column(ARRAY(String), nullable=False)
    token_expiry = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "user_email": self.user_email,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "token_uri": self.token_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scopes": self.scopes,
            "token_expiry": self.token_expiry.isoformat() if self.token_expiry else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_credentials(cls, user_email, credentials):
        """Create a model instance from Google credentials object."""
        return cls(
            user_email=user_email,
            access_token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            scopes=credentials.scopes,
            token_expiry=credentials.expiry
        )

def get_db_engine():
    """Get the SQLAlchemy engine."""
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/vbm")
    return create_engine(db_url)

def get_db_session():
    """Get a new database session."""
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def init_db():
    """Initialize the database by creating all tables."""
    engine = get_db_engine()
    Base.metadata.create_all(engine) 