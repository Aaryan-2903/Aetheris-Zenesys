import React from 'react';
import { Button } from '../components/ui/Button';
import { useNavigate } from 'react-router-dom';


export const Comparison: React.FC = () => {
  const navigate = useNavigate();

  const vendors = [
    {
      id: "V-1001",
      name: "TechCorp Solutions",
      category: "IT Hardware",
      pricePerUnit: 112000,
      totalCost: 560000,
      deliveryReliability: "94%",
      qualityScore: "96%",
      leadTime: "10 Days",
      paymentTerms: "Net 45",
      compositeScore: "94.5%",
      recommended: true,
      exposure: "₹1.8L"
    },
    {
      id: "V-1002",
      name: "Apex Parts Intl.",
      category: "IT Hardware",
      pricePerUnit: 125000,
      totalCost: 625000,
      deliveryReliability: "82%",
      qualityScore: "90%",
      leadTime: "14 Days",
      paymentTerms: "Net 30 (50% Adv)",
      compositeScore: "81.2%",
      recommended: false,
      flag: "Price Anomaly (+13.6%)",
      exposure: "₹5.2L"
    },
    {
      id: "V-1003",
      name: "Global Mfg Inc.",
      category: "IT Hardware",
      pricePerUnit: 118000,
      totalCost: 590000,
      deliveryReliability: "88%",
      qualityScore: "89%",
      leadTime: "21 Days",
      paymentTerms: "Net 30",
      compositeScore: "85.0%",
      recommended: false,
      exposure: "₹2.6L"
    }
  ];

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <div>
          <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold">
            VENDOR INTELLIGENCE
          </div>
          <h1 className="text-[30px] md:text-[36px] tracking-[-0.035em] font-bold mt-1 mb-0.5 text-text">
            Supplier Comparison Scorecard
          </h1>
          <p className="text-[#5f6673] text-[14px] md:text-[15px] max-w-3xl leading-relaxed">
            Multi-dimensional evaluation ranked deterministically against price competitiveness, quality, delivery SLAs, and financial exposure.
          </p>
        </div>

        <Button variant="primary" onClick={() => navigate('/benchmark')} className="text-xs px-4 py-2.5">
          View Category Benchmarks
        </Button>
      </div>

      <div className="overflow-x-auto bg-card border border-border rounded-[18px] shadow-card">
        <table className="w-full border-collapse text-left text-sm">
          <thead>
            <tr className="bg-[#fafafd] border-b border-border">
              <th className="py-4 px-6 text-xs uppercase tracking-wider text-muted font-bold">Evaluation Metric</th>
              {vendors.map(v => (
                <th key={v.id} className="py-4 px-6 text-xs uppercase tracking-wider font-bold">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-text font-bold">{v.name}</span>
                    {v.recommended && (
                      <span className="text-[9px] bg-greenbg text-green px-2 py-0.5 rounded-full font-bold">
                        Top Rank
                      </span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border text-[13px]">
            <tr>
              <td className="py-3.5 px-6 font-semibold text-muted bg-[#fdfdfe]">Composite Score</td>
              {vendors.map(v => (
                <td key={v.id} className="py-3.5 px-6 font-bold text-primary text-base">
                  {v.compositeScore}
                </td>
              ))}
            </tr>
            <tr>
              <td className="py-3.5 px-6 font-semibold text-muted bg-[#fdfdfe]">Quoted Unit Price</td>
              {vendors.map(v => (
                <td key={v.id} className="py-3.5 px-6 font-bold text-text">
                  ₹{v.pricePerUnit.toLocaleString()}
                </td>
              ))}
            </tr>
            <tr>
              <td className="py-3.5 px-6 font-semibold text-muted bg-[#fdfdfe]">Total Order Value (5 units)</td>
              {vendors.map(v => (
                <td key={v.id} className="py-3.5 px-6 font-semibold text-text">
                  ₹{v.totalCost.toLocaleString()}
                </td>
              ))}
            </tr>
            <tr>
              <td className="py-3.5 px-6 font-semibold text-muted bg-[#fdfdfe]">Delivery Reliability</td>
              {vendors.map(v => (
                <td key={v.id} className="py-3.5 px-6 font-semibold">
                  <span className={Number(v.deliveryReliability.replace('%','')) < 85 ? 'text-warning' : 'text-text'}>
                    {v.deliveryReliability}
                  </span>
                </td>
              ))}
            </tr>
            <tr>
              <td className="py-3.5 px-6 font-semibold text-muted bg-[#fdfdfe]">Quality Rating</td>
              {vendors.map(v => (
                <td key={v.id} className="py-3.5 px-6 font-semibold text-text">
                  {v.qualityScore}
                </td>
              ))}
            </tr>
            <tr>
              <td className="py-3.5 px-6 font-semibold text-muted bg-[#fdfdfe]">Delivery Lead Time</td>
              {vendors.map(v => (
                <td key={v.id} className="py-3.5 px-6 text-text font-medium">
                  {v.leadTime}
                </td>
              ))}
            </tr>
            <tr>
              <td className="py-3.5 px-6 font-semibold text-muted bg-[#fdfdfe]">Payment Terms</td>
              {vendors.map(v => (
                <td key={v.id} className="py-3.5 px-6 text-text font-medium">
                  {v.paymentTerms}
                </td>
              ))}
            </tr>
            <tr>
              <td className="py-3.5 px-6 font-semibold text-muted bg-[#fdfdfe]">Financial Exposure (At Risk)</td>
              {vendors.map(v => (
                <td key={v.id} className="py-3.5 px-6 font-bold text-[#b42318]">
                  {v.exposure}
                </td>
              ))}
            </tr>
            <tr>
              <td className="py-4 px-6 font-semibold text-muted bg-[#fdfdfe]">Action</td>
              {vendors.map(v => (
                <td key={v.id} className="py-4 px-6">
                  {v.recommended ? (
                    <Button variant="primary" onClick={() => navigate('/po')} className="text-xs py-1.5 px-3">
                      Select Vendor
                    </Button>
                  ) : (
                    <Button variant="secondary" onClick={() => navigate('/negotiation')} className="text-xs py-1.5 px-3">
                      Negotiate Terms
                    </Button>
                  )}
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
