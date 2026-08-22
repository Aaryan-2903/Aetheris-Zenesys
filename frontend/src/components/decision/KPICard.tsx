import React from 'react';

interface KPICardProps {
  label: string;
  value: string;
  trend?: string;
  desc?: string;
  isPositive?: boolean;
  highlight?: boolean;
}

export const KPICard: React.FC<KPICardProps> = ({ 
  label, 
  value, 
  trend, 
  desc, 
  isPositive = false,
  highlight = false 
}) => {
  return (
    <div className={`bg-card border rounded-[18px] shadow-card p-[22px] relative overflow-hidden group hover:shadow-md transition-all ${
      highlight ? 'border-[#ffccc7] bg-[#fffaf9]' : 'border-border'
    }`}>
      <div className={`absolute -right-6 -top-6 w-[90px] h-[90px] rounded-full transition-transform group-hover:scale-110 ${
        highlight ? 'bg-[#ff4d4f0a]' : 'bg-[#0066cc08]'
      }`} />
      
      <div className="flex items-center justify-between relative z-10">
        <div className={`text-[11px] uppercase tracking-[0.07em] font-semibold ${
          highlight ? 'text-[#b42318]' : 'text-muted'
        }`}>
          {label}
        </div>
        {highlight && (
          <span className="text-[10px] uppercase font-bold text-[#b42318] bg-redbg px-2 py-0.5 rounded-full tracking-wider">
            At Risk
          </span>
        )}
      </div>

      <div className={`text-[32px] md:text-[34px] font-bold tracking-[-0.04em] mt-2.5 mb-1 tabular-nums relative z-10 ${
        highlight ? 'text-[#b42318]' : 'text-text'
      }`}>
        {value}
      </div>
      
      {trend && (
        <div className={`text-xs ${isPositive ? 'text-green font-medium' : 'text-muted'} relative z-10`}>
          {trend}
        </div>
      )}
      {desc && (
        <div className="text-xs text-muted relative z-10">
          {desc}
        </div>
      )}
    </div>
  );
};
