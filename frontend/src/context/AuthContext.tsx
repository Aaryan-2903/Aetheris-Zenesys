import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '../api/auth';
import type { UserResponse, UserLogin, UserSignup } from '../api/auth';
import { getAuthToken } from '../api/client';

interface AuthContextType {
  user: UserResponse | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (data: UserLogin) => Promise<void>;
  signup: (data: UserSignup) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = getAuthToken();
      if (!token) {
        setIsLoading(false);
        return;
      }
      try {
        const savedUser = localStorage.getItem('procuraiq_user');
        if (savedUser) {
          setUser(JSON.parse(savedUser));
        }
        const me = await authApi.me();
        setUser(me);
        localStorage.setItem('procuraiq_user', JSON.stringify(me));
      } catch (err) {
        console.warn("Session expired or invalid, logging out.");
        authApi.logout();
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = async (data: UserLogin) => {
    const res = await authApi.login(data);
    setUser(res.user);
  };

  const signup = async (data: UserSignup) => {
    await authApi.signup(data);
    await login({ email: data.email, password: data.password });
  };

  const logout = () => {
    authApi.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, isLoading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
