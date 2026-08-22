import { apiClient } from './client';

export interface ScoringWeights {
  weight_delivery?: number;
  weight_quality?: number;
  weight_price?: number;
  weight_lead_time?: number;
  weight_payment?: number;
}

export interface VendorScoreRequestItem {
  vendor_id: string;
  on_time_delivery_rate: number;
  avg_quality_score: number;
  vendor_price: number;
  actual_lead_time: number;
  payment_terms_days: number;
}

export interface ProcurementScoringRequest {
  budget_per_unit: number;
  required_lead_time: number;
  vendors: VendorScoreRequestItem[];
  weights?: ScoringWeights;
}

export interface VendorScoreComponents {
  delivery_score: number;
  quality_score: number;
  price_score: number;
  lead_time_score: number;
  payment_score: number;
}

export interface VendorScoreResponseItem {
  vendor_id: string;
  final_score: number;
  components: VendorScoreComponents;
}

export interface ProcurementScoringResponse {
  ranked_vendors: VendorScoreResponseItem[];
}

export const scoreApi = {
  rankVendors: async (data: ProcurementScoringRequest): Promise<ProcurementScoringResponse> => {
    return apiClient<ProcurementScoringResponse>('/api/score/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
};
