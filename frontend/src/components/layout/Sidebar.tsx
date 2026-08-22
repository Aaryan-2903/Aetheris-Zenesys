import React from 'react';
import { Target, FileText, Search, BarChart2, PieChart, DollarSign, MessageSquare, CheckSquare, FileDigit, Settings, HelpCircle, Plus, X } from 'lucide-react';
import { NavLink } from 'react-router-dom';

interface SidebarProps {
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
  onNewProcurement?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  mobileOpen = false,
  onCloseMobile,
  onNewProcurement
}) => {
  const mainNav = [
    { id: '/', label: 'Decision Center', icon: <Target size={18} /> },
    { id: '/requirement', label: 'Requirement', icon: <FileText size={18} /> },
    { id: '/discovery', label: 'Discovery', icon: <Search size={18} /> },
    { id: '/comparison', label: 'Comparison', icon: <BarChart2 size={18} /> },
    { id: '/benchmark', label: 'Benchmark', icon: <PieChart size={18} /> },
    { id: '/savings', label: 'Savings', icon: <DollarSign size={18} /> },
    { id: '/negotiation', label: 'Negotiation', icon: <MessageSquare size={18} /> },
    { id: '/approval', label: 'Approval', icon: <CheckSquare size={18} /> },
    { id: '/po', label: 'Purchase Order', icon: <FileDigit size={18} /> },
  ];

  const content = (
    <div className="w-[260px] bg-white border-r border-border p-5 flex flex-col h-full flex-shrink-0">
      <div className="flex items-center justify-between pt-1 pb-7">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-navy text-white flex items-center justify-center font-bold text-xl shadow-sm">
            P
          </div>
          <div>
            <b className="text-xl tracking-[-0.04em] block text-text leading-tight font-bold">ProcuraIQ</b>
            <small className="block text-muted text-[10px] tracking-[0.08em] uppercase font-semibold mt-0.5">Enterprise Procurement</small>
          </div>
        </div>
        {onCloseMobile && (
          <button 
            onClick={onCloseMobile} 
            className="md:hidden text-muted hover:text-text p-1"
            aria-label="Close Sidebar"
          >
            <X size={20} />
          </button>
        )}
      </div>
      
      <button 
        onClick={onNewProcurement}
        className="w-full bg-navy text-white rounded-full py-3 px-4 font-semibold text-sm flex items-center justify-center gap-2 hover:bg-[#00287a] transition-all mb-5 shadow-sm active:scale-[0.99]"
      >
        <Plus size={16} /> New Procurement
      </button>

      <nav className="flex flex-col gap-1 flex-1 overflow-y-auto">
        {mainNav.map(item => (
          <NavLink
            key={item.id}
            to={item.id}
            onClick={onCloseMobile}
            className={({ isActive }) => `w-full text-left px-3 py-2.5 rounded-lg flex items-center gap-3 transition-colors text-sm
              ${isActive 
                ? 'bg-[#eaf2ff] text-primary font-semibold' 
                : 'text-[#606673] hover:bg-[#eaf2ff] hover:text-primary hover:font-semibold'
              }`}
          >
            <span className="w-5 text-center flex justify-center">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="mt-auto pt-3 border-t border-border">
        <nav className="flex flex-col gap-1">
          <NavLink 
            to="/settings" 
            onClick={onCloseMobile}
            className="w-full text-left px-3 py-2.5 rounded-lg flex items-center gap-3 text-[#606673] hover:bg-[#eaf2ff] hover:text-primary text-sm transition-colors"
          >
            <span className="w-5 text-center flex justify-center"><Settings size={18} /></span> Settings
          </NavLink>
          <NavLink 
            to="/support" 
            onClick={onCloseMobile}
            className="w-full text-left px-3 py-2.5 rounded-lg flex items-center gap-3 text-[#606673] hover:bg-[#eaf2ff] hover:text-primary text-sm transition-colors"
          >
            <span className="w-5 text-center flex justify-center"><HelpCircle size={18} /></span> Support
          </NavLink>
        </nav>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop sidebar */}
      <aside className="hidden md:flex h-full flex-shrink-0 z-20">
        {content}
      </aside>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 md:hidden flex">
          <div 
            className="fixed inset-0 bg-black/30 backdrop-blur-xs transition-opacity" 
            onClick={onCloseMobile}
          />
          <div className="relative z-10 h-full shadow-2xl animate-in slide-in-from-left duration-200">
            {content}
          </div>
        </div>
      )}
    </>
  );
};
