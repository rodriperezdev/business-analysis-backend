"""
Scenario analysis endpoint router.
"""

from fastapi import APIRouter, HTTPException
from app.models.scenario import ScenarioInput
from app.models.responses import ScenarioResponse
from app.services.metrics_calculator import MetricsCalculator
from app.utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/scenario", tags=["Scenario"])


@router.post("", response_model=ScenarioResponse)
async def scenario_analysis(scenario: ScenarioInput) -> ScenarioResponse:
    """
    What-if scenario analysis endpoint.
    
    Applies percentage changes to base metrics and calculates the impact
    on all derived metrics.
    
    Args:
        scenario: Base metrics and changes to apply
        
    Returns:
        Comparison of base vs. new metrics with impact analysis
        
    Raises:
        HTTPException: If scenario analysis fails
    """
    try:
        logger.info(f"Running scenario analysis with {len(scenario.changes)} changes")
        
        # Calculate base metrics
        base_metrics = MetricsCalculator.calculate(scenario.base_metrics)
        
        # Apply changes to create modified metrics
        modified_data = scenario.base_metrics.model_copy(deep=True)
        for field, change_pct in scenario.changes.items():
            if hasattr(modified_data, field):
                current_value = getattr(modified_data, field)
                if current_value is not None and isinstance(current_value, (int, float)):
                    new_value = current_value * (1 + change_pct / 100)
                    setattr(modified_data, field, new_value)
                    logger.debug(f"Applied {change_pct}% change to {field}")
        
        # Calculate new metrics
        new_metrics = MetricsCalculator.calculate(modified_data)
        
        # Calculate deltas
        impact: dict[str, dict[str, float]] = {}
        for key in base_metrics:
            if key in new_metrics:
                delta = new_metrics[key] - base_metrics[key]
                delta_pct = (
                    (delta / base_metrics[key] * 100) 
                    if base_metrics[key] != 0 
                    else 0.0
                )
                impact[key] = {
                    "absolute": round(delta, 2),
                    "percentage": round(delta_pct, 2)
                }
        
        logger.info("Scenario analysis complete")
        
        return ScenarioResponse(
            base_metrics=base_metrics,
            new_metrics=new_metrics,
            changes_applied=scenario.changes,
            impact=impact
        )
        
    except ValueError as e:
        logger.error(f"Validation error in scenario analysis: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in scenario analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during scenario analysis"
        )



