import { apiClient } from "./client";

export interface ContractRequest {
  vendor_id: string;
  title: string;
  total_value: number;
  start_date: string;
  end_date: string;
  payment_terms: string;
  cancellation_clause: string;
}

export interface ContractResponse {
  contract_id: string;
  vendor_id: string;
  title: string;
  total_value: number;
  start_date: string;
  end_date: string;
  payment_terms: string;
  cancellation_clause: string;
  status: string;
  created_at: string;
}

export async function createContract(data: ContractRequest): Promise<ContractResponse> {
  return apiClient<ContractResponse>("/api/contracts/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getContract(contractId: string): Promise<ContractResponse> {
  return apiClient<ContractResponse>(`/api/contracts/${contractId}`, {
    method: "GET",
  });
}
