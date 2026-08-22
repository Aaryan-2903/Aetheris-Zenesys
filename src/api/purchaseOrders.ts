import { apiClient } from "./client";

export interface ReturnAndRefundPolicy {
  return_window_days: number;
  eligible_return_conditions: string;
  refund_method: string;
  refund_processing_days: number;
  return_shipping_responsibility: string;
  restocking_fee_percentage: number;
  non_returnable_conditions: string;
}

export interface PurchaseOrderRequest {
  procurement_request_id: string;
  vendor_id: string;
  category: string;
  item_description: string;
  quantity: number;
  unit_price: number;
  selected_warranty_plan?: string;
  warranty_fee?: number;
  insurance_provider?: string;
  insurance_cost?: number;
  payment_terms: string;
  expected_delivery_date: string;
  contract_id?: string;
  warranty_id?: string;
  insurance_id?: string;
  return_and_refund_policy?: ReturnAndRefundPolicy;
}

export interface PurchaseOrderResponse {
  purchase_order_id: string;
  procurement_request_id: string;
  vendor_id: string;
  vendor_name: string;
  category: string;
  item_description: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
  selected_warranty_plan?: string;
  warranty_fee?: number;
  insurance_provider?: string;
  insurance_cost?: number;
  total_amount: number;
  payment_terms: string;
  expected_delivery_date: string;
  contract_id?: string;
  warranty_id?: string;
  insurance_id?: string;
  return_and_refund_policy?: ReturnAndRefundPolicy;
  payment_status: string;
  status: string;
  order_tracking_status: string;
  tracking_updated_at: string;
  tracking_history: Array<{status: string, timestamp: string}>;
  razorpay_order_id?: string;
  razorpay_payment_id?: string;
  created_at: string;
}

export async function createPurchaseOrder(data: PurchaseOrderRequest): Promise<PurchaseOrderResponse> {
  return apiClient<PurchaseOrderResponse>("/api/purchase-orders/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getPurchaseOrder(purchaseOrderId: string): Promise<PurchaseOrderResponse> {
  return apiClient<PurchaseOrderResponse>(`/api/purchase-orders/${purchaseOrderId}`, {
    method: "GET",
  });
}

export async function getPurchaseOrderPdf(purchaseOrderId: string): Promise<Blob> {
  return apiClient<Blob>(`/api/purchase-orders/${purchaseOrderId}/pdf`, {
    method: "GET",
    headers: {
      "Accept": "application/pdf"
    }
  });
}
