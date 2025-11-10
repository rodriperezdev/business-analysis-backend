"""
Benchmarks endpoint router.
"""

from fastapi import APIRouter, Query
from app.models.business_metrics import IndustryType, MarketType
from app.models.responses import BenchmarkResponse
from app.services.benchmark_service import BenchmarkService
from app.utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/benchmarks", tags=["Benchmarks"])


@router.get("/{industry}", response_model=BenchmarkResponse)
async def get_benchmarks(
    industry: IndustryType,
    market: MarketType = Query(default=MarketType.USA, description="Market for market-specific benchmarks")
) -> BenchmarkResponse:
    """
    Get industry benchmark data for a specific market.
    
    Args:
        industry: Industry type
        market: Market type (defaults to USA)
        
    Returns:
        Benchmark values for the specified industry and market
    """
    logger.info(f"Fetching benchmarks for {industry.value} industry in {market.value} market")
    
    benchmarks = BenchmarkService.get_benchmarks(industry, market)
    
    return BenchmarkResponse(
        industry=industry,
        benchmarks=benchmarks
    )

