import { apiClient } from "./client";

export interface FeedbackSubmissionRequest {
  purchase_order_id: string;
  vendor_id: string;
  overall_rating: number;
  quality_rating: number;
  delivery_rating: number;
  responsiveness_rating: number;
  comments?: string;
}

export interface FeedbackResponse {
  feedback_id: string;
  purchase_order_id: string;
  vendor_id: string;
  overall_rating: number;
  quality_rating: number;
  delivery_rating: number;
  responsiveness_rating: number;
  comments?: string;
  created_at: string;
}

export interface VendorFeedbackSummary {
  vendor_id: string;
  feedback_count: number;
  average_overall_rating: number;
  average_quality_rating: number;
  average_delivery_rating: number;
  average_responsiveness_rating: number;
}

export async function submitFeedback(data: FeedbackSubmissionRequest): Promise<FeedbackResponse> {
  return apiClient<FeedbackResponse>("/api/feedback/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getVendorFeedbackSummary(vendorId: string): Promise<VendorFeedbackSummary> {
  return apiClient<VendorFeedbackSummary>(`/api/feedback/vendor/${vendorId}`, {
    method: "GET",
  });
}
