import logging
import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from .routes import health, email, auth, calendar
from .config import SESSION_SECRET, CORS_ORIGINS, DEV_MODE

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Virtual Business Manager API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
app.add_middleware(
    SessionMiddleware, 
    secret_key=SESSION_SECRET,
    session_cookie="vbm_session",
    max_age=30 * 24 * 60 * 60,  # 30 days in seconds
)

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    if not DEV_MODE:
        from .database import init_db
        await init_db()
        logger.info("Database initialized successfully")
    else:
        logger.info("Running in development mode - skipping database initialization")
    
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")

# Include routers with prefix
app.include_router(health.router, prefix="/api")
app.include_router(email.router)
app.include_router(auth.router)
app.include_router(calendar.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Virtual Business Manager API"}

@app.get("/api/healthcheck")
async def healthcheck():
    """Direct health check endpoint."""
    try:
        logger.info("Health check requested via direct endpoint")
        return {"status": "healthy", "direct": True}
    except Exception as e:
        logger.error(f"Error in direct health check: {str(e)}")
        return {"status": "error", "error": str(e)} 