import React from 'react';
import { Button } from '../ui/Button';

interface ProtectionPanelProps {
  onGeneratePlan: () => void;
  onApplyProtection: () => void;
  onReviewSupplier?: () => void;
}

export const ProtectionPanel: React.FC<ProtectionPanelProps> = ({ 
  onGeneratePlan, 
  onApplyProtection,
  onReviewSupplier 
}) => {
  const protectionItems = [
    {
      id: "1",
      title: "Milestone-based payment",
      description: "Reduce upfront financial exposure."
    },
    {
      id: "2",
      title: "Delivery SLA clause",
      description: "Tie payment to delivery performance."
    },
    {
      id: "3",
      title: "Negotiate quote",
      description: "Use benchmark variance as leverage."
    }
  ];

  return (
    <div className="bg-card border border-border rounded-[18px] shadow-card p-6">
      <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold">RECOMMENDED PROTECTION</div>
      <h3 className="mt-1 mb-1 text-xl font-bold text-text">Reduce downside before approval</h3>
      <p className="text-[13px] text-muted mb-4">ProcuraIQ converts detected signals into practical procurement controls.</p>
      
      <div className="mb-5">
        {protectionItems.map(action => (
          <div key={action.id} className="flex gap-3 py-3 border-b border-border last:border-0 items-start">
            <div className="w-6 h-6 rounded-full bg-[#edf4ff] text-primary flex items-center justify-center text-[11px] font-bold flex-shrink-0 mt-0.5">
              {action.id}
            </div>
            <div>
              <b className="text-[13px] text-text font-semibold">{action.title}</b>
              <span className="block text-xs text-muted mt-0.5">{action.description}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="flex flex-col gap-2">
        <Button variant="primary" onClick={onGeneratePlan} className="w-full justify-center font-semibold text-sm py-2.5">
          Generate Negotiation Plan
        </Button>
        <div className="grid grid-cols-2 gap-2 mt-1">
          <Button variant="secondary" onClick={onApplyProtection} className="w-full justify-center text-xs py-2">
            Apply Protection
          </Button>
          {onReviewSupplier && (
            <Button variant="secondary" onClick={onReviewSupplier} className="w-full justify-center text-xs py-2">
              Review Supplier
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};
