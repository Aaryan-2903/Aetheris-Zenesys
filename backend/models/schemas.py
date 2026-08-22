from pydantic import BaseModel, Field
from typing import Optional, List

class PredictionRequest(BaseModel):
    category: str = Field(..., description="Procurement category")
    unit_price: float = Field(..., description="Unit price of item")
    quantity: int = Field(..., description="Order quantity")
    total_order_value: float = Field(..., description="Calculated from price × quantity")
    lead_time_days: int = Field(..., description="Promised delivery lead time")
    historical_on_time_rate: float = Field(..., description="Vendor historical on-time delivery %")
    historical_quality_score: float = Field(..., description="Vendor historical quality rating (0-1)")
    payment_terms_days: int = Field(..., description="Net payment terms in days")
    advance_payment_pct: float = Field(..., description="% of order paid in advance")
    order_complexity: float = Field(..., description="Derived complexity score (0-1)")
    vendor_transaction_count: int = Field(..., description="Historical order volume with vendor")
    vendor_defect_rate: float = Field(..., description="Historical defect/rejection rate")

class PredictionResponse(BaseModel):
    predicted_outcome: int = Field(..., description="1 (on-time, successful delivery) or 0 (late or failed delivery)")
    confidence_score: float = Field(..., description="Probability of success (0.0 to 1.0)")
