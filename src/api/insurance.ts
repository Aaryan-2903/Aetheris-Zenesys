import { apiClient } from "./client";

export interface InsuranceRequest {
  vendor_id: string;
  shipment_value: number;
  origin_country: string;
  destination_country: string;
  transport_mode: string;
  goods_category: string;
}

export interface InsuranceResponse {
  insurance_id: string;
  vendor_id: string;
  provider: string;
  premium_amount: number;
  coverage_amount: number;
  deductible: number;
  policy_terms: string;
  status: string;
  created_at: string;
}

export async function purchaseInsurance(data: InsuranceRequest): Promise<InsuranceResponse> {
  return apiClient<InsuranceResponse>("/api/insurance/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
