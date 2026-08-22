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

# --- Scoring Engine Schemas ---

class ScoringWeights(BaseModel):
    weight_delivery: float = Field(0.25, description="Weight for delivery reliability")
    weight_quality: float = Field(0.25, description="Weight for quality")
    weight_price: float = Field(0.20, description="Weight for price competitiveness")
    weight_lead_time: float = Field(0.15, description="Weight for lead time")
    weight_payment: float = Field(0.15, description="Weight for payment terms")

class VendorScoreRequestItem(BaseModel):
    vendor_id: str = Field(..., description="Unique vendor identifier")
    on_time_delivery_rate: float = Field(..., description="Historical on-time delivery rate (0-1)")
    avg_quality_score: float = Field(..., description="Historical average quality score (0-1)")
    vendor_price: float = Field(..., description="Offered price per unit")
    actual_lead_time: int = Field(..., description="Offered lead time in days")
    payment_terms_days: int = Field(..., description="Offered payment terms in days")

class ProcurementScoringRequest(BaseModel):
    budget_per_unit: float = Field(..., description="Target budget per unit")
    required_lead_time: int = Field(..., description="Required lead time in days")
    vendors: List[VendorScoreRequestItem] = Field(..., description="List of vendors to score and rank")
    weights: Optional[ScoringWeights] = Field(None, description="Custom weights (defaults will be used if omitted)")

class VendorScoreComponents(BaseModel):
    delivery_score: float
    quality_score: float
    price_score: float
    lead_time_score: float
    payment_score: float

class VendorScoreResponseItem(BaseModel):
    vendor_id: str
    final_score: float = Field(..., description="Deterministic composite score (0-1)")
    components: VendorScoreComponents

class ProcurementScoringResponse(BaseModel):
    ranked_vendors: List[VendorScoreResponseItem] = Field(..., description="Vendors ranked by final_score descending")

# --- Risk Engine Schemas ---

class RiskAssessmentRequest(BaseModel):
    vendor_id: str
    on_time_delivery_rate: float = Field(..., ge=0.0, le=1.0)
    defect_rate: float = Field(..., ge=0.0, le=1.0)
    avg_quality_score: float = Field(..., ge=0.0, le=1.0)
    vendor_category_spend: float = Field(..., ge=0.0)
    total_category_spend: float = Field(..., ge=0.0)
    advance_payment_pct: float = Field(..., ge=0.0, le=1.0)
    transaction_count: int = Field(..., ge=0, description="Number of historical transactions")

class RiskComponent(BaseModel):
    score: float = Field(..., description="Calculated risk score")
    label: str = Field(..., description="Risk label: Low, Medium, or High")

class RiskAssessmentResponse(BaseModel):
    vendor_id: str
    delivery_risk: RiskComponent
    quality_risk: RiskComponent
    supplier_risk: RiskComponent
    payment_risk: RiskComponent
    overall_risk: RiskComponent
    supplier_health_score: float = Field(..., description="Deterministic supplier health score (0-1)")
    is_low_confidence: bool = Field(False, description="Flagged if < 5 transactions or zero category spend")

# --- Financial Exposure Schemas ---

class FinancialExposureRequest(BaseModel):
    purchase_value: float = Field(..., ge=0.0)
    advance_payment_pct: float = Field(..., ge=0.0, le=1.0)
    historical_price_stddev: float = Field(..., ge=0.0)
    historical_avg_price: float = Field(..., ge=0.0)
    transaction_count: int = Field(..., ge=0)
    supplier_health_score: float = Field(..., ge=0.0, le=1.0)
    payment_risk_score: float = Field(..., ge=0.0, le=1.0)
    delivery_risk_score: float = Field(..., ge=0.0, le=1.0)
    quality_risk_score: float = Field(..., ge=0.0, le=1.0)

class FinancialExposureResponse(BaseModel):
    purchase_value: float
    price_risk_exposure: float
    supplier_risk_exposure: float
    payment_risk_exposure: float
    delivery_risk_exposure: float
    quality_risk_exposure: float
    total_money_at_risk: float
    exposure_percentage: float = Field(..., description="total_money_at_risk / purchase_value")
    is_low_confidence_price: bool = Field(..., description="True if < 5 transactions or zero avg price")

# --- Contract Engine Schemas ---

class ContractCreateRequest(BaseModel):
    procurement_request_id: str
    vendor_id: str
    buyer_terms: str
    vendor_terms: str
    payment_terms: str
    delivery_terms: str
    warranty_terms: str
    return_replacement_terms: str
    compliance_requirements: str
    buyer_code_of_conduct: str
    vendor_code_of_conduct: str

class ContractResponse(BaseModel):
    contract_id: str
    procurement_request_id: str
    vendor_id: str
    buyer_terms: str
    vendor_terms: str
    payment_terms: str
    delivery_terms: str
    warranty_terms: str
    return_replacement_terms: str
    compliance_requirements: str
    buyer_code_of_conduct: str
    vendor_code_of_conduct: str
    status: str
    buyer_accepted: bool
    vendor_accepted: bool
    created_at: str
    accepted_at: Optional[str] = None

# --- Protection Layer Schemas ---

class WarrantyPlan(BaseModel):
    plan_id: str
    plan_name: str
    warranty_period_months: int
    warranty_fee: float
    coverage_description: str

class WarrantyCreateRequest(BaseModel):
    procurement_request_id: str
    vendor_id: str
    product_or_service: str
    plan_id: str
    warranty_start_date: str

class WarrantyResponse(BaseModel):
    warranty_id: str
    procurement_request_id: str
    vendor_id: str
    product_or_service: str
    plan_id: str
    warranty_period_months: int
    warranty_fee: float
    warranty_start_date: str
    warranty_expiry_date: str
    status: str
    coverage_description: str
    claim_reference: Optional[str] = None

class InsuranceCreateRequest(BaseModel):
    procurement_request_id: str
    vendor_id: str
    provider: str
    policy_number: str
    coverage_amount: float = Field(..., ge=0.0)
    start_date: str
    expiry_date: str
    coverage_description: str

class InsuranceResponse(BaseModel):
    insurance_id: str
    procurement_request_id: str
    vendor_id: str
    provider: str
    policy_number: str
    coverage_amount: float
    start_date: str
    expiry_date: str
    status: str
    coverage_description: str

# --- Vendor Intelligence Schemas ---

class RepeatRatioRequest(BaseModel):
    vendor_id: str
    total_orders: int = Field(..., gt=0, description="Total number of orders")
    repeat_orders: int = Field(..., ge=0, description="Number of repeat orders")

class RepeatRatioResponse(BaseModel):
    vendor_id: str
    total_orders: int
    repeat_orders: int
    order_repeat_ratio: float = Field(..., ge=0.0, le=100.0, description="Repeat Ratio percentage")
    interpretation: str

# --- Buyer Feedback Schemas ---

class BuyerFeedbackRequest(BaseModel):
    order_id: str
    vendor_id: str
    overall_rating: int = Field(..., ge=1, le=5)
    quality_rating: int = Field(..., ge=1, le=5)
    delivery_rating: int = Field(..., ge=1, le=5)
    responsiveness_rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = Field(None, max_length=1000)

class BuyerFeedbackResponse(BaseModel):
    feedback_id: str
    order_id: str
    vendor_id: str
    overall_rating: int
    quality_rating: int
    delivery_rating: int
    responsiveness_rating: int
    comments: Optional[str] = None
    created_at: str

class VendorFeedbackSummary(BaseModel):
    vendor_id: str
    feedback_count: int
    average_overall_rating: float
    average_quality_rating: float
    average_delivery_rating: float
    average_responsiveness_rating: float
