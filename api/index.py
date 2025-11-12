"""
Vercel serverless function entry point for Business Analysis API.
This file imports the FastAPI app from app.main for Vercel deployment.
"""
from app.main import app

# Vercel will use this app instance
__all__ = ["app"]


