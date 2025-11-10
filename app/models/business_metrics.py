"""
Business metrics data models.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class IndustryType(str, Enum):
    """Supported industry types for benchmarking."""
    
    SAAS = "saas"
    ECOMMERCE = "ecommerce"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    SERVICES = "services"


class MarketType(str, Enum):
    """Supported geographic markets for benchmarking."""
    
    USA = "usa"
    ARGENTINA = "argentina"
    BRAZIL = "brazil"
    CHILE = "chile"


class BusinessMetrics(BaseModel):
    """
    Business metrics input model.
    
    All financial values should be in the same currency unit.
    Time period should match the revenue period (e.g., if revenue is monthly, 
    time_period_months should be 1).
    """
    
    # Revenue & Costs
    revenue: float = Field(
        gt=0,
        description="Total revenue for the period",
        examples=[100000.0]
    )
    cogs: float = Field(
        ge=0,
        description="Cost of goods sold",
        examples=[30000.0]
    )
    operating_expenses: float = Field(
        ge=0,
        description="Operating expenses (excluding COGS)",
        examples=[40000.0]
    )
    sales_marketing_expense: float = Field(
        ge=0,
        description="Sales & marketing spend",
        examples=[15000.0]
    )
    
    # Customer Metrics
    new_customers: Optional[int] = Field(
        None,
        gt=0,
        description="New customers acquired in the period"
    )
    total_customers: Optional[int] = Field(
        None,
        gt=0,
        description="Total active customers at period end"
    )
    churned_customers: Optional[int] = Field(
        None,
        ge=0,
        description="Customers lost during the period"
    )
    
    # Financial Health
    cash_balance: Optional[float] = Field(
        None,
        ge=0,
        description="Current cash balance"
    )
    monthly_burn: Optional[float] = Field(
        None,
        ge=0,
        description="Monthly cash burn rate"
    )
    
    # Context
    industry: IndustryType = Field(
        description="Industry type for benchmarking"
    )
    market: MarketType = Field(
        default=MarketType.USA,
        description="Geographic market for market-specific benchmarking"
    )
    time_period_months: int = Field(
        default=1,
        gt=0,
        le=12,
        description="Reporting period in months (1-12)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "revenue": 100000.0,
                "cogs": 30000.0,
                "operating_expenses": 40000.0,
                "sales_marketing_expense": 15000.0,
                "new_customers": 50,
                "total_customers": 500,
                "churned_customers": 10,
                "cash_balance": 200000.0,
                "monthly_burn": 35000.0,
                "industry": "saas",
                "market": "usa",
                "time_period_months": 1
            }
        }

