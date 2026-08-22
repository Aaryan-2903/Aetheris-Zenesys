from backend.models.schemas import ProcurementScoringRequest, ProcurementScoringResponse, VendorScoreComponents, VendorScoreResponseItem, ScoringWeights

def calculate_business_score(request: ProcurementScoringRequest) -> ProcurementScoringResponse:
    """
    Calculates deterministic vendor scores based on docs/rules.md Layer 2.
    """
    weights = request.weights or ScoringWeights()
    
    # Normalize weights to sum to 1.0 just in case
    total_weight = (
        weights.weight_delivery +
        weights.weight_quality +
        weights.weight_price +
        weights.weight_lead_time +
        weights.weight_payment
    )
    
    w_delivery = weights.weight_delivery / total_weight
    w_quality = weights.weight_quality / total_weight
    w_price = weights.weight_price / total_weight
    w_lead_time = weights.weight_lead_time / total_weight
    w_payment = weights.weight_payment / total_weight

    scored_vendors = []
    
    for vendor in request.vendors:
        # Price Score: price_competitiveness_score = min(budget_per_unit, vendor_price) / max(budget_per_unit, vendor_price)
        # Handle zero division safely
        max_price = max(request.budget_per_unit, vendor.vendor_price)
        price_score = min(request.budget_per_unit, vendor.vendor_price) / max_price if max_price > 0 else 1.0

        # Lead Time Score: 1.0 if actual_lead_time <= required_lead_time else required_lead_time / actual_lead_time
        # Handle zero division safely
        if vendor.actual_lead_time <= request.required_lead_time:
            lead_time_score = 1.0
        else:
            lead_time_score = request.required_lead_time / vendor.actual_lead_time if vendor.actual_lead_time > 0 else 1.0
            
        # Payment Terms Score: min(payment_terms_days, 60) / 60
        payment_score = min(vendor.payment_terms_days, 60) / 60.0 if vendor.payment_terms_days >= 0 else 0.0

        # Component Scores
        delivery_score = vendor.on_time_delivery_rate
        quality_score = vendor.avg_quality_score

        components = VendorScoreComponents(
            delivery_score=delivery_score,
            quality_score=quality_score,
            price_score=price_score,
            lead_time_score=lead_time_score,
            payment_score=payment_score
        )
        
        # Final Score
        final_score = (
            (w_delivery * delivery_score) +
            (w_quality * quality_score) +
            (w_price * price_score) +
            (w_lead_time * lead_time_score) +
            (w_payment * payment_score)
        )
        
        scored_vendors.append(VendorScoreResponseItem(
            vendor_id=vendor.vendor_id,
            final_score=final_score,
            components=components
        ))
        
    # Rank descending by final_score
    scored_vendors.sort(key=lambda x: x.final_score, reverse=True)
    
    return ProcurementScoringResponse(ranked_vendors=scored_vendors)

