from backend.models.schemas import RiskAssessmentRequest, RiskAssessmentResponse, RiskComponent

def get_risk_label(score: float) -> str:
    if score < 0.33:
        return "Low"
    elif score < 0.67:
        return "Medium"
    else:
        return "High"

def calculate_risk(request: RiskAssessmentRequest) -> RiskAssessmentResponse:
    # 1. Delivery Risk
    delivery_risk_score = max(0.0, min(1.0, 1.0 - request.on_time_delivery_rate))
    
    # 2. Quality Risk
    quality_risk_score = request.defect_rate + (1.0 - request.avg_quality_score) * 0.5
    quality_risk_score = max(0.0, min(1.0, quality_risk_score))
    
    # 3. Supplier Concentration Risk
    is_low_confidence = False
    if request.transaction_count < 5:
        is_low_confidence = True
        
    supplier_risk_score = 0.0
    if request.total_category_spend > 0:
        supplier_risk_score = request.vendor_category_spend / request.total_category_spend
        supplier_risk_score = max(0.0, min(1.0, supplier_risk_score))
    else:
        is_low_confidence = True
        
    # 4. Payment Risk
    payment_risk_score = request.advance_payment_pct * (1.0 - request.on_time_delivery_rate)
    payment_risk_score = max(0.0, min(1.0, payment_risk_score))
    
    # Weights
    w_delivery = 0.30
    w_quality = 0.30
    w_supplier = 0.20
    w_payment = 0.20
    
    # Weighted Average Risk
    weighted_risk = (
        (w_delivery * delivery_risk_score) +
        (w_quality * quality_risk_score) +
        (w_supplier * supplier_risk_score) +
        (w_payment * payment_risk_score)
    )
    
    overall_risk_score = max(0.0, min(1.0, weighted_risk))
    supplier_health_score = max(0.0, min(1.0, 1.0 - overall_risk_score))
    
    return RiskAssessmentResponse(
        vendor_id=request.vendor_id,
        delivery_risk=RiskComponent(score=delivery_risk_score, label=get_risk_label(delivery_risk_score)),
        quality_risk=RiskComponent(score=quality_risk_score, label=get_risk_label(quality_risk_score)),
        supplier_risk=RiskComponent(score=supplier_risk_score, label=get_risk_label(supplier_risk_score)),
        payment_risk=RiskComponent(score=payment_risk_score, label=get_risk_label(payment_risk_score)),
        overall_risk=RiskComponent(score=overall_risk_score, label=get_risk_label(overall_risk_score)),
        supplier_health_score=supplier_health_score,
        is_low_confidence=is_low_confidence
    )
