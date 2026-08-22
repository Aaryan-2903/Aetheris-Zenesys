import { apiClient } from './client';

export interface PredictionRequest {
  category: string;
  unit_price: number;
  quantity: number;
  total_order_value: number;
  lead_time_days: number;
  historical_on_time_rate: number;
  historical_quality_score: number;
  payment_terms_days: number;
  advance_payment_pct: number;
  order_complexity: number;
  vendor_transaction_count: number;
  vendor_defect_rate: number;
}

export interface PredictionResponse {
  predicted_outcome: number;
  confidence_score: number;
}

export const predictionApi = {
  predict: async (data: PredictionRequest): Promise<PredictionResponse> => {
    return apiClient<PredictionResponse>('/api/predict/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
};
