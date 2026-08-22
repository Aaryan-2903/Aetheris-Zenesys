import React from 'react';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { TriangleAlert, Clock, IndianRupee, ShieldAlert } from 'lucide-react';
import { decisionData } from '../../data/procurementData';
import { formatEnumLabel } from '../../utils/formatters';

interface DecisionCardProps {
  onApplyProtection: () => void;
  onReviewSupplier: () => void;
  requestName?: string;
  supplierName?: string;
  moneyAtRisk?: string;
  realData?: {
    status: string | null;
    actions: any[];
  };
}

export const DecisionCard: React.FC<DecisionCardProps> = ({
  onApplyProtection,
  onReviewSupplier,
  moneyAtRisk = decisionData.moneyAtRisk,
  realData
}) => {
  const getIcon = (id: string, index?: number) => {
    switch (id) {
      case 'price': return <TriangleAlert size={18} className="text-[#b42318]" />;
      case 'delivery': return <Clock size={18} className="text-[#b42318]" />;
      case 'exposure': return <IndianRupee size={18} className="text-[#b42318]" />;
      default: 
        if (index === 0) return <TriangleAlert size={18} className="text-[#b42318]" />;
        if (index === 1) return <Clock size={18} className="text-[#b42318]" />;
        return <ShieldAlert size={18} className="text-[#b42318]" />;
    }
  };

  const hasRealData = realData && realData.actions && realData.actions.length > 0;
  
  // Status label
  const rawStatus = realData?.status || "ACTION_REQUIRED";
  const humanStatus = formatEnumLabel(rawStatus);

  const title = decisionData.title;
  const description = decisionData.description;
  const recommendation = hasRealData 
    ? realData.actions[0].recommendation 
    : "protect the transaction before approval rather than simply rejecting the supplier.";

  return (
    <div className="bg-card border border-[#d8e5f7] rounded-[18px] shadow-card p-6 md:p-7 relative">
      <div className="flex justify-between items-start gap-4">
        <div>
          <Badge variant="red">{humanStatus}</Badge>
          <h2 className="text-xl md:text-2xl tracking-[-0.025em] font-semibold mt-3 mb-1 text-text">
            {title}
          </h2>
          <p className="text-[#656c78] leading-relaxed m-0 text-[14px] md:text-[15px]">{description}</p>
        </div>
      </div>

      <div className="my-5 md:my-6 p-4 md:p-5 rounded-[14px] bg-[#fff7f6] border border-[#ffe0dc] flex items-center justify-between">
        <div>
          <span className="text-xs text-[#777] block mb-0.5 font-medium">Estimated Money At Risk</span>
          <strong className="text-[28px] md:text-[34px] text-[#b42318] tracking-[-0.04em] tabular-nums leading-none block font-bold">
            {moneyAtRisk}
          </strong>
        </div>
        <span className="text-xs text-[#777] font-medium">{decisionData.status}</span>
      </div>

      <div className="text-[13px] md:text-[14px] font-bold text-text uppercase tracking-[0.05em] mt-5 mb-3">
        Why ProcuraIQ is flagging this
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {decisionData.signals.map((signal, idx) => (
          <div key={signal.id} className="p-4 border border-border rounded-xl bg-white/50">
            <div className="mb-2.5 flex items-center justify-between">
              {getIcon(signal.id, idx)}
              <span className="text-[10px] font-bold uppercase text-muted tracking-wider">0{idx + 1}</span>
            </div>
            <b className="block text-[13px] mb-1.5 text-text font-semibold">{signal.title}</b>
            <small className="text-muted leading-relaxed block text-xs">{signal.description}</small>
          </div>
        ))}
      </div>

      <div className="text-[14px] font-semibold mt-5 mb-2 text-text">Decision</div>
      <p className="text-[14px] md:text-[15px] text-text mb-4">
        <strong>Recommended:</strong> {recommendation}
      </p>

      <div className="flex flex-col sm:flex-row gap-2.5 mt-5">
        <Button variant="primary" onClick={onApplyProtection} className="w-full sm:w-auto px-6 py-2.5 font-semibold text-sm">
          Apply Protection Plan
        </Button>
        <Button variant="secondary" onClick={onReviewSupplier} className="w-full sm:w-auto px-6 py-2.5 font-semibold text-sm">
          Review Supplier
        </Button>
      </div>
    </div>
  );
};
