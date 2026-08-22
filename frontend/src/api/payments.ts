import { apiClient } from './client';

export interface PaymentCreateRequest {
  purchase_order_id: string;
}

export interface PaymentCreateResponse {
  purchase_order_id: string;
  razorpay_order_id: string;
  amount: number;
  currency: string;
  key_id: string;
  payment_status: string;
}

export interface PaymentVerifyRequest {
  purchase_order_id: string;
  razorpay_order_id: string;
  razorpay_payment_id: string;
  razorpay_signature: string;
}

export const paymentsApi = {
  createOrder: async (data: PaymentCreateRequest): Promise<PaymentCreateResponse> => {
    return apiClient<PaymentCreateResponse>('/api/payments/create-order', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  verify: async (data: PaymentVerifyRequest): Promise<any> => {
    return apiClient<any>('/api/payments/verify', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
};
