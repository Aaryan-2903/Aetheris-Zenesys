import { apiClient } from "./client";

export interface RiskRequest {
  vendor_id: string;
  category: string;
  historical_delay_days: number;
  market_volatility_index: number;
  geopolitical_risk_score: number;
  compliance_score: number;
}

export interface RiskResponse {
  vendor_id: string;
  risk_probability: number;
  risk_level: string;
  mitigation_strategy: string;
}

export async function assessRisk(data: RiskRequest): Promise<RiskResponse> {
  return apiClient<RiskResponse>("/api/risk/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
