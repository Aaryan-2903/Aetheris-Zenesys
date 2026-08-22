import { apiClient } from "./client";

export interface WarrantyPlan {
  plan_id: string;
  plan_name: string;
  duration_months: number;
  coverage_type: string;
  fee_percentage: number;
}

export interface WarrantyPurchaseRequest {
  vendor_id: string;
  equipment_category: string;
  purchase_price: number;
  plan_id: string;
}

export interface WarrantyResponse {
  warranty_id: string;
  plan_id: string;
  plan_name: string;
  vendor_id: string;
  equipment_category: string;
  coverage_end_date: string;
  fee_amount: number;
  status: string;
}

export async function getWarrantyPlans(): Promise<WarrantyPlan[]> {
  return apiClient<WarrantyPlan[]>("/api/warranty/plans", {
    method: "GET",
  });
}

export async function purchaseWarranty(data: WarrantyPurchaseRequest): Promise<WarrantyResponse> {
  return apiClient<WarrantyResponse>("/api/warranty/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
