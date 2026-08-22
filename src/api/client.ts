// src/api/client.ts

// Base URL falls back to local dev server if env variable is missing
export const BASE_URL = import.meta.env?.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export class ApiError extends Error {
  public status: number;
  public data: any;

  constructor(status: number, message: string, data?: any) {
    super(message);
    this.status = status;
    this.data = data;
    this.name = "ApiError";
  }
}

interface FetchOptions extends RequestInit {
  params?: Record<string, string>;
}

export async function apiClient<T>(endpoint: string, options: FetchOptions = {}): Promise<T> {
  const { params, ...customConfig } = options;
  
  let url = `${BASE_URL}${endpoint}`;
  
  if (params) {
    const urlObj = new URL(url);
    Object.entries(params).forEach(([key, value]) => {
      urlObj.searchParams.append(key, value);
    });
    url = urlObj.toString();
  }

  const headers = {
    "Content-Type": "application/json",
    ...customConfig.headers,
  };

  const config: RequestInit = {
    ...customConfig,
    headers,
  };

  try {
    const response = await fetch(url, config);
    
    // Support blob response (like for PDFs)
    if (config.headers && (config.headers as Record<string, string>)["Accept"] === "application/pdf") {
      if (!response.ok) {
        throw new ApiError(response.status, `HTTP Error ${response.status}`);
      }
      return response.blob() as unknown as Promise<T>;
    }

    let data;
    try {
      data = await response.json();
    } catch (err) {
      // Empty response or non-JSON
      if (response.ok) return {} as T;
      throw new ApiError(response.status, `HTTP Error ${response.status}`);
    }

    if (!response.ok) {
      throw new ApiError(
        response.status,
        data.detail || data.message || `API Error: ${response.status}`,
        data
      );
    }

    return data as T;
  } catch (error: any) {
    if (error instanceof ApiError) throw error;
    throw new Error(`Network Error: ${error.message}`);
  }
}
