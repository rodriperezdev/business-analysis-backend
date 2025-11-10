"""
API route handlers.
"""

from .analysis import router as analysis_router
from .scenario import router as scenario_router
from .benchmarks import router as benchmarks_router
from .market_comparison import router as market_comparison_router

__all__ = [
    "analysis_router",
    "scenario_router",
    "benchmarks_router",
    "market_comparison_router",
]

