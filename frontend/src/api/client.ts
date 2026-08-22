export const BASE_URL = import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL || "https://aetheris-zenesys.onrender.com";

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

export function getAuthToken(): string | null {
  return localStorage.getItem("procuraiq_token");
}

export function setAuthToken(token: string) {
  localStorage.setItem("procuraiq_token", token);
}

export function removeAuthToken() {
  localStorage.removeItem("procuraiq_token");
  localStorage.removeItem("procuraiq_user");
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

  const token = getAuthToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(customConfig.headers as Record<string, string>),
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
    } catch {
      if (response.ok) return {} as T;
      throw new ApiError(response.status, `HTTP Error ${response.status}`);
    }

    if (!response.ok) {
      if (response.status === 401) {
        removeAuthToken();
      }
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
