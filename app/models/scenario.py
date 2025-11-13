"""
Scenario analysis models.
"""

from pydantic import BaseModel, Field
from typing import Dict
from .business_metrics import BusinessMetrics


class ScenarioInput(BaseModel):
    """
    Input for what-if scenario analysis.
    
    Changes are specified as percentage changes (e.g., 15 means +15%, -10 means -10%).
    """
    
    base_metrics: BusinessMetrics = Field(
        description="Base business metrics"
    )
    changes: Dict[str, float] = Field(
        description="Percentage changes to apply to metrics",
        examples=[{"revenue": 15, "cogs": -10, "operating_expenses": -5}]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "base_metrics": {
                    "revenue": 100000.0,
                    "cogs": 30000.0,
                    "operating_expenses": 40000.0,
                    "sales_marketing_expense": 15000.0,
                    "industry": "saas",
                    "time_period_months": 1
                },
                "changes": {
                    "revenue": 15,
                    "cogs": -10
                }
            }
        }






