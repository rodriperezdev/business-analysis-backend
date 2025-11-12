"""
Main FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import analysis_router, scenario_router, benchmarks_router, market_comparison_router
from app.utils.logging import setup_logging, get_logger

# Setup logging
setup_logging(settings.log_level)
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=settings.cors_origin_regex,  # ✅ ADD THIS LINE
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Include routers
app.include_router(analysis_router)
app.include_router(scenario_router)
app.include_router(benchmarks_router)
app.include_router(market_comparison_router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": settings.api_title,
        "version": settings.api_version,
        "status": "running",
        "docs": "/docs",
    }


@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info(f"{settings.api_title} v{settings.api_version} starting up")
    logger.info(f"Server running on {settings.host}:{settings.port}")


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information."""
    logger.info(f"{settings.api_title} shutting down")

