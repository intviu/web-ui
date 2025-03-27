"""
Health check routes for the API.
"""
import logging
from fastapi import APIRouter, Request, HTTPException

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    tags=["health"],
    responses={404: {"description": "Not found"}},
)

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        logger.info("Health check requested")
        return {
            "status": "healthy",
            "version": "0.1.0"
        }
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return {"status": "error", "error": str(e)} 