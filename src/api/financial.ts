import { apiClient } from "./client";

export interface FinancialExposureRequest {
  vendor_id: string;
  order_volume: number;
  unit_price: number;
  currency_volatility_index: number;
  default_probability: number;
}

export interface FinancialExposureResponse {
  vendor_id: string;
  total_exposure: number;
  value_at_risk: number;
  risk_status: string;
}

export async function calculateFinancialExposure(data: FinancialExposureRequest): Promise<FinancialExposureResponse> {
  return apiClient<FinancialExposureResponse>("/api/financial/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
