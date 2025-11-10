"""
Response models for API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from .business_metrics import IndustryType


class Insight(BaseModel):
    """Actionable insight with recommendations."""
    
    priority: str = Field(
        description="Priority level: critical, high, medium, low",
        examples=["critical"]
    )
    category: str = Field(
        description="Insight category",
        examples=["profitability", "growth", "financial_health", "retention"]
    )
    title: str = Field(
        description="Short title for the insight",
        examples=["Gross Margin Below Target"]
    )
    description: str = Field(
        description="Detailed description of the issue or opportunity"
    )
    recommendations: List[str] = Field(
        description="Actionable recommendations",
        default_factory=list
    )


class MetricComparison(BaseModel):
    """Comparison of a metric against industry benchmarks."""
    
    status: str = Field(
        description="Status: excellent, good, needs_improvement",
        examples=["good"]
    )
    message: str = Field(
        description="Human-readable status message"
    )
    your_value: float = Field(
        description="Your metric value"
    )
    benchmark_good: float = Field(
        description="Industry 'good' benchmark"
    )
    benchmark_acceptable: float = Field(
        description="Industry 'acceptable' benchmark"
    )


class CurrencyInfo(BaseModel):
    """Currency conversion information."""
    
    input_currency: str = Field(
        description="Currency used for input (e.g., BRL, ARS)"
    )
    benchmark_currency: str = Field(
        default="USD",
        description="Currency used for benchmarking (always USD)"
    )
    exchange_rate: float = Field(
        description="Exchange rate used for conversion"
    )
    rate_date: Optional[str] = Field(
        default=None,
        description="Date when exchange rate was fetched"
    )
    note: Optional[str] = Field(
        default=None,
        description="Human-readable note about conversion"
    )


class AnalysisResponse(BaseModel):
    """Response from the main analysis endpoint."""
    
    metrics: Dict[str, float] = Field(
        description="Calculated financial and operational metrics in USD"
    )
    metrics_local: Optional[Dict[str, float]] = Field(
        default=None,
        description="Calculated metrics in original input currency"
    )
    benchmarks: Dict[str, MetricComparison] = Field(
        description="Comparison against industry benchmarks"
    )
    insights: List[Insight] = Field(
        description="Actionable insights and recommendations",
        default_factory=list
    )
    industry: IndustryType = Field(
        description="Industry type used for benchmarking"
    )
    market: Optional[str] = Field(
        default=None,
        description="Market used for benchmarking"
    )
    currency_info: Optional[CurrencyInfo] = Field(
        default=None,
        description="Currency conversion information"
    )


class ScenarioResponse(BaseModel):
    """Response from scenario analysis endpoint."""
    
    base_metrics: Dict[str, float] = Field(
        description="Original metrics before changes"
    )
    new_metrics: Dict[str, float] = Field(
        description="Metrics after applying changes"
    )
    changes_applied: Dict[str, float] = Field(
        description="Percentage changes that were applied"
    )
    impact: Dict[str, Dict[str, float]] = Field(
        description="Impact of changes (absolute and percentage deltas)"
    )


class BenchmarkResponse(BaseModel):
    """Response from benchmark endpoint."""
    
    industry: IndustryType = Field(
        description="Industry type"
    )
    benchmarks: Dict[str, Dict[str, float]] = Field(
        description="Industry benchmark values"
    )

