import React from 'react';
import { Button } from '../ui/Button';
import { protectionActions } from '../../data/procurementData';

interface ProtectionPanelProps {
  onGeneratePlan: () => void;
  onApplyProtection?: () => void;
}

export const ProtectionPanel: React.FC<ProtectionPanelProps> = ({ onGeneratePlan }) => {
  return (
    <div className="bg-card border border-border rounded-[18px] shadow-card p-6">
      <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold">Recommended Protection</div>
      <h3 className="mt-1 mb-1.5 text-xl font-semibold text-text">Reduce downside before approval</h3>
      <p className="text-[13px] text-muted mb-4">ProcuraIQ converts detected signals into practical procurement controls.</p>
      
      <div className="mb-5">
        {protectionActions.map(action => (
          <div key={action.id} className="flex gap-3 py-[13px] border-b border-border last:border-0 items-start">
            <div className="w-7 h-7 rounded-full bg-[#edf4ff] text-primary flex items-center justify-center text-[11px] font-bold flex-shrink-0 mt-0.5">
              {action.id}
            </div>
            <div>
              <b className="text-[13px] text-text font-semibold">{action.id} — {action.title}</b>
              <span className="block text-xs text-muted mt-0.5">{action.description}</span>
            </div>
          </div>
        ))}
      </div>

      <Button variant="primary" onClick={onGeneratePlan} className="w-full justify-center font-semibold text-sm py-2.5">
        Generate Negotiation Plan
      </Button>
    </div>
  );
};
