import React from 'react';
import { Button } from '../components/ui/Button';
import { KPICard } from '../components/decision/KPICard';
import { useNavigate } from 'react-router-dom';


export const Benchmark: React.FC = () => {
  const navigate = useNavigate();

  const benchmarkCategories = [
    {
      category: "IT Hardware & Servers",
      currentQuote: "₹125,000",
      marketMedian: "₹110,000",
      variancePct: "+13.6%",
      potentialSavings: "₹75,000",
      trend: "Rising +2.4% Q3",
      status: "Above Benchmark"
    },
    {
      category: "Industrial Fasteners",
      currentQuote: "₹450/kg",
      marketMedian: "₹410/kg",
      variancePct: "+9.7%",
      potentialSavings: "₹38,000",
      trend: "Stable",
      status: "Above Benchmark"
    },
    {
      category: "Raw Materials & Steel",
      currentQuote: "₹68,000/ton",
      marketMedian: "₹67,500/ton",
      variancePct: "+0.7%",
      potentialSavings: "₹12,000",
      trend: "Falling -1.8%",
      status: "Market Aligned"
    },
    {
      category: "Office & Facility Supplies",
      currentQuote: "₹72,000",
      marketMedian: "₹74,000",
      variancePct: "-2.7%",
      potentialSavings: "₹0",
      trend: "Stable",
      status: "Below Benchmark"
    }
  ];

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4">
        <div>
          <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold">
            MARKET BENCHMARKS
          </div>
          <h1 className="text-[30px] md:text-[36px] tracking-[-0.035em] font-bold mt-1 mb-0.5 text-text">
            Category Price Benchmarks
          </h1>
          <p className="text-[#5f6673] text-[14px] md:text-[15px] max-w-3xl leading-relaxed">
            Real-time market price indices and supplier quote variance across active procurement categories.
          </p>
        </div>

        <Button variant="primary" onClick={() => navigate('/savings')} className="text-xs px-4 py-2.5">
          View Realized Savings
        </Button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 my-6">
        <KPICard label="Median Price Index" value="₹110.0K" trend="Standard specification base" />
        <KPICard label="Max Category Variance" value="+13.6%" trend="IT Hardware (Apex Parts)" highlight />
        <KPICard label="Total Addressable Variance" value="₹1.25L" trend="Potential direct savings" isPositive />
      </div>

      <div className="bg-card border border-border rounded-[18px] shadow-card overflow-hidden">
        <div className="p-5 border-b border-border">
          <h3 className="m-0 text-lg font-bold text-text">Category Price Index</h3>
          <p className="text-xs text-muted mt-0.5">Calculated from historical procurement data and verified supplier transactions.</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-left text-sm whitespace-nowrap">
            <thead>
              <tr className="bg-[#fafafd] border-b border-border text-muted uppercase text-[10px] font-bold tracking-wider">
                <th className="py-4 px-6">Category</th>
                <th className="py-4 px-6">Quoted Price</th>
                <th className="py-4 px-6">Market Median</th>
                <th className="py-4 px-6">Variance</th>
                <th className="py-4 px-6">Savings Potential</th>
                <th className="py-4 px-6">Position</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border text-[13px]">
              {benchmarkCategories.map((item, idx) => (
                <tr key={idx} className="hover:bg-gray-50/70 transition-colors">
                  <td className="py-4 px-6 font-semibold text-text">{item.category}</td>
                  <td className="py-4 px-6 font-bold text-text">{item.currentQuote}</td>
                  <td className="py-4 px-6 text-muted font-medium">{item.marketMedian}</td>
                  <td className="py-4 px-6 font-bold text-[#b42318]">{item.variancePct}</td>
                  <td className="py-4 px-6 font-bold text-green">{item.potentialSavings}</td>
                  <td className="py-4 px-6">
                    <span className={`text-[11px] font-semibold px-2.5 py-1 rounded-md ${
                      item.status === 'Above Benchmark' ? 'bg-redbg text-[#b42318]' :
                      item.status === 'Below Benchmark' ? 'bg-greenbg text-green' : 'bg-gray-100 text-muted'
                    }`}>
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
