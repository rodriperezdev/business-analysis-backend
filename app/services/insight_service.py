"""
Service for generating actionable insights with market-specific context.
"""

from typing import Dict, List
from app.models.business_metrics import IndustryType, MarketType
from app.models.responses import Insight, MetricComparison
from app.utils.logging import get_logger

logger = get_logger(__name__)


# Market-specific context for insights
MARKET_CONTEXT: Dict[str, str] = {
    "argentina": "High inflation environment requires focus on pricing power and USD-linked contracts",
    "brazil": "Large market with strong digital adoption - focus on scale and efficiency",
    "chile": "Most stable LATAM economy - benchmarks closer to developed markets",
    "usa": "Highly competitive market requiring strong unit economics",
}


class InsightService:
    """Service for generating actionable business insights with market context."""
    
    @staticmethod
    def generate_insights(
        metrics: Dict[str, float],
        comparisons: Dict[str, MetricComparison],
        industry: IndustryType,
        market: MarketType = MarketType.USA
    ) -> List[Insight]:
        """
        Generate actionable insights based on metrics and benchmarks with market context.
        
        Args:
            metrics: Calculated metrics
            comparisons: Benchmark comparisons
            industry: Industry type
            market: Market type for market-specific insights
            
        Returns:
            List of insights with recommendations
        """
        logger.debug(f"Generating insights for {industry.value} industry in {market.value} market")
        
        insights: List[Insight] = []
        
        # Margin insights with market context
        insights.extend(InsightService._generate_margin_insights(comparisons, industry, market))
        
        # Customer acquisition insights
        insights.extend(InsightService._generate_customer_insights(metrics, market))
        
        # Cash runway insights
        insights.extend(InsightService._generate_cash_insights(metrics, market))
        
        # Churn insights
        insights.extend(InsightService._generate_churn_insights(metrics))
        
        logger.debug(f"Generated {len(insights)} insights for {market.value} market")
        return insights
    
    @staticmethod
    def _generate_margin_insights(
        comparisons: Dict[str, MetricComparison],
        industry: IndustryType,
        market: MarketType
    ) -> List[Insight]:
        """Generate insights about profit margins with market context."""
        insights: List[Insight] = []
        market_context = MARKET_CONTEXT.get(market.value, "")
        market_note = f" Note: In {market.value.upper()}, {market_context}" if market_context else ""
        
        if "gross_margin" in comparisons:
            comp = comparisons["gross_margin"]
            if comp.status == "needs_improvement":
                insights.append(Insight(
                    priority="high",
                    category="profitability",
                    title="Gross Margin Below Target",
                    description=(
                        f"Your gross margin of {comp.your_value}% is below the "
                        f"{industry.value} industry standard of {comp.benchmark_acceptable}% for {market.value}.{market_note}"
                    ),
                    recommendations=[
                        "Negotiate better supplier rates or find alternative vendors",
                        "Increase prices where market allows",
                        "Reduce production costs through automation or process improvements",
                    ]
                ))
        
        if "net_margin" in comparisons:
            comp = comparisons["net_margin"]
            if comp.status == "needs_improvement":
                insights.append(Insight(
                    priority="high",
                    category="profitability",
                    title="Net Margin Below Target",
                    description=(
                        f"Your net margin of {comp.your_value}% is below the "
                        f"{industry.value} industry standard of {comp.benchmark_acceptable}% for {market.value}.{market_note}"
                    ),
                    recommendations=[
                        "Review and optimize operating expenses",
                        "Focus on high-margin revenue streams",
                        "Consider automating manual processes to reduce costs",
                    ]
                ))
        
        return insights
    
    @staticmethod
    def _generate_customer_insights(metrics: Dict[str, float], market: MarketType = MarketType.USA) -> List[Insight]:
        """Generate insights about customer acquisition with market context."""
        insights: List[Insight] = []
        
        if "ltv_cac_ratio" in metrics:
            ratio = metrics["ltv_cac_ratio"]
            
            if ratio < 3:
                insights.append(Insight(
                    priority="critical",
                    category="growth",
                    title="Unsustainable Customer Acquisition",
                    description=(
                        f"LTV:CAC ratio of {ratio}:1 indicates you're spending "
                        "too much to acquire customers relative to their lifetime value."
                    ),
                    recommendations=[
                        "Reduce paid advertising spend and focus on organic channels",
                        "Improve conversion rates through A/B testing",
                        "Increase customer lifetime value through upsells and retention programs",
                        "Optimize sales and marketing processes to reduce CAC",
                    ]
                ))
            elif ratio > 5:
                insights.append(Insight(
                    priority="medium",
                    category="growth",
                    title="Growth Opportunity",
                    description=(
                        f"LTV:CAC ratio of {ratio}:1 suggests room to invest more "
                        "in customer acquisition to accelerate growth."
                    ),
                    recommendations=[
                        "Increase sales & marketing budget to accelerate growth",
                        "Expand into new channels or markets",
                        "Scale successful campaigns",
                        "Consider raising capital to fund growth",
                    ]
                ))
        
        if "cac_payback_months" in metrics:
            payback = metrics["cac_payback_months"]
            if payback > 18:
                insights.append(Insight(
                    priority="high",
                    category="growth",
                    title="Long CAC Payback Period",
                    description=(
                        f"CAC payback period of {payback} months is longer than ideal. "
                        "This impacts cash flow and growth velocity."
                    ),
                    recommendations=[
                        "Focus on improving conversion rates",
                        "Optimize pricing strategy",
                        "Target higher-value customer segments",
                    ]
                ))
        
        return insights
    
    @staticmethod
    def _generate_cash_insights(metrics: Dict[str, float], market: MarketType = MarketType.USA) -> List[Insight]:
        """Generate insights about cash runway with market context."""
        insights: List[Insight] = []
        
        # Market-specific cash runway recommendations
        market_cash_notes = {
            "argentina": "In Argentina's volatile economy, consider holding USD reserves and shorter payment terms.",
            "brazil": "Brazil's large market offers growth opportunities but requires careful cash management.",
            "chile": "Chile's stable economy allows for longer planning horizons.",
            "usa": "US market requires strong unit economics and efficient capital deployment.",
        }
        market_cash_note = market_cash_notes.get(market.value, "")
        
        if "runway_months" in metrics:
            runway = metrics["runway_months"]
            
            if runway < 6:
                recommendations = [
                    "Reduce operating expenses immediately",
                    "Accelerate revenue collection (shorten payment terms)",
                    "Begin fundraising process or explore bridge financing",
                    "Focus on highest-margin revenue opportunities",
                ]
                if market_cash_note:
                    recommendations.append(market_cash_note)
                
                insights.append(Insight(
                    priority="critical",
                    category="financial_health",
                    title="Low Cash Runway",
                    description=(
                        f"With only {runway} months of runway, immediate action is required."
                    ),
                    recommendations=recommendations
                ))
            elif runway < 12:
                recommendations = [
                    "Plan fundraising timeline if not yet profitable",
                    "Identify and eliminate non-essential expenses",
                    "Focus on high-margin revenue opportunities",
                    "Consider extending payment terms with suppliers",
                ]
                if market_cash_note:
                    recommendations.append(market_cash_note)
                
                insights.append(Insight(
                    priority="high",
                    category="financial_health",
                    title="Moderate Cash Runway",
                    description=(
                        f"{runway} months of runway requires proactive planning."
                    ),
                    recommendations=recommendations
                ))
        
        if "burn_multiple" in metrics:
            burn_multiple = metrics["burn_multiple"]
            if burn_multiple > 2.0:
                insights.append(Insight(
                    priority="high",
                    category="financial_health",
                    title="High Burn Multiple",
                    description=(
                        f"Burn multiple of {burn_multiple} indicates high burn rate "
                        "relative to revenue growth."
                    ),
                    recommendations=[
                        "Focus on improving revenue growth efficiency",
                        "Review and optimize spending across all departments",
                        "Ensure spending aligns with revenue-generating activities",
                    ]
                ))
        
        return insights
    
    @staticmethod
    def _generate_churn_insights(metrics: Dict[str, float]) -> List[Insight]:
        """Generate insights about customer churn."""
        insights: List[Insight] = []
        
        if "churn_rate" in metrics:
            churn = metrics["churn_rate"]
            
            if churn > 5:
                insights.append(Insight(
                    priority="high",
                    category="retention",
                    title="High Customer Churn",
                    description=(
                        f"Monthly churn rate of {churn}% is eroding your customer base."
                    ),
                    recommendations=[
                        "Implement customer success program to identify at-risk accounts",
                        "Conduct exit interviews to understand churn reasons",
                        "Add features or improve product based on customer feedback",
                        "Improve onboarding experience",
                        "Create retention campaigns for at-risk segments",
                    ]
                ))
            elif churn < 2:
                insights.append(Insight(
                    priority="low",
                    category="retention",
                    title="Excellent Customer Retention",
                    description=(
                        f"Churn rate of {churn}% indicates strong customer satisfaction."
                    ),
                    recommendations=[
                        "Leverage low churn to focus on expansion revenue",
                        "Consider referral programs to capitalize on satisfied customers",
                        "Use retention success as a sales differentiator",
                    ]
                ))
        
        return insights

