import React, { useState } from 'react';
import { Button } from '../components/ui/Button';
import { Toast } from '../components/ui/Toast';

import { useNavigate } from 'react-router-dom';

export const Negotiation: React.FC = () => {
  const navigate = useNavigate();
  const [toastMsg, setToastMsg] = useState<string | null>(null);

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
        <div>
          <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold">
            STRATEGIC SOURCING
          </div>
          <h1 className="text-[30px] md:text-[36px] tracking-[-0.035em] font-bold mt-1 mb-0.5 text-text">
            Negotiation Playbook
          </h1>
          <p className="text-[#5f6673] text-[14px] md:text-[15px] max-w-3xl leading-relaxed">
            Data-backed negotiation scripts, pricing delta leverage, and milestone contract terms generated from live signals.
          </p>
        </div>

        <Button variant="primary" onClick={() => navigate('/approval')} className="text-xs px-4 py-2.5">
          Proceed to Approvals
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 my-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-card border border-border rounded-[18px] shadow-card p-6">
            <div className="flex items-center gap-2 mb-3">
              <span className="text-[11px] uppercase tracking-wider font-bold bg-[#edf4ff] text-primary px-2.5 py-1 rounded-md">
                Active Negotiation Case: REQ-1002
              </span>
            </div>
            <h2 className="text-2xl font-bold text-text mb-1">IT Hardware Procurement — Apex Parts Intl.</h2>
            <p className="text-sm text-muted mb-5">Quoted: ₹1,25,000/unit · Benchmark Median: ₹1,10,000/unit · Units: 5</p>

            <div className="space-y-4">
              <div className="p-4 bg-[#f9f9fb] border border-border rounded-xl">
                <b className="text-xs uppercase font-bold text-muted block mb-1">Pricing Delta Leverage</b>
                <p className="text-sm text-text leading-relaxed">
                  The supplier's current quote exceeds median benchmark by <strong className="text-[#b42318]">+13.6% (+₹15,000/unit)</strong>. Total pricing variance is <strong>₹75,000</strong>.
                </p>
              </div>

              <div className="p-4 bg-[#f9f9fb] border border-border rounded-xl">
                <b className="text-xs uppercase font-bold text-muted block mb-1">Performance Risk Leverage</b>
                <p className="text-sm text-text leading-relaxed">
                  Supplier's on-time delivery rate is <strong className="text-warning">82%</strong> (down from historical 91%). Demand 30/70 payment milestones tied to delivery SLA penalty clauses.
                </p>
              </div>

              <div className="p-4 bg-[#f9f9fb] border border-border rounded-xl">
                <b className="text-xs uppercase font-bold text-muted block mb-2">Recommended Talking Points</b>
                <div className="space-y-2 text-sm text-text">
                  <div className="p-2.5 bg-white border border-border rounded-lg">
                    1. <em>"Our intelligence index indicates market median at ₹110K. We are prepared to commit immediately at ₹112K for 5 units."</em>
                  </div>
                  <div className="p-2.5 bg-white border border-border rounded-lg">
                    2. <em>"Due to recent delivery variance, we require advance payment reduced from 50% to 30%, with 70% paid post-inspection."</em>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <div className="bg-card border border-border rounded-[18px] shadow-card p-6">
            <h3 className="text-lg font-bold text-text mb-1">Target Outcome</h3>
            <p className="text-xs text-muted mb-4">Financial objectives for this negotiation</p>

            <div className="space-y-3 text-sm">
              <div className="flex justify-between py-2 border-b border-border">
                <span className="text-muted">Target Unit Price:</span>
                <span className="font-bold text-text">₹1,12,000</span>
              </div>
              <div className="flex justify-between py-2 border-b border-border">
                <span className="text-muted">Direct Cost Savings:</span>
                <span className="font-bold text-green">₹65,000</span>
              </div>
              <div className="flex justify-between py-2 border-b border-border">
                <span className="text-muted">Advance Exposure:</span>
                <span className="font-bold text-primary">30% (vs 50%)</span>
              </div>
              <div className="flex justify-between py-2">
                <span className="text-muted">SLA Penalty:</span>
                <span className="font-bold text-text">1% per day late</span>
              </div>
            </div>

            <Button 
              variant="primary" 
              onClick={() => setToastMsg("Negotiation summary exported to procurement folder.")}
              className="w-full justify-center mt-5 font-semibold text-sm py-2.5"
            >
              Export Negotiation Brief
            </Button>
          </div>
        </div>
      </div>

      <Toast message={toastMsg} onClose={() => setToastMsg(null)} />
    </div>
  );
};
