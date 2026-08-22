import { apiClient } from "./client";

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

export interface PaymentVerifyResponse {
  status: string;
  message: string;
}

export async function createPaymentOrder(purchaseOrderId: string): Promise<PaymentCreateResponse> {
  return apiClient<PaymentCreateResponse>("/api/payments/create-order", {
    method: "POST",
    body: JSON.stringify({ purchase_order_id: purchaseOrderId }),
  });
}

export async function verifyPayment(data: PaymentVerifyRequest): Promise<PaymentVerifyResponse> {
  return apiClient<PaymentVerifyResponse>("/api/payments/verify", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
