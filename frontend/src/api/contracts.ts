import { apiClient } from './client';

export interface ContractCreateRequest {
  procurement_request_id: string;
  vendor_id: string;
  buyer_terms: string;
  vendor_terms: string;
  payment_terms: string;
  delivery_terms: string;
  warranty_terms: string;
  return_replacement_terms: string;
  compliance_requirements: string;
  buyer_code_of_conduct: string;
  vendor_code_of_conduct: string;
}

export interface ContractResponse {
  contract_id: string;
  procurement_request_id: string;
  vendor_id: string;
  buyer_terms: string;
  vendor_terms: string;
  payment_terms: string;
  delivery_terms: string;
  warranty_terms: string;
  return_replacement_terms: string;
  compliance_requirements: string;
  buyer_code_of_conduct: string;
  vendor_code_of_conduct: string;
  status: string;
  buyer_accepted: boolean;
  vendor_accepted: boolean;
  created_at: string;
  accepted_at?: string;
}

export const contractsApi = {
  create: async (data: ContractCreateRequest): Promise<ContractResponse> => {
    return apiClient<ContractResponse>('/api/contracts/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  get: async (contractId: string): Promise<ContractResponse> => {
    return apiClient<ContractResponse>(`/api/contracts/${contractId}`, {
      method: 'GET',
    });
  }
};
