import { apiClient } from "./client";

export interface OrderHistoryRequest {
  vendor_id: string;
  total_orders_last_year: number;
  repeat_orders: number;
  average_order_value: number;
  return_rate_percentage: number;
}

export interface RepeatRatioResponse {
  vendor_id: string;
  repeat_ratio: number;
  loyalty_tier: string;
  recommendation: string;
}

export async function evaluateRepeatRatio(data: OrderHistoryRequest): Promise<RepeatRatioResponse> {
  return apiClient<RepeatRatioResponse>("/api/repeat-ratio/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
