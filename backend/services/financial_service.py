from backend.models.schemas import FinancialExposureRequest, FinancialExposureResponse

def calculate_financial_exposure(req: FinancialExposureRequest) -> FinancialExposureResponse:
    # Calculate price_stddev_pct
    is_low_confidence_price = False
    if req.transaction_count < 5 or req.historical_avg_price <= 0:
        price_stddev_pct = 0.0
        is_low_confidence_price = True
    else:
        price_stddev_pct = req.historical_price_stddev / req.historical_avg_price
    
    # 1. Price Risk Exposure
    # Formula: purchase_value * price_stddev_pct * 0.5
    price_risk_exposure = req.purchase_value * price_stddev_pct * 0.5
    
    # 2. Supplier Risk Exposure
    # Formula: purchase_value * (1.0 - supplier_health_score) * 0.3
    supplier_risk_exposure = req.purchase_value * (1.0 - req.supplier_health_score) * 0.3
    
    # 3. Payment/Advance Risk Exposure
    # Formula: (advance_payment_pct * purchase_value) * payment_risk_score
    payment_risk_exposure = (req.advance_payment_pct * req.purchase_value) * req.payment_risk_score
    
    # 4. Delivery Risk Exposure
    # Formula: purchase_value * delivery_risk_score * 0.15
    delivery_risk_exposure = req.purchase_value * req.delivery_risk_score * 0.15
    
    # 5. Quality Risk Exposure
    # Formula: purchase_value * quality_risk_score * 0.2
    quality_risk_exposure = req.purchase_value * req.quality_risk_score * 0.2
    
    # Total Money At Risk
    total_mar = (
        price_risk_exposure +
        supplier_risk_exposure +
        payment_risk_exposure +
        delivery_risk_exposure +
        quality_risk_exposure
    )
    
    # Calculate percentage
    exposure_pct = 0.0
    if req.purchase_value > 0:
        exposure_pct = total_mar / req.purchase_value
        
    return FinancialExposureResponse(
        purchase_value=req.purchase_value,
        price_risk_exposure=price_risk_exposure,
        supplier_risk_exposure=supplier_risk_exposure,
        payment_risk_exposure=payment_risk_exposure,
        delivery_risk_exposure=delivery_risk_exposure,
        quality_risk_exposure=quality_risk_exposure,
        total_money_at_risk=total_mar,
        exposure_percentage=exposure_pct,
        is_low_confidence_price=is_low_confidence_price
    )
