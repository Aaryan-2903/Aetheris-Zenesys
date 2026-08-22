import React from 'react';
import { KPICard } from '../components/decision/KPICard';
import { Button } from '../components/ui/Button';
import { useNavigate } from 'react-router-dom';


export const Savings: React.FC = () => {
  const navigate = useNavigate();

  const savingsBreakdown = [
    {
      source: "Benchmark Negotiation",
      category: "IT Hardware",
      supplier: "Apex Parts Intl.",
      realized: "₹75,000",
      type: "Price Variance Capture",
      status: "Verified"
    },
    {
      source: "Milestone Advance Protection",
      category: "IT Infrastructure",
      supplier: "Apex Parts Intl.",
      realized: "₹2,25,000",
      type: "Advance Risk Hedging",
      status: "Active Bound"
    },
    {
      source: "Alternate Vendor Selection",
      category: "Raw Materials",
      supplier: "Global Mfg Inc.",
      realized: "₹1,40,000",
      type: "Direct Sourcing Optimization",
      status: "Verified"
    },
    {
      source: "SLA Delay Penalty Recovery",
      category: "Industrial Fasteners",
      supplier: "TechCorp Solutions",
      realized: "₹45,000",
      type: "Contract SLA Enforcement",
      status: "Recovered"
    }
  ];

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
        <div>
          <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold">
            FINANCIAL INTELLIGENCE
          </div>
          <h1 className="text-[30px] md:text-[36px] tracking-[-0.035em] font-bold mt-1 mb-0.5 text-text">
            Savings & Value Capture
          </h1>
          <p className="text-[#5f6673] text-[14px] md:text-[15px] max-w-3xl leading-relaxed">
            Audit trail of realized and potential cost savings achieved through ProcuraIQ decision intelligence and risk mitigation.
          </p>
        </div>

        <Button variant="primary" onClick={() => navigate('/negotiation')} className="text-xs px-4 py-2.5">
          Open Negotiation Hub
        </Button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 my-6">
        <KPICard label="Potential Savings" value="₹12.4M" trend="↑ 15.2% vs last quarter" isPositive />
        <KPICard label="Realized Savings" value="₹8.1M" trend="↑ 8.4% vs last quarter" isPositive />
        <KPICard label="Protected Capital" value="₹4.85L" desc="Unhedged advance risk eliminated" isPositive />
        <KPICard label="Negotiation ROI" value="18.4x" desc="Value captured per transaction" isPositive />
      </div>

      <div className="bg-card border border-border rounded-[18px] shadow-card overflow-hidden">
        <div className="p-5 border-b border-border">
          <h3 className="m-0 text-lg font-bold text-text">Realized Value Log</h3>
          <p className="text-xs text-muted mt-0.5">Verified cost reductions and contract protection capital savings.</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-left text-sm whitespace-nowrap">
            <thead>
              <tr className="bg-[#fafafd] border-b border-border text-muted uppercase text-[10px] font-bold tracking-wider">
                <th className="py-4 px-6">Source Strategy</th>
                <th className="py-4 px-6">Category</th>
                <th className="py-4 px-6">Supplier</th>
                <th className="py-4 px-6">Value Captured</th>
                <th className="py-4 px-6">Type</th>
                <th className="py-4 px-6">Audit Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border text-[13px]">
              {savingsBreakdown.map((item, idx) => (
                <tr key={idx} className="hover:bg-gray-50/70 transition-colors">
                  <td className="py-4 px-6 font-semibold text-text">{item.source}</td>
                  <td className="py-4 px-6 text-muted">{item.category}</td>
                  <td className="py-4 px-6 text-text font-medium">{item.supplier}</td>
                  <td className="py-4 px-6 font-bold text-green tabular-nums">{item.realized}</td>
                  <td className="py-4 px-6 text-muted">{item.type}</td>
                  <td className="py-4 px-6">
                    <span className="text-[11px] font-semibold bg-greenbg text-green px-2.5 py-1 rounded-md">
                      {item.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
