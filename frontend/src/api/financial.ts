import { apiClient } from './client';

export interface FinancialExposureRequest {
  purchase_value: number;
  advance_payment_pct: number;
  historical_price_stddev: number;
  historical_avg_price: number;
  transaction_count: number;
  supplier_health_score: number;
  payment_risk_score: number;
  delivery_risk_score: number;
  quality_risk_score: number;
}

export interface FinancialExposureResponse {
  purchase_value: number;
  price_risk_exposure: number;
  supplier_risk_exposure: number;
  payment_risk_exposure: number;
  delivery_risk_exposure: number;
  quality_risk_exposure: number;
  total_money_at_risk: number;
  exposure_percentage: number;
  is_low_confidence_price: boolean;
}

export const financialApi = {
  calculateExposure: async (data: FinancialExposureRequest): Promise<FinancialExposureResponse> => {
    return apiClient<FinancialExposureResponse>('/api/financial/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
};
