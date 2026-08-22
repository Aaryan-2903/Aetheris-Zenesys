import React, { useState } from 'react';
import { Button } from '../components/ui/Button';
import { Toast } from '../components/ui/Toast';
import { useNavigate } from 'react-router-dom';


export const Requirement: React.FC = () => {
  const navigate = useNavigate();
  const [toastMsg, setToastMsg] = useState<string | null>(null);

  const activeRequirements = [
    {
      id: "REQ-1002",
      title: "IT Hardware — Server Rack Upgrades",
      department: "Infrastructure Engineering",
      quantity: "5 Units",
      budget: "₹6,25,000",
      status: "EVALUATION_ACTIVE",
      priority: "HIGH",
      targetDate: "2026-09-15"
    },
    {
      id: "REQ-1001",
      title: "Industrial Fasteners & High-Tensile Bolts",
      department: "Manufacturing Operations",
      quantity: "500 Kg",
      budget: "₹2,10,000",
      status: "COMPLETED",
      priority: "MEDIUM",
      targetDate: "2026-08-30"
    },
    {
      id: "REQ-1003",
      title: "Raw Sheet Metal & Aluminum Extrusions",
      department: "Plant Production",
      quantity: "2 Tons",
      budget: "₹1,30,000",
      status: "APPROVAL_PENDING",
      priority: "HIGH",
      targetDate: "2026-09-01"
    }
  ];

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
        <div>
          <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold">
            PROCUREMENT INITIATION
          </div>
          <h1 className="text-[30px] md:text-[36px] tracking-[-0.035em] font-bold mt-1 mb-0.5 text-text">
            Procurement Requirements
          </h1>
          <p className="text-[#5f6673] text-[14px] md:text-[15px] max-w-3xl leading-relaxed">
            Specify technical parameters, quantity requirements, and target budgets to trigger ProcuraIQ intelligence signals.
          </p>
        </div>

        <Button variant="primary" onClick={() => navigate('/discovery')} className="text-xs px-4 py-2.5">
          Discover Qualified Vendors
        </Button>
      </div>

      <div className="bg-card border border-border rounded-[18px] shadow-card overflow-hidden my-6">
        <div className="p-5 border-b border-border">
          <h3 className="m-0 text-lg font-bold text-text">Active Requirements Pipeline</h3>
          <p className="text-xs text-muted mt-0.5">Specifications undergoing automated signal detection and risk modeling.</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-left text-sm whitespace-nowrap">
            <thead>
              <tr className="bg-[#fafafd] border-b border-border text-muted uppercase text-[10px] font-bold tracking-wider">
                <th className="py-4 px-6">ID</th>
                <th className="py-4 px-6">Requirement</th>
                <th className="py-4 px-6">Department</th>
                <th className="py-4 px-6">Quantity</th>
                <th className="py-4 px-6">Budget</th>
                <th className="py-4 px-6">Priority</th>
                <th className="py-4 px-6">Status</th>
                <th className="py-4 px-6">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border text-[13px]">
              {activeRequirements.map((req) => (
                <tr key={req.id} className="hover:bg-gray-50/70 transition-colors">
                  <td className="py-4 px-6 font-mono font-bold text-muted">{req.id}</td>
                  <td className="py-4 px-6 font-semibold text-text">{req.title}</td>
                  <td className="py-4 px-6 text-muted">{req.department}</td>
                  <td className="py-4 px-6 text-text font-medium">{req.quantity}</td>
                  <td className="py-4 px-6 font-bold text-text tabular-nums">{req.budget}</td>
                  <td className="py-4 px-6">
                    <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${
                      req.priority === 'HIGH' ? 'bg-redbg text-[#b42318]' : 'bg-gray-100 text-muted'
                    }`}>
                      {req.priority}
                    </span>
                  </td>
                  <td className="py-4 px-6">
                    <span className="text-[11px] font-semibold bg-[#eaf2ff] text-primary px-2.5 py-1 rounded-md">
                      {req.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="py-4 px-6">
                    <Button variant="secondary" onClick={() => navigate('/')} className="text-xs py-1.5 px-3">
                      Evaluate Signals
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <Toast message={toastMsg} onClose={() => setToastMsg(null)} />
    </div>
  );
};
