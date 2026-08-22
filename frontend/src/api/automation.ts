import { apiClient } from './client';

export interface AutomationEvaluationRequest {
  vendor_id: string;
  category: string;
  unit_price: number;
  quantity: number;
  lead_time_days: number;
  payment_terms_days: number;
  advance_payment_pct: number;
  historical_on_time_rate: number;
  historical_quality_score: number;
  historical_avg_price: number;
  vendor_defect_rate: number;
  vendor_transaction_count: number;
  vendor_category_spend: number;
  total_category_spend: number;
  historical_price_stddev: number;
}

export interface GeneratedAction {
  action: string;
  priority: string;
  reason: string;
  recommendation: string;
  trigger_source: string;
}

export interface AutomationEvaluationResponse {
  automation_status: string;
  generated_actions: GeneratedAction[];
  created_at: string;
}

export const automationApi = {
  evaluate: async (data: AutomationEvaluationRequest): Promise<AutomationEvaluationResponse> => {
    return apiClient<AutomationEvaluationResponse>('/api/automation/evaluate', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
};
