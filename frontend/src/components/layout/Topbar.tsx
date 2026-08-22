import React from 'react';
import { Search, Bell, HelpCircle, Menu, LogOut } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';

interface TopbarProps {
  onSearch: (query: string) => void;
  onToggleMobileMenu?: () => void;
}

export const Topbar: React.FC<TopbarProps> = ({ onSearch, onToggleMobileMenu }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const initial = user?.name ? user.name.charAt(0).toUpperCase() : 'A';

  return (
    <header className="h-[72px] border-b border-border bg-white/80 backdrop-blur-md flex items-center gap-[18px] px-4 md:px-[34px] sticky top-0 z-10">
      {onToggleMobileMenu && (
        <button 
          onClick={onToggleMobileMenu}
          className="md:hidden text-[#606673] hover:text-text p-2 rounded-lg hover:bg-gray-100 transition-colors"
          aria-label="Open Navigation Menu"
        >
          <Menu size={22} />
        </button>
      )}

      <div className="relative flex-1 max-w-[460px]">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-muted">
          <Search size={18} />
        </div>
        <input 
          className="w-full bg-[#f9f9fb] border border-border rounded-full py-2 pl-11 pr-4 text-sm text-text placeholder-muted focus:outline-none focus:border-primary focus:bg-white transition-colors"
          placeholder="Search procurement data..."
          onChange={(e) => onSearch(e.target.value)}
        />
      </div>
      
      <div className="ml-auto flex items-center gap-3 text-muted">
        <button className="hover:text-text transition-colors p-1.5 rounded-full hover:bg-gray-100">
          <Bell size={18} />
        </button>
        <button className="hover:text-text transition-colors p-1.5 rounded-full hover:bg-gray-100 hidden sm:block">
          <HelpCircle size={18} />
        </button>

        {user ? (
          <div className="flex items-center gap-2 pl-2 border-l border-border">
            <div className="w-[34px] h-[34px] rounded-full bg-[#dbe8f8] flex items-center justify-center text-navy font-bold text-xs border border-[#c3d8f2] shadow-xs" title={user.email}>
              {initial}
            </div>
            <span className="text-xs font-semibold text-text hidden sm:inline">{user.name}</span>
            <button 
              onClick={handleLogout}
              className="text-muted hover:text-[#b42318] p-1.5 rounded-md hover:bg-gray-100 transition-colors"
              title="Sign Out"
            >
              <LogOut size={16} />
            </button>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <button 
              onClick={() => navigate('/login')}
              className="text-xs font-semibold text-primary hover:underline px-2 py-1"
            >
              Sign In
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
