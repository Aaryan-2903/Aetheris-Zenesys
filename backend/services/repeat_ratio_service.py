from fastapi import HTTPException
from backend.models.schemas import RepeatRatioRequest, RepeatRatioResponse

_repeat_ratios = {}

def get_interpretation(ratio: float) -> str:
    if ratio <= 30.0:
        return "Low"
    elif ratio <= 60.0:
        return "Moderate"
    elif ratio <= 80.0:
        return "High"
    else:
        return "Very High"

def calculate_repeat_ratio(request: RepeatRatioRequest) -> RepeatRatioResponse:
    if request.repeat_orders > request.total_orders:
        raise HTTPException(
            status_code=400,
            detail="repeat_orders cannot be greater than total_orders"
        )
        
    ratio = (request.repeat_orders / request.total_orders) * 100.0
    
    response = RepeatRatioResponse(
        vendor_id=request.vendor_id,
        total_orders=request.total_orders,
        repeat_orders=request.repeat_orders,
        order_repeat_ratio=ratio,
        interpretation=get_interpretation(ratio)
    )
    
    _repeat_ratios[request.vendor_id] = response
    return response

def get_repeat_ratio(vendor_id: str) -> RepeatRatioResponse:
    if vendor_id not in _repeat_ratios:
        raise HTTPException(status_code=404, detail="Repeat ratio data not found for vendor")
    return _repeat_ratios[vendor_id]
