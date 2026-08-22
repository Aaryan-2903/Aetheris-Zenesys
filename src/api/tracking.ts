import { apiClient } from "./client";

export interface TrackingHistoryEvent {
  status: string;
  timestamp: string;
}

export interface OrderTrackingResponse {
  purchase_order_id: string;
  tracking_status: string;
  expected_delivery_date: string;
  tracking_updated_at: string;
  tracking_history: TrackingHistoryEvent[];
  valid_next_statuses: string[];
  current_status: string;
  completed_steps: string[];
  next_step?: string;
}

export async function getOrderTracking(purchaseOrderId: string): Promise<OrderTrackingResponse> {
  return apiClient<OrderTrackingResponse>(`/api/purchase-orders/${purchaseOrderId}/tracking`, {
    method: "GET",
  });
}

export async function updateOrderTracking(purchaseOrderId: string, status: string): Promise<OrderTrackingResponse> {
  return apiClient<OrderTrackingResponse>(`/api/purchase-orders/${purchaseOrderId}/tracking`, {
    method: "POST",
    body: JSON.stringify({ status }),
  });
}
