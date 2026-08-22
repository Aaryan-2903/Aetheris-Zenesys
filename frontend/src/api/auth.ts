import { apiClient, setAuthToken, removeAuthToken } from './client';

export interface UserSignup {
  name: string;
  email: string;
  password: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserResponse {
  user_id: string;
  name: string;
  email: string;
  role: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: UserResponse;
}

export const authApi = {
  signup: async (data: UserSignup): Promise<UserResponse> => {
    return apiClient<UserResponse>('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  login: async (data: UserLogin): Promise<TokenResponse> => {
    const res = await apiClient<TokenResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    if (res.access_token) {
      setAuthToken(res.access_token);
      localStorage.setItem('procuraiq_user', JSON.stringify(res.user));
    }
    return res;
  },

  me: async (): Promise<UserResponse> => {
    return apiClient<UserResponse>('/api/auth/me', {
      method: 'GET',
    });
  },

  logout: () => {
    removeAuthToken();
  }
};
