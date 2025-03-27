from fastapi import FastAPI
import uvicorn
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Health Check API")

@app.get("/")
async def root():
    """Root endpoint."""
    logger.info("Root endpoint requested")
    return {"message": "Health Check API"}

@app.get("/health")
async def health():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {"status": "healthy"}

@app.get("/api/health")
async def api_health():
    """API health check endpoint."""
    logger.info("API health check requested")
    return {"status": "healthy", "path": "api/health"}

if __name__ == "__main__":
    logger.info("Starting health check server on port 8002")
    uvicorn.run(app, host="0.0.0.0", port=8002) 