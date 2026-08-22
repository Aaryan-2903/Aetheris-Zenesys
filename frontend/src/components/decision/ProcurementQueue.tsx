import React, { useState } from 'react';
import { procurementQueue } from '../../data/procurementData';
import { formatEnumLabel } from '../../utils/formatters';

interface ProcurementQueueProps {
  externalSearch?: string;
}

export const ProcurementQueue: React.FC<ProcurementQueueProps> = ({ externalSearch = '' }) => {
  const [internalSearch, setInternalSearch] = useState('');

  const activeSearch = externalSearch || internalSearch;

  const filteredQueue = procurementQueue.filter(item => 
    item.request.toLowerCase().includes(activeSearch.toLowerCase()) || 
    item.supplier.toLowerCase().includes(activeSearch.toLowerCase()) ||
    item.decision.toLowerCase().includes(activeSearch.toLowerCase())
  );

  const getPillStyles = (decision: string) => {
    const formatted = formatEnumLabel(decision).toLowerCase();
    const base = 'inline-block px-2.5 py-1 rounded-md text-[11px] font-semibold';
    
    if (formatted.includes('proceed')) {
      return `${base} bg-greenbg text-green`;
    }
    if (formatted.includes('approval') || formatted.includes('action')) {
      return `${base} bg-redbg text-[#b42318]`;
    }
    return `${base} bg-warningbg text-warning`;
  };

  return (
    <div className="bg-card border border-border rounded-[18px] shadow-card mt-6 overflow-hidden">
      <div className="p-5 px-6 border-b border-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div>
          <h3 className="m-0 text-lg font-semibold text-text">Live Procurement Queue</h3>
          <p className="text-xs text-muted mt-0.5">Continuous evaluation across active purchase pipelines</p>
        </div>
        <input 
          className="border border-border rounded-lg py-1.5 px-3 text-xs md:text-sm outline-none w-full sm:w-[220px] focus:border-primary transition-colors bg-white"
          placeholder="Filter requests..."
          value={internalSearch}
          onChange={(e) => setInternalSearch(e.target.value)}
        />
      </div>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left text-[13px] whitespace-nowrap">
          <thead>
            <tr className="bg-[#fafafd]">
              <th className="font-semibold text-[10px] uppercase tracking-[0.07em] text-muted py-3.5 px-6 border-b border-border">Request</th>
              <th className="font-semibold text-[10px] uppercase tracking-[0.07em] text-muted py-3.5 px-6 border-b border-border">Supplier</th>
              <th className="font-semibold text-[10px] uppercase tracking-[0.07em] text-muted py-3.5 px-6 border-b border-border">Exposure</th>
              <th className="font-semibold text-[10px] uppercase tracking-[0.07em] text-muted py-3.5 px-6 border-b border-border">Decision</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {filteredQueue.length > 0 ? (
              filteredQueue.map(item => (
                <tr key={item.id} className="hover:bg-gray-50/70 transition-colors cursor-pointer group">
                  <td className="py-4 px-6 font-semibold text-text">{item.request}</td>
                  <td className="py-4 px-6 text-text">{item.supplier}</td>
                  <td className="py-4 px-6 text-[#b42318] font-semibold tabular-nums">{item.exposure}</td>
                  <td className="py-4 px-6">
                    <span className={getPillStyles(item.decision)}>
                      {formatEnumLabel(item.decision)}
                    </span>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={4} className="py-8 text-center text-muted text-xs">
                  No matching procurement requests found in queue.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
