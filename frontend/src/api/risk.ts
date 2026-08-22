import { apiClient } from './client';

export interface RiskComponent {
  score: number;
  label: string;
}

export interface RiskAssessmentRequest {
  vendor_id: string;
  on_time_delivery_rate: number;
  defect_rate: number;
  avg_quality_score: number;
  vendor_category_spend: number;
  total_category_spend: number;
  advance_payment_pct: number;
  transaction_count: number;
}

export interface RiskAssessmentResponse {
  vendor_id: string;
  delivery_risk: RiskComponent;
  quality_risk: RiskComponent;
  supplier_risk: RiskComponent;
  payment_risk: RiskComponent;
  overall_risk: RiskComponent;
  supplier_health_score: number;
  is_low_confidence: boolean;
}

export const riskApi = {
  assessRisk: async (data: RiskAssessmentRequest): Promise<RiskAssessmentResponse> => {
    return apiClient<RiskAssessmentResponse>('/api/risk/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
};
