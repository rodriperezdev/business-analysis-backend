"""
Analysis endpoint router.
"""

from fastapi import APIRouter, HTTPException
from app.models.business_metrics import BusinessMetrics
from app.models.responses import AnalysisResponse, CurrencyInfo
from app.services.metrics_calculator import MetricsCalculator
from app.services.benchmark_service import BenchmarkService
from app.services.insight_service import InsightService
from app.services.currency_service import currency_service
from app.utils.logging import get_logger
from datetime import datetime

logger = get_logger(__name__)

router = APIRouter(prefix="/analyze", tags=["Analysis"])


@router.post("", response_model=AnalysisResponse)
async def analyze_business(data: BusinessMetrics) -> AnalysisResponse:
    """
    Main analysis endpoint.
    
    Calculates metrics, compares against industry benchmarks, and generates
    actionable insights. Automatically handles currency conversion if market is specified.
    
    Args:
        data: Business metrics input
        
    Returns:
        Complete analysis with metrics, benchmarks, and insights
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        logger.info(f"Analyzing business metrics for {data.industry.value} industry")
        
        # Handle currency conversion if market is specified
        input_currency = "USD"
        exchange_rate = 1.0
        currency_info = None
        original_data = data
        
        if data.market:
            input_currency = currency_service.get_currency_from_market(data.market.value)
            
            if input_currency != "USD":
                # Get exchange rate
                exchange_rate = await currency_service.get_exchange_rate(input_currency, "USD")
                
                # Convert all financial inputs to USD for benchmarking
                from app.models.business_metrics import BusinessMetrics as BM
                converted_data = BM(
                    revenue=await currency_service.convert_to_usd_async(data.revenue, input_currency),
                    cogs=await currency_service.convert_to_usd_async(data.cogs, input_currency),
                    operating_expenses=await currency_service.convert_to_usd_async(data.operating_expenses, input_currency),
                    sales_marketing_expense=await currency_service.convert_to_usd_async(data.sales_marketing_expense, input_currency),
                    new_customers=data.new_customers,
                    total_customers=data.total_customers,
                    churned_customers=data.churned_customers,
                    cash_balance=await currency_service.convert_to_usd_async(data.cash_balance, input_currency) if data.cash_balance else None,
                    monthly_burn=await currency_service.convert_to_usd_async(data.monthly_burn, input_currency) if data.monthly_burn else None,
                    industry=data.industry,
                    market=data.market,
                    time_period_months=data.time_period_months,
                )
                data = converted_data
                
                # Create currency info
                currency_info = CurrencyInfo(
                    input_currency=input_currency,
                    benchmark_currency="USD",
                    exchange_rate=exchange_rate,
                    rate_date=datetime.now().isoformat(),
                    note=f"Your {input_currency} {original_data.revenue:,.0f} revenue ≈ ${data.revenue:,.0f} USD (at rate {exchange_rate:.4f})"
                )
                
                logger.info(f"Converted {input_currency} to USD using rate {exchange_rate:.4f}")
        
        # Calculate all metrics in USD
        metrics_usd = MetricsCalculator.calculate(data)
        
        # Convert metrics back to original currency for display
        metrics_local = None
        if input_currency != "USD" and currency_info:
            metrics_local = {}
            # Convert absolute values back to local currency
            for key, value in metrics_usd.items():
                if key.endswith("_margin") or key.endswith("_rate") or key.endswith("_ratio") or key.endswith("_multiple"):
                    # Percentages and ratios stay the same
                    metrics_local[key] = value
                elif key.endswith("_months"):
                    # Time periods stay the same
                    metrics_local[key] = value
                else:
                    # Convert absolute values back to local currency
                    metrics_local[key] = await currency_service.convert_from_usd_async(value, input_currency)
        
        # Benchmark against industry and market (always in USD)
        comparisons = BenchmarkService.compare_metrics(metrics_usd, data.industry, data.market)
        
        # Generate insights with market context
        insights = InsightService.generate_insights(metrics_usd, comparisons, data.industry, data.market)
        
        logger.info(f"Analysis complete: {len(metrics_usd)} metrics, {len(insights)} insights")
        
        return AnalysisResponse(
            metrics=metrics_usd,
            metrics_local=metrics_local,
            benchmarks=comparisons,
            insights=insights,
            industry=data.industry,
            market=data.market.value,
            currency_info=currency_info
        )
        
    except ValueError as e:
        logger.error(f"Validation error in analysis: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during analysis")

