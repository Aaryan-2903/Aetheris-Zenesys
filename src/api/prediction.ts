import { apiClient } from "./client";

export interface PredictionRequest {
  category: string;
  historical_delay_days: number;
  quality_score: number;
  delivery_score: number;
  price: number;
  volume: number;
}

export interface PredictionResponse {
  vendor_score: number;
  risk_probability: number;
  recommendation: string;
}

export async function predictVendor(data: PredictionRequest): Promise<PredictionResponse> {
  return apiClient<PredictionResponse>("/api/predict/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
