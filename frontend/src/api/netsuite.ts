import { apiClient } from './client';

export interface NetSuiteStatus {
  status: string;
  message: string;
  mode?: string;
  last_sync?: string | null;
}

export const netsuiteApi = {
  getStatus: async (): Promise<NetSuiteStatus> => {
    return apiClient<NetSuiteStatus>('/api/netsuite/status', {
      method: 'GET',
    });
  }
};
