import { apiClient } from "./client";

export interface ScoreRequest {
  vendor_id: string;
  quality_rating: number;
  delivery_rating: number;
  responsiveness_rating: number;
  price_competitiveness: number;
}

export interface ScoreResponse {
  vendor_id: string;
  score: number;
  tier: string;
  recommendation: string;
}

export async function scoreVendor(data: ScoreRequest): Promise<ScoreResponse> {
  return apiClient<ScoreResponse>("/api/score/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
