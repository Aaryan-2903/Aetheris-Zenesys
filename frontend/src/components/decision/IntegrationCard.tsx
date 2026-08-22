import React from 'react';

export const IntegrationCard: React.FC = () => {
  return (
    <div className="mt-4 bg-card border border-border rounded-[18px] shadow-card p-5">
      <div className="flex justify-between items-center">
        <div>
          <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold">Enterprise ERP</div>
          <b className="text-[15px] font-bold text-text mt-0.5 block">Oracle NetSuite</b>
          <div className="text-[12px] text-muted mt-0.5">SuiteCloud Integration</div>
        </div>
        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-[#eaf2ff] text-primary">
          <span className="text-[9px]">●</span> SuiteCloud Ready
        </div>
      </div>
    </div>
  );
};
