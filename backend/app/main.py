"""
FastAPI application entry point.

This starts the web server that the frontend will connect to.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes

app = FastAPI(
    title="Gross Financial Analysis API",
    description="API for analyzing financial ratios from multiple sources",
    version="0.1.0"
)

# Configure CORS - Allow frontend to connect
# Frontend runs on port 3001, backend on port 8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "*"],  # Allow frontend ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(routes.router, prefix="/api", tags=["analysis"])


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Gross Financial Analysis API",
        "docs": "/docs",
        "health": "/api/health"
    }

