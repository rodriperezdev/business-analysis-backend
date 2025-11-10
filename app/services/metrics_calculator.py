"""
Service for calculating business metrics.
"""

from typing import Dict
from app.models.business_metrics import BusinessMetrics
from app.utils.logging import get_logger

logger = get_logger(__name__)


class MetricsCalculator:
    """Calculate financial and operational metrics from business data."""
    
    @staticmethod
    def calculate(data: BusinessMetrics) -> Dict[str, float]:
        """
        Calculate all financial and operational metrics.
        
        Args:
            data: Business metrics input
            
        Returns:
            Dictionary of calculated metrics
        """
        logger.debug(f"Calculating metrics for {data.industry} industry")
        
        # Basic financial metrics
        gross_profit = data.revenue - data.cogs
        gross_margin = (gross_profit / data.revenue * 100) if data.revenue > 0 else 0.0
        
        net_profit = gross_profit - data.operating_expenses
        net_margin = (net_profit / data.revenue * 100) if data.revenue > 0 else 0.0
        
        ebitda = net_profit  # Simplified - could be enhanced
        ebitda_margin = (ebitda / data.revenue * 100) if data.revenue > 0 else 0.0
        
        metrics: Dict[str, float] = {
            "gross_profit": round(gross_profit, 2),
            "gross_margin": round(gross_margin, 2),
            "net_profit": round(net_profit, 2),
            "net_margin": round(net_margin, 2),
            "ebitda": round(ebitda, 2),
            "ebitda_margin": round(ebitda_margin, 2),
        }
        
        # Customer economics
        metrics.update(MetricsCalculator._calculate_customer_metrics(data, gross_margin))
        
        # Churn metrics
        if data.churned_customers is not None and data.total_customers:
            churn_rate = (data.churned_customers / data.total_customers * 100)
            metrics["churn_rate"] = round(churn_rate, 2)
        
        # Cash metrics
        if data.cash_balance is not None and data.monthly_burn is not None:
            metrics.update(MetricsCalculator._calculate_cash_metrics(data))
        
        logger.debug(f"Calculated {len(metrics)} metrics")
        return metrics
    
    @staticmethod
    def _calculate_customer_metrics(
        data: BusinessMetrics,
        gross_margin: float
    ) -> Dict[str, float]:
        """Calculate customer acquisition and lifetime value metrics."""
        metrics: Dict[str, float] = {}
        
        if data.new_customers and data.new_customers > 0:
            cac = data.sales_marketing_expense / data.new_customers
            metrics["cac"] = round(cac, 2)
            
            # Estimate LTV (simplified - assumes 3 year lifetime)
            if data.total_customers and data.total_customers > 0:
                monthly_revenue_per_customer = (
                    (data.revenue / data.time_period_months) / data.total_customers
                )
                avg_lifetime_months = 36
                ltv = (
                    monthly_revenue_per_customer 
                    * avg_lifetime_months 
                    * (gross_margin / 100)
                )
                metrics["ltv"] = round(ltv, 2)
                
                if cac > 0:
                    metrics["ltv_cac_ratio"] = round(ltv / cac, 2)
                else:
                    metrics["ltv_cac_ratio"] = 0.0
                
                # CAC payback period in months
                gross_margin_decimal = gross_margin / 100
                if monthly_revenue_per_customer > 0 and gross_margin_decimal > 0:
                    cac_payback = cac / (monthly_revenue_per_customer * gross_margin_decimal)
                    metrics["cac_payback_months"] = round(cac_payback, 1)
                else:
                    metrics["cac_payback_months"] = 0.0
        
        return metrics
    
    @staticmethod
    def _calculate_cash_metrics(data: BusinessMetrics) -> Dict[str, float]:
        """Calculate cash runway and burn metrics."""
        metrics: Dict[str, float] = {}
        
        if data.monthly_burn and data.monthly_burn > 0:
            if data.cash_balance is not None:
                runway_months = data.cash_balance / data.monthly_burn
                metrics["runway_months"] = round(runway_months, 1)
            
            # Burn multiple (burn rate / revenue)
            monthly_revenue = data.revenue / data.time_period_months
            if monthly_revenue > 0:
                burn_multiple = data.monthly_burn / monthly_revenue
                metrics["burn_multiple"] = round(burn_multiple, 2)
            else:
                metrics["burn_multiple"] = 0.0
        
        return metrics

