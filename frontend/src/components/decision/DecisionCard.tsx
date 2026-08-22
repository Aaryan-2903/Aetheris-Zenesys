import React from 'react';
import { Button } from '../ui/Button';
import { formatEnumLabel } from '../../utils/formatters';
import { TrendingDown, DollarSign, Activity, ShieldAlert, Sparkles, HelpCircle } from 'lucide-react';

interface DecisionCardProps {
  onApplyProtection?: () => void;
  onReviewSupplier?: () => void;
  requestName?: string;
  supplierName?: string;
  moneyAtRisk?: string;
  realData?: {
    status?: string | null;
    actions?: any[];
  };
}

export const DecisionCard: React.FC<DecisionCardProps> = ({ 
  onApplyProtection,
  onReviewSupplier,
  requestName = "IT Hardware Procurement",
  supplierName = "Apex Parts Intl.",
  moneyAtRisk = "₹5.2L",
  realData
}) => {
  const statusLabel = realData?.status 
    ? formatEnumLabel(realData.status) 
    : "Action Required";

  const getStatusBadgeStyle = () => {
    const s = statusLabel.toLowerCase();
    if (s.includes('proceed') || s.includes('no action')) {
      return 'bg-greenbg text-green border-[#b7eb8f]';
    }
    if (s.includes('approval') || s.includes('action required')) {
      return 'bg-redbg text-[#b42318] border-[#ffccc7]';
    }
    return 'bg-warningbg text-warning border-[#ffe58f]';
  };

  return (
    <div className="bg-card border border-border rounded-[18px] shadow-card p-6 md:p-[28px] relative overflow-hidden flex flex-col justify-between">
      {/* Top Header Badge & Identifier */}
      <div>
        <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
          <div className="flex items-center gap-2">
            <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border ${getStatusBadgeStyle()}`}>
              <span className="w-1.5 h-1.5 rounded-full bg-current"></span>
              {statusLabel}
            </span>
          </div>
          <span className="text-xs text-muted font-medium">
            Signal Velocity: <strong>High</strong>
          </span>
        </div>

        {/* Title and Supplier */}
        <h2 className="text-[24px] md:text-[28px] font-bold text-text tracking-tight m-0">
          {requestName}
        </h2>
        <div className="text-sm font-semibold text-muted mt-1 mb-5">
          Supplier: <span className="text-text font-bold">{supplierName}</span>
        </div>

        {/* HERO METRIC: Money At Risk */}
        <div className="p-4 md:p-5 rounded-2xl bg-[#fff5f5] border border-[#ffccc7] flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-6 shadow-xs">
          <div>
            <div className="text-[11px] font-bold uppercase tracking-[0.08em] text-[#b42318]">
              HERO METRIC · FINANCIAL EXPOSURE
            </div>
            <div className="text-[26px] md:text-[32px] font-bold text-[#b42318] tabular-nums tracking-tight mt-0.5">
              MONEY AT RISK: {moneyAtRisk}
            </div>
          </div>
          <div className="text-xs text-[#7a1b12] max-w-xs leading-relaxed">
            Direct unhedged capital exposed to delivery degradation and price benchmark variance before PO release.
          </div>
        </div>

        {/* WHY PROCURAIQ IS FLAGGING THIS */}
        <div className="mb-6">
          <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold mb-3 flex items-center gap-1.5">
            <HelpCircle size={14} className="text-primary" /> WHY PROCURAiQ IS FLAGGING THIS
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {/* Signal 1: Price Anomaly */}
            <div className="p-3.5 bg-[#f9f9fb] border border-border rounded-xl flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-redbg text-[#b42318] flex items-center justify-center flex-shrink-0 mt-0.5">
                <DollarSign size={16} />
              </div>
              <div>
                <b className="text-xs font-bold text-text block">Price Anomaly Detected</b>
                <p className="text-[12px] text-muted mt-0.5 leading-snug">
                  Current quote exceeds historical benchmark median by <strong>+13.6%</strong> (+₹15K/unit).
                </p>
              </div>
            </div>

            {/* Signal 2: Delivery Degradation */}
            <div className="p-3.5 bg-[#f9f9fb] border border-border rounded-xl flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-warningbg text-warning flex items-center justify-center flex-shrink-0 mt-0.5">
                <TrendingDown size={16} />
              </div>
              <div>
                <b className="text-xs font-bold text-text block">Delivery Performance Degradation</b>
                <p className="text-[12px] text-muted mt-0.5 leading-snug">
                  Supplier SLA adherence dropped to <strong>82%</strong> (down from historical 91%).
                </p>
              </div>
            </div>

            {/* Signal 3: Financial Exposure */}
            <div className="p-3.5 bg-[#f9f9fb] border border-border rounded-xl flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-[#edf4ff] text-primary flex items-center justify-center flex-shrink-0 mt-0.5">
                <ShieldAlert size={16} />
              </div>
              <div>
                <b className="text-xs font-bold text-text block">Unhedged Financial Exposure</b>
                <p className="text-[12px] text-muted mt-0.5 leading-snug">
                  50% upfront payment creates <strong>{moneyAtRisk}</strong> downside risk without milestone protection.
                </p>
              </div>
            </div>

            {/* Signal 4: ML Confidence / Risk Level */}
            <div className="p-3.5 bg-[#f9f9fb] border border-border rounded-xl flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-gray-100 text-muted flex items-center justify-center flex-shrink-0 mt-0.5">
                <Activity size={16} />
              </div>
              <div>
                <b className="text-xs font-bold text-text block">ML Prediction Confidence</b>
                <p className="text-[12px] text-muted mt-0.5 leading-snug">
                  Model confidence score: <strong>63.8%</strong> with heightened defect and delay probability.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* RECOMMENDED PROTECTION */}
        <div className="mb-6">
          <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold mb-3 flex items-center gap-1.5">
            <Sparkles size={14} className="text-primary" /> RECOMMENDED PROTECTION
          </div>

          <div className="space-y-2.5">
            <div className="p-3 bg-[#fafafd] border border-border rounded-xl flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-primary text-white font-bold text-xs flex items-center justify-center flex-shrink-0 mt-0.5">
                1
              </div>
              <div>
                <b className="text-xs font-bold text-text block">Milestone-based Payment Schedule</b>
                <span className="text-[12px] text-muted block">
                  Restructure 50% advance to 30% advance, with 70% paid post-inspection to hedge downside exposure.
                </span>
              </div>
            </div>

            <div className="p-3 bg-[#fafafd] border border-border rounded-xl flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-primary text-white font-bold text-xs flex items-center justify-center flex-shrink-0 mt-0.5">
                2
              </div>
              <div>
                <b className="text-xs font-bold text-text block">Delivery SLA Penalty Clause</b>
                <span className="text-[12px] text-muted block">
                  Include 1% per day late-delivery liquidated damages to offset performance degradation.
                </span>
              </div>
            </div>

            <div className="p-3 bg-[#fafafd] border border-border rounded-xl flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-primary text-white font-bold text-xs flex items-center justify-center flex-shrink-0 mt-0.5">
                3
              </div>
              <div>
                <b className="text-xs font-bold text-text block">Negotiate Quote Against Benchmark</b>
                <span className="text-[12px] text-muted block">
                  Target price adjustment to ₹112,000 to capture ₹65,000 in immediate cost savings.
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-wrap gap-2.5 pt-4 border-t border-border mt-2">
        <Button 
          variant="primary" 
          onClick={onApplyProtection}
          className="text-xs px-4 py-2.5 font-semibold"
        >
          Apply Protection Plan
        </Button>
        <Button 
          variant="secondary" 
          onClick={onReviewSupplier}
          className="text-xs px-4 py-2.5 font-semibold"
        >
          Review Supplier Scorecard
        </Button>
      </div>
    </div>
  );
};
