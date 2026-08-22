import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/Button';

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login({ email, password });
      navigate('/');
    } catch (err: any) {
      setError(err.message || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="bg-white border border-border rounded-2xl w-full max-w-md p-8 shadow-card">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-lg bg-navy text-white flex items-center justify-center font-bold text-xl shadow-sm">
            P
          </div>
          <div>
            <b className="text-xl tracking-tight block text-text font-bold leading-tight">ProcuraIQ</b>
            <small className="block text-muted text-[10px] tracking-wider uppercase font-semibold">Enterprise Procurement Intelligence</small>
          </div>
        </div>

        <h2 className="text-2xl font-bold text-text mb-1">Sign In</h2>
        <p className="text-sm text-muted mb-6">Access your procurement decision center</p>

        {error && (
          <div className="p-3 mb-4 rounded-lg bg-redbg text-[#b42318] text-xs font-semibold border border-[#ffccc7]">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-text mb-1 uppercase tracking-wider">Email Address</label>
            <input 
              type="email"
              required
              className="w-full border border-border rounded-lg py-2.5 px-3.5 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
              placeholder="buyer@enterprise.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-text mb-1 uppercase tracking-wider">Password</label>
            <input 
              type="password"
              required
              className="w-full border border-border rounded-lg py-2.5 px-3.5 text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <Button 
            type="submit" 
            variant="primary" 
            className="w-full justify-center py-2.5 mt-2 font-semibold text-sm"
            disabled={loading}
          >
            {loading ? 'Signing In...' : 'Sign In to Decision Center'}
          </Button>
        </form>

        <div className="mt-6 text-center text-xs text-muted">
          Don't have an account?{' '}
          <Link to="/signup" className="text-primary font-semibold hover:underline">
            Create Account
          </Link>
        </div>
      </div>
    </div>
  );
};
