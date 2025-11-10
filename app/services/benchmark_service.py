"""
Service for industry benchmarking with market-specific benchmarks.
"""

from typing import Dict, Optional
from app.models.business_metrics import IndustryType, MarketType
from app.models.responses import MetricComparison
from app.utils.logging import get_logger

logger = get_logger(__name__)


# Multi-market benchmarks: market -> industry -> metric -> thresholds
BENCHMARKS: Dict[str, Dict[str, Dict[str, Dict[str, float]]]] = {
    "usa": {
        "saas": {
            "gross_margin": {"good": 75, "acceptable": 65},
            "net_margin": {"good": 20, "acceptable": 10},
            "ltv_cac_ratio": {"good": 4, "acceptable": 3},
            "cac_payback_months": {"good": 12, "acceptable": 18},
            "burn_multiple": {"good": 1.5, "acceptable": 2.0},
        },
        "ecommerce": {
            "gross_margin": {"good": 40, "acceptable": 30},
            "net_margin": {"good": 10, "acceptable": 5},
            "ltv_cac_ratio": {"good": 3, "acceptable": 2},
            "cac_payback_months": {"good": 6, "acceptable": 12},
        },
        "retail": {
            "gross_margin": {"good": 35, "acceptable": 25},
            "net_margin": {"good": 5, "acceptable": 2},
        },
        "manufacturing": {
            "gross_margin": {"good": 30, "acceptable": 20},
            "net_margin": {"good": 8, "acceptable": 4},
        },
        "services": {
            "gross_margin": {"good": 50, "acceptable": 40},
            "net_margin": {"good": 15, "acceptable": 8},
        },
    },
    "argentina": {
        "saas": {
            "gross_margin": {"good": 65, "acceptable": 55},  # Lower due to higher costs
            "net_margin": {"good": 15, "acceptable": 5},
            "ltv_cac_ratio": {"good": 3, "acceptable": 2},
            "cac_payback_months": {"good": 18, "acceptable": 24},  # Longer due to market conditions
        },
        "ecommerce": {
            "gross_margin": {"good": 35, "acceptable": 25},  # Lower than US
            "net_margin": {"good": 8, "acceptable": 3},
            "ltv_cac_ratio": {"good": 2.5, "acceptable": 1.5},
        },
        "retail": {
            "gross_margin": {"good": 30, "acceptable": 20},
            "net_margin": {"good": 4, "acceptable": 1},
        },
        "manufacturing": {
            "gross_margin": {"good": 25, "acceptable": 15},
            "net_margin": {"good": 6, "acceptable": 2},
        },
        "services": {
            "gross_margin": {"good": 45, "acceptable": 35},
            "net_margin": {"good": 12, "acceptable": 5},
        },
    },
    "brazil": {
        "saas": {
            "gross_margin": {"good": 70, "acceptable": 60},
            "net_margin": {"good": 18, "acceptable": 8},
            "ltv_cac_ratio": {"good": 3.5, "acceptable": 2.5},
            "cac_payback_months": {"good": 15, "acceptable": 20},
        },
        "ecommerce": {
            "gross_margin": {"good": 38, "acceptable": 28},
            "net_margin": {"good": 9, "acceptable": 4},
            "ltv_cac_ratio": {"good": 2.8, "acceptable": 2},
        },
        "retail": {
            "gross_margin": {"good": 32, "acceptable": 22},
            "net_margin": {"good": 4, "acceptable": 1},
        },
        "manufacturing": {
            "gross_margin": {"good": 28, "acceptable": 18},
            "net_margin": {"good": 7, "acceptable": 3},
        },
        "services": {
            "gross_margin": {"good": 48, "acceptable": 38},
            "net_margin": {"good": 14, "acceptable": 7},
        },
    },
    "chile": {
        "saas": {
            "gross_margin": {"good": 72, "acceptable": 62},
            "net_margin": {"good": 19, "acceptable": 9},
            "ltv_cac_ratio": {"good": 3.8, "acceptable": 2.8},
            "cac_payback_months": {"good": 14, "acceptable": 18},
        },
        "ecommerce": {
            "gross_margin": {"good": 40, "acceptable": 30},
            "net_margin": {"good": 10, "acceptable": 5},
            "ltv_cac_ratio": {"good": 3, "acceptable": 2.2},
        },
        "retail": {
            "gross_margin": {"good": 33, "acceptable": 23},
            "net_margin": {"good": 5, "acceptable": 2},
        },
        "manufacturing": {
            "gross_margin": {"good": 29, "acceptable": 19},
            "net_margin": {"good": 8, "acceptable": 4},
        },
        "services": {
            "gross_margin": {"good": 49, "acceptable": 39},
            "net_margin": {"good": 15, "acceptable": 8},
        },
    },
}


class BenchmarkService:
    """Service for comparing metrics against market-specific industry benchmarks."""
    
    @staticmethod
    def get_benchmarks(
        industry: IndustryType,
        market: MarketType = MarketType.USA
    ) -> Dict[str, Dict[str, float]]:
        """
        Get benchmark data for an industry in a specific market.
        
        Args:
            industry: Industry type
            market: Market type (defaults to USA)
            
        Returns:
            Dictionary of benchmark metrics
        """
        market_benchmarks = BENCHMARKS.get(market.value, BENCHMARKS["usa"])
        return market_benchmarks.get(industry.value, {})
    
    @staticmethod
    def compare_metrics(
        metrics: Dict[str, float],
        industry: IndustryType,
        market: MarketType = MarketType.USA
    ) -> Dict[str, MetricComparison]:
        """
        Compare calculated metrics against market-specific industry benchmarks.
        
        Args:
            metrics: Calculated metrics
            industry: Industry type for benchmarking
            market: Market type for market-specific benchmarks
            
        Returns:
            Dictionary of metric comparisons
        """
        logger.debug(f"Comparing metrics for {industry.value} industry in {market.value} market")
        
        # Get market-specific benchmarks
        market_benchmarks = BENCHMARKS.get(market.value, BENCHMARKS["usa"])
        benchmarks = market_benchmarks.get(industry.value, {})
        
        comparisons: Dict[str, MetricComparison] = {}
        
        for metric_name, benchmark_data in benchmarks.items():
            if metric_name not in metrics:
                continue
            
            value = metrics[metric_name]
            good_benchmark = benchmark_data["good"]
            acceptable_benchmark = benchmark_data["acceptable"]
            
            # Determine status
            if value >= good_benchmark:
                status = "excellent"
                message = f"Above {market.value.upper()} industry standard"
            elif value >= acceptable_benchmark:
                status = "good"
                message = f"Within acceptable range for {market.value.upper()}"
            else:
                status = "needs_improvement"
                message = f"Below {market.value.upper()} industry standard"
            
            comparisons[metric_name] = MetricComparison(
                status=status,
                message=message,
                your_value=value,
                benchmark_good=good_benchmark,
                benchmark_acceptable=acceptable_benchmark,
            )
        
        logger.debug(f"Compared {len(comparisons)} metrics against {market.value} benchmarks")
        return comparisons

