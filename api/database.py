"""
Database operations for the API server.
"""
import logging
import json
from typing import Dict, Any, Optional
import asyncpg
from .config import DATABASE_URL, DEV_MODE

# Setup logging
logger = logging.getLogger(__name__)

# Global connection pool
pool = None

# Mock database for development mode
mock_users = {}
mock_credentials = {}

async def init_db():
    """Initialize the database connection pool and create tables if they don't exist."""
    global pool
    
    if DEV_MODE:
        logger.info("Development mode: using mock database")
        return
    
    try:
        # Create connection pool
        pool = await asyncpg.create_pool(DATABASE_URL)
        logger.info("Connected to PostgreSQL database")
        
        # Create tables if they don't exist
        async with pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    name TEXT,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS credentials (
                    email TEXT PRIMARY KEY REFERENCES users(email) ON DELETE CASCADE,
                    token JSONB NOT NULL,
                    scopes TEXT[] NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
        logger.info("Database tables created if they didn't exist")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise

async def get_user(email: str) -> Optional[Dict[str, Any]]:
    """Get a user by email."""
    if DEV_MODE:
        return mock_users.get(email)
    
    if not pool:
        logger.error("Database not initialized")
        raise RuntimeError("Database not initialized")
    
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT email, name, created_at FROM users WHERE email = $1",
            email
        )
        
        if row:
            return dict(row)
        return None

async def save_user(email: str, name: str) -> bool:
    """Save or update a user."""
    if DEV_MODE:
        mock_users[email] = {
            "email": email,
            "name": name,
            "created_at": "mock_timestamp"
        }
        return True
    
    if not pool:
        logger.error("Database not initialized")
        raise RuntimeError("Database not initialized")
    
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO users (email, name) 
                VALUES ($1, $2)
                ON CONFLICT (email) 
                DO UPDATE SET name = $2
                """,
                email, name
            )
            return True
    except Exception as e:
        logger.error(f"Error saving user: {str(e)}")
        return False

async def save_credentials(email: str, credentials: Dict[str, Any], scopes: list) -> bool:
    """Save or update OAuth credentials for a user."""
    if DEV_MODE:
        mock_credentials[email] = {
            "token": credentials,
            "scopes": scopes
        }
        return True
    
    if not pool:
        logger.error("Database not initialized")
        raise RuntimeError("Database not initialized")
    
    try:
        # First ensure user exists
        user = await get_user(email)
        if not user:
            await save_user(email, email.split('@')[0])  # Use part before @ as name
        
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO credentials (email, token, scopes, updated_at) 
                VALUES ($1, $2, $3, CURRENT_TIMESTAMP)
                ON CONFLICT (email) 
                DO UPDATE SET 
                    token = $2,
                    scopes = $3,
                    updated_at = CURRENT_TIMESTAMP
                """,
                email, json.dumps(credentials), scopes
            )
            return True
    except Exception as e:
        logger.error(f"Error saving credentials: {str(e)}")
        return False

async def get_user_credentials(email: str) -> Optional[Dict[str, Any]]:
    """Get OAuth credentials for a user."""
    if DEV_MODE:
        if email in mock_credentials:
            return mock_credentials[email]["token"]
        return None
    
    if not pool:
        logger.error("Database not initialized")
        raise RuntimeError("Database not initialized")
    
    try:
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT token, scopes FROM credentials WHERE email = $1",
                email
            )
            
            if not row:
                return None
                
            # Convert token from JSON string to dictionary
            token = json.loads(row['token'])
            return token
    except Exception as e:
        logger.error(f"Error getting credentials: {str(e)}")
        return None

async def delete_user_credentials(email: str) -> bool:
    """Delete a user's credentials."""
    if DEV_MODE:
        if email in mock_credentials:
            del mock_credentials[email]
        return True
    
    if not pool:
        logger.error("Database not initialized")
        raise RuntimeError("Database not initialized")
    
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM credentials WHERE email = $1",
                email
            )
            return True
    except Exception as e:
        logger.error(f"Error deleting credentials: {str(e)}")
        return False 