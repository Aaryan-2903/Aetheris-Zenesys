from datetime import datetime
from typing import List
from backend.models.schemas import (
    AutomationEvaluationRequest,
    GeneratedAction,
    AutomationEvaluationResponse,
    PredictionRequest,
    RiskAssessmentRequest,
    FinancialExposureRequest
)
from backend.services.procurement_prediction_service import get_prediction
from backend.services.risk_service import calculate_risk
from backend.services.financial_service import calculate_financial_exposure

def evaluate_automation(req: AutomationEvaluationRequest) -> AutomationEvaluationResponse:
    actions: List[GeneratedAction] = []
    
    # ML Prediction
    pred_req = PredictionRequest(
        category=req.category,
        unit_price=req.unit_price,
        quantity=req.quantity,
        total_order_value=req.unit_price * req.quantity,
        lead_time_days=req.lead_time_days,
        historical_on_time_rate=req.historical_on_time_rate,
        historical_quality_score=req.historical_quality_score,
        payment_terms_days=req.payment_terms_days,
        advance_payment_pct=req.advance_payment_pct,
        order_complexity=0.5, # Default generic complexity
        vendor_transaction_count=req.vendor_transaction_count,
        vendor_defect_rate=req.vendor_defect_rate
    )
    prediction = get_prediction(pred_req)
    
    # Low-confidence ML prediction
    if prediction.confidence_score < 0.60:
        actions.append(GeneratedAction(
            action="MANUAL_REVIEW",
            priority="MEDIUM",
            reason=f"Prediction confidence is low ({prediction.confidence_score:.2f}).",
            recommendation="Human review required because prediction confidence is low.",
            trigger_source="ml_prediction"
        ))

    # Price Anomaly
    if req.historical_avg_price > 0 and req.unit_price > req.historical_avg_price * 1.2:
        actions.append(GeneratedAction(
            action="REVIEW_PRICE",
            priority="HIGH",
            reason="Procurement price signal indicates an abnormal/high price.",
            recommendation="Negotiate with the vendor or compare alternate vendors.",
            trigger_source="price_signal"
        ))

    # Delivery Degradation
    if req.historical_on_time_rate < 0.80:
        actions.append(GeneratedAction(
            action="REVIEW_DELIVERY",
            priority="HIGH",
            reason="Vendor delivery performance has degraded significantly.",
            recommendation="Consider an alternate vendor or request a revised delivery commitment.",
            trigger_source="delivery_performance"
        ))
        
    # Quality Degradation
    if req.historical_quality_score < 0.85:
        actions.append(GeneratedAction(
            action="VENDOR_REVIEW",
            priority="HIGH",
            reason="Quality performance indicates significant deterioration.",
            recommendation="Review vendor quality history before creating the next purchase order.",
            trigger_source="quality_performance"
        ))
        
    # Risk Assessment
    risk_req = RiskAssessmentRequest(
        vendor_id=req.vendor_id,
        on_time_delivery_rate=req.historical_on_time_rate,
        defect_rate=req.vendor_defect_rate,
        avg_quality_score=req.historical_quality_score,
        vendor_category_spend=req.vendor_category_spend,
        total_category_spend=req.total_category_spend,
        advance_payment_pct=req.advance_payment_pct,
        transaction_count=req.vendor_transaction_count
    )
    risk_assessment = calculate_risk(risk_req)
    
    # Payment Risk
    if risk_assessment.payment_risk.score > 0.7 or risk_assessment.payment_risk.label == "High":
        priority = "HIGH" if risk_assessment.payment_risk.score > 0.85 else "MEDIUM"
        actions.append(GeneratedAction(
            action="PAYMENT_REVIEW",
            priority=priority,
            reason="Payment-related risk signal exceeds the existing configured threshold.",
            recommendation="Review payment terms before proceeding.",
            trigger_source="payment_risk"
        ))

    # Financial Exposure
    fin_req = FinancialExposureRequest(
        purchase_value=req.unit_price * req.quantity,
        advance_payment_pct=req.advance_payment_pct,
        historical_price_stddev=req.historical_price_stddev,
        historical_avg_price=req.historical_avg_price,
        transaction_count=req.vendor_transaction_count,
        supplier_health_score=risk_assessment.supplier_health_score,
        payment_risk_score=risk_assessment.payment_risk.score,
        delivery_risk_score=risk_assessment.delivery_risk.score,
        quality_risk_score=risk_assessment.quality_risk.score
    )
    fin_exposure = calculate_financial_exposure(fin_req)
    
    # High Financial Exposure
    if fin_exposure.total_money_at_risk > 50000 or fin_exposure.exposure_percentage > 0.40:
        actions.append(GeneratedAction(
            action="APPROVAL_REQUIRED",
            priority="HIGH",
            reason="Existing financial exposure indicates substantial money at risk.",
            recommendation="Require procurement approval before proceeding.",
            trigger_source="financial_exposure"
        ))

    # Determine automation status
    if len(actions) > 0:
        status = "ACTION_REQUIRED"
    else:
        status = "NO_ACTION_REQUIRED"
        
        # Strong Procurement Decision
        if (
            prediction.confidence_score >= 0.75 and 
            req.historical_on_time_rate >= 0.85 and 
            req.historical_quality_score >= 0.85 and 
            fin_exposure.exposure_percentage <= 0.30 and 
            (req.historical_avg_price == 0 or req.unit_price <= req.historical_avg_price * 1.1)
        ):
             actions.append(GeneratedAction(
                 action="PROCEED",
                 priority="LOW",
                 reason="Vendor performance is strong and exposure is acceptable.",
                 recommendation="Procurement can proceed with the selected vendor.",
                 trigger_source="strong_procurement_decision"
             ))

    return AutomationEvaluationResponse(
        automation_status=status,
        generated_actions=actions,
        created_at=datetime.utcnow().isoformat() + "Z"
    )
