"""
Market comparison endpoint router.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from app.models.business_metrics import BusinessMetrics, MarketType
from app.services.metrics_calculator import MetricsCalculator
from app.services.benchmark_service import BenchmarkService
from app.utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/compare-markets", tags=["Market Comparison"])


def get_market_summary(market: MarketType) -> dict:
    """Provide market-specific context and summary."""
    summaries = {
        "argentina": {
            "inflation_rate": "High (100%+ historically)",
            "ecommerce_growth": "14% annually",
            "key_challenges": ["Currency volatility", "Import restrictions", "High inflation"],
            "opportunities": ["Growing fintech adoption", "18% of retail is online", "Large market size"],
        },
        "brazil": {
            "inflation_rate": "Moderate (4-6%)",
            "ecommerce_growth": "15-20% annually",
            "key_challenges": ["Complex tax system", "Logistics infrastructure", "Currency fluctuations"],
            "opportunities": ["Largest LATAM market", "Strong digital payment adoption", "Growing middle class"],
        },
        "chile": {
            "inflation_rate": "Low to moderate (3-5%)",
            "ecommerce_growth": "12% annually",
            "key_challenges": ["Smaller market size", "Mature competition", "Higher costs"],
            "opportunities": ["Most stable LATAM economy", "High internet penetration", "Strong purchasing power"],
        },
        "usa": {
            "inflation_rate": "Low to moderate (2-4%)",
            "ecommerce_growth": "8-10% annually",
            "key_challenges": ["Saturated markets", "High CAC", "Intense competition"],
            "opportunities": ["Large market", "Strong infrastructure", "High purchasing power"],
        },
    }
    return summaries.get(market.value, {})


@router.post("")
async def compare_markets(
    base_metrics: BusinessMetrics,
    target_markets: List[MarketType]
):
    """
    Compare how the same business would be benchmarked in different markets.
    
    Args:
        base_metrics: Base business metrics
        target_markets: List of markets to compare against
        
    Returns:
        Comparison results for each target market
    """
    try:
        logger.info(f"Comparing business across {len(target_markets)} markets")
        
        # Calculate base metrics
        base_metrics_calc = MetricsCalculator.calculate(base_metrics)
        
        results = {}
        
        for market in target_markets:
            # Compare against market-specific benchmarks
            comparisons = BenchmarkService.compare_metrics(
                base_metrics_calc,
                base_metrics.industry,
                market
            )
            
            results[market.value] = {
                "benchmarks": {
                    key: {
                        "status": comp.status,
                        "message": comp.message,
                        "your_value": comp.your_value,
                        "benchmark_good": comp.benchmark_good,
                        "benchmark_acceptable": comp.benchmark_acceptable,
                    }
                    for key, comp in comparisons.items()
                },
                "market_summary": get_market_summary(market),
            }
        
        return {
            "base_market": base_metrics.market.value,
            "base_metrics": base_metrics_calc,
            "comparisons": results,
        }
        
    except ValueError as e:
        logger.error(f"Validation error in market comparison: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in market comparison: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during market comparison"
        )






