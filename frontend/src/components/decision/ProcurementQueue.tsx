import React, { useState } from 'react';
import { formatEnumLabel } from '../../utils/formatters';
import { Button } from '../ui/Button';
import { useNavigate } from 'react-router-dom';

interface ProcurementQueueProps {
  externalSearch?: string;
}

export const ProcurementQueue: React.FC<ProcurementQueueProps> = ({ externalSearch = '' }) => {
  const navigate = useNavigate();
  const [internalSearch, setInternalSearch] = useState('');

  const queueItems = [
    {
      id: "1",
      request: "Industrial Fasteners",
      supplier: "Apex Parts Intl.",
      exposure: "₹2.1L",
      decision: "Review Price",
      status: "review"
    },
    {
      id: "2",
      request: "IT Hardware",
      supplier: "TechCorp Solutions",
      exposure: "₹1.8L",
      decision: "Proceed",
      status: "proceed"
    },
    {
      id: "3",
      request: "Raw Materials",
      supplier: "Global Mfg Inc.",
      exposure: "₹1.3L",
      decision: "Approval Required",
      status: "approval"
    },
    {
      id: "4",
      request: "Office Equipment",
      supplier: "Nexus Industries",
      exposure: "₹72K",
      decision: "Proceed",
      status: "proceed"
    }
  ];

  const activeSearch = externalSearch || internalSearch;

  const filteredQueue = queueItems.filter(item => 
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
          <h3 className="m-0 text-lg font-bold text-text">Procurement Decision Queue</h3>
          <p className="text-xs text-muted mt-0.5">Continuous signal monitoring and risk calculation across active procurement pipelines</p>
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
              <th className="font-semibold text-[10px] uppercase tracking-[0.07em] text-muted py-3.5 px-6 border-b border-border">Financial Exposure</th>
              <th className="font-semibold text-[10px] uppercase tracking-[0.07em] text-muted py-3.5 px-6 border-b border-border">Decision</th>
              <th className="font-semibold text-[10px] uppercase tracking-[0.07em] text-muted py-3.5 px-6 border-b border-border">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {filteredQueue.length > 0 ? (
              filteredQueue.map(item => (
                <tr key={item.id} className="hover:bg-gray-50/70 transition-colors cursor-pointer group">
                  <td className="py-4 px-6 font-semibold text-text">{item.request}</td>
                  <td className="py-4 px-6 text-text">{item.supplier}</td>
                  <td className="py-4 px-6 text-[#b42318] font-bold tabular-nums">{item.exposure}</td>
                  <td className="py-4 px-6">
                    <span className={getPillStyles(item.decision)}>
                      {formatEnumLabel(item.decision)}
                    </span>
                  </td>
                  <td className="py-4 px-6">
                    <Button 
                      variant="secondary" 
                      onClick={() => navigate('/negotiation')}
                      className="text-xs py-1 px-2.5"
                    >
                      Review
                    </Button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={5} className="py-8 text-center text-muted text-xs">
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
