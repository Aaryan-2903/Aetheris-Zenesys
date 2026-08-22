import React, { useState } from 'react';
import { Button } from '../components/ui/Button';
import { Toast } from '../components/ui/Toast';
import { ShieldCheck } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Approval: React.FC = () => {
  const navigate = useNavigate();
  const [toastMsg, setToastMsg] = useState<string | null>(null);

  const [approvalList, setApprovalList] = useState([
    {
      id: "REQ-1002",
      item: "IT Hardware Procurement (Server Upgrade)",
      supplier: "Apex Parts Intl.",
      amount: "₹6,25,000",
      exposure: "₹5.2L",
      trigger: "Price Variance (+13.6%) + Delivery Degradation",
      protectionPlan: "Milestone 30/70 + Delivery SLA",
      status: "PENDING_APPROVAL"
    },
    {
      id: "REQ-1003",
      item: "Raw Materials (Sheet Metal & Fasteners)",
      supplier: "Global Mfg Inc.",
      amount: "₹1,30,000",
      exposure: "₹1.3L",
      trigger: "Supplier Concentration Risk",
      protectionPlan: "Standard Warranty + 30 Days Replacement",
      status: "APPROVED"
    }
  ]);

  const handleAction = (id: string, newStatus: 'APPROVED' | 'REJECTED') => {
    setApprovalList(prev => prev.map(item => item.id === id ? { ...item, status: newStatus } : item));
    setToastMsg(`Procurement ${id} marked as ${newStatus.toLowerCase()}.`);
  };

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
        <div>
          <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold">
            GOVERNANCE & COMPLIANCE
          </div>
          <h1 className="text-[30px] md:text-[36px] tracking-[-0.035em] font-bold mt-1 mb-0.5 text-text">
            Procurement Approvals
          </h1>
          <p className="text-[#5f6673] text-[14px] md:text-[15px] max-w-3xl leading-relaxed">
            Multi-tier risk sign-off workflow. Transactions with Money At Risk exceeding ₹50,000 require mitigation compliance review.
          </p>
        </div>

        <Button variant="primary" onClick={() => navigate('/po')} className="text-xs px-4 py-2.5">
          Go to Purchase Orders
        </Button>
      </div>

      <div className="space-y-4 my-6">
        {approvalList.map(item => (
          <div key={item.id} className="bg-card border border-border rounded-[18px] shadow-card p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div className="space-y-1 max-w-2xl">
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs font-bold text-muted">{item.id}</span>
                <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full ${
                  item.status === 'APPROVED' ? 'bg-greenbg text-green' :
                  item.status === 'REJECTED' ? 'bg-redbg text-[#b42318]' : 'bg-warningbg text-warning'
                }`}>
                  {item.status.replace('_', ' ')}
                </span>
              </div>
              <h3 className="text-lg font-bold text-text">{item.item}</h3>
              <div className="text-xs text-muted">
                Supplier: <strong className="text-text">{item.supplier}</strong> · Total Amount: <strong className="text-text">{item.amount}</strong> · Money At Risk: <strong className="text-[#b42318]">{item.exposure}</strong>
              </div>
              <div className="text-xs text-text pt-2">
                <strong>Trigger Reason:</strong> {item.trigger}
              </div>
              <div className="text-xs text-primary font-medium flex items-center gap-1">
                <ShieldCheck size={14} /> <strong>Protection Bound:</strong> {item.protectionPlan}
              </div>
            </div>

            <div className="flex items-center gap-2 w-full md:w-auto">
              {item.status === 'PENDING_APPROVAL' ? (
                <>
                  <Button variant="secondary" onClick={() => handleAction(item.id, 'REJECTED')} className="text-xs py-2 px-3">
                    Reject
                  </Button>
                  <Button variant="primary" onClick={() => handleAction(item.id, 'APPROVED')} className="text-xs py-2 px-4">
                    Approve with Protection
                  </Button>
                </>
              ) : (
                <span className="text-xs font-semibold text-muted">
                  Decision Logged
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      <Toast message={toastMsg} onClose={() => setToastMsg(null)} />
    </div>
  );
};
