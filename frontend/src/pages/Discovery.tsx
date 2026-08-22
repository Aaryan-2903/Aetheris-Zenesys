import React, { useState, useEffect } from 'react';
import { scoreApi } from '../api/score';
import type { VendorScoreResponseItem } from '../api/score';
import { Button } from '../components/ui/Button';
import { Search, CheckCircle, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const Discovery: React.FC = () => {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [scoredVendors, setScoredVendors] = useState<VendorScoreResponseItem[]>([]);
  const [loading, setLoading] = useState(false);

  const initialVendors = [
    {
      id: "V-1001",
      name: "TechCorp Solutions",
      category: "IT Hardware",
      location: "Bangalore, India",
      on_time_delivery_rate: 0.94,
      avg_quality_score: 0.96,
      vendor_price: 112000.0,
      actual_lead_time: 10,
      payment_terms_days: 45,
      rating: 4.8,
      verified: true
    },
    {
      id: "V-1002",
      name: "Apex Parts Intl.",
      category: "IT Hardware",
      location: "Mumbai, India",
      on_time_delivery_rate: 0.82,
      avg_quality_score: 0.90,
      vendor_price: 125000.0,
      actual_lead_time: 14,
      payment_terms_days: 30,
      rating: 4.1,
      verified: true
    },
    {
      id: "V-1003",
      name: "Global Mfg Inc.",
      category: "Raw Materials",
      location: "Chennai, India",
      on_time_delivery_rate: 0.88,
      avg_quality_score: 0.89,
      vendor_price: 95000.0,
      actual_lead_time: 21,
      payment_terms_days: 30,
      rating: 4.3,
      verified: true
    },
    {
      id: "V-1004",
      name: "Nexus Industries",
      category: "Office Equipment",
      location: "Pune, India",
      on_time_delivery_rate: 0.96,
      avg_quality_score: 0.92,
      vendor_price: 72000.0,
      actual_lead_time: 7,
      payment_terms_days: 60,
      rating: 4.7,
      verified: true
    }
  ];

  useEffect(() => {
    const fetchVendorScores = async () => {
      setLoading(true);
      try {
        const res = await scoreApi.rankVendors({
          budget_per_unit: 120000.0,
          required_lead_time: 14,
          vendors: initialVendors.map(v => ({
            vendor_id: v.id,
            on_time_delivery_rate: v.on_time_delivery_rate,
            avg_quality_score: v.avg_quality_score,
            vendor_price: v.vendor_price,
            actual_lead_time: v.actual_lead_time,
            payment_terms_days: v.payment_terms_days
          }))
        });
        setScoredVendors(res.ranked_vendors);
      } catch (err) {
        console.warn("Using local vendor intelligence:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchVendorScores();
  }, []);

  const filtered = initialVendors.filter(v => 
    v.name.toLowerCase().includes(search.toLowerCase()) || 
    v.category.toLowerCase().includes(search.toLowerCase()) ||
    v.location.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-2">
        <div>
          <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold">
            SUPPLIER INTELLIGENCE
          </div>
          <h1 className="text-[30px] md:text-[36px] tracking-[-0.035em] font-bold mt-1 mb-0.5 text-text">
            Vendor Discovery
          </h1>
          <p className="text-[#5f6673] text-[14px] md:text-[15px] max-w-3xl leading-relaxed">
            Discover, evaluate and qualify suppliers scored against real delivery reliability, price competitiveness, and quality ratings.
          </p>
        </div>

        <div className="w-full sm:w-auto">
          <Button variant="primary" onClick={() => navigate('/comparison')} className="w-full sm:w-auto text-xs px-4 py-2.5 flex items-center gap-1.5 justify-center">
            {loading && <Loader2 size={13} className="animate-spin" />}
            Compare Top Vendors
          </Button>
        </div>
      </div>

      <div className="my-5 relative max-w-md">
        <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-muted">
          <Search size={16} />
        </div>
        <input 
          className="w-full bg-white border border-border rounded-xl py-2.5 pl-10 pr-4 text-sm text-text placeholder-muted focus:outline-none focus:border-primary transition-all shadow-xs"
          placeholder="Search by supplier name, category, or region..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map(vendor => {
          const scoreInfo = scoredVendors.find(s => s.vendor_id === vendor.id);
          const compositeScore = scoreInfo ? (scoreInfo.final_score * 100).toFixed(1) : (vendor.on_time_delivery_rate * 100).toFixed(1);

          return (
            <div key={vendor.id} className="bg-card border border-border rounded-[18px] shadow-card p-5 flex flex-col justify-between hover:border-primary/40 transition-colors">
              <div>
                <div className="flex justify-between items-start gap-2 mb-2">
                  <div>
                    <span className="text-[10px] uppercase font-bold text-muted tracking-wider">{vendor.category}</span>
                    <h3 className="text-lg font-bold text-text flex items-center gap-1.5 mt-0.5">
                      {vendor.name}
                      {vendor.verified && <CheckCircle size={15} className="text-primary" />}
                    </h3>
                    <div className="text-xs text-muted mt-0.5">{vendor.location} · ID: {vendor.id}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-[10px] uppercase tracking-wider text-muted font-bold">ProcuraIQ Score</div>
                    <strong className="text-xl font-bold text-primary tabular-nums block">{compositeScore}%</strong>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-2 my-4 p-3 bg-[#f9f9fb] border border-border rounded-xl text-center">
                  <div>
                    <span className="text-[10px] uppercase text-muted block font-semibold">On-Time</span>
                    <strong className="text-xs font-bold text-text">{(vendor.on_time_delivery_rate * 100).toFixed(0)}%</strong>
                  </div>
                  <div>
                    <span className="text-[10px] uppercase text-muted block font-semibold">Quality</span>
                    <strong className="text-xs font-bold text-text">{(vendor.avg_quality_score * 100).toFixed(0)}%</strong>
                  </div>
                  <div>
                    <span className="text-[10px] uppercase text-muted block font-semibold">Lead Time</span>
                    <strong className="text-xs font-bold text-text">{vendor.actual_lead_time} Days</strong>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between pt-3 border-t border-border mt-2">
                <div>
                  <span className="text-[10px] uppercase text-muted font-bold block">Quoted Unit Price</span>
                  <strong className="text-sm font-bold text-text">₹{vendor.vendor_price.toLocaleString()}</strong>
                </div>
                <div className="flex gap-2">
                  <Button variant="secondary" onClick={() => navigate('/comparison')} className="text-xs py-1.5 px-3">
                    View Scorecard
                  </Button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
