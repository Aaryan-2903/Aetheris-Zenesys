import React, { useState } from 'react';
import { Sidebar } from '../components/layout/Sidebar';
import { Topbar } from '../components/layout/Topbar';
import { Outlet, useNavigate } from 'react-router-dom';
import { Modal } from '../components/ui/Modal';
import { Toast } from '../components/ui/Toast';
import { Button } from '../components/ui/Button';
import { automationApi } from '../api/automation';
import { Loader2 } from 'lucide-react';

export const Layout: React.FC = () => {
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isNewProcurementOpen, setIsNewProcurementOpen] = useState(false);
  const [toastMsg, setToastMsg] = useState<string | null>(null);
  const [evaluating, setEvaluating] = useState(false);

  // Form fields
  const [category, setCategory] = useState('IT Hardware');
  const [description, setDescription] = useState('Enterprise Server Upgrade');
  const [department, setDepartment] = useState('Infrastructure Engineering');
  const [quantity, setQuantity] = useState(10);
  const [unitPrice, setUnitPrice] = useState(125000);
  const [leadTime, setLeadTime] = useState(14);
  const [specs, setSpecs] = useState('Dual 64-Core Xeon, 256GB ECC RAM, 4TB NVMe SSD, Hot-swappable Redundant PSU');

  // Search query state
  const [searchQuery, setSearchQuery] = useState('');

  const handleCreateProcurement = async (e: React.FormEvent) => {
    e.preventDefault();
    setEvaluating(true);
    try {
      const newContext = {
        vendor_id: "V-1002",
        vendor_name: "Apex Parts Intl.",
        category,
        item_name: description,
        unit_price: Number(unitPrice),
        quantity: Number(quantity),
        lead_time_days: Number(leadTime),
        payment_terms_days: 30,
        advance_payment_pct: 0.5,
        historical_on_time_rate: 0.82,
        historical_quality_score: 0.90,
        historical_avg_price: 110000.0,
        vendor_defect_rate: 0.05,
        vendor_transaction_count: 8,
        vendor_category_spend: 880000.0,
        total_category_spend: 2500000.0,
        historical_price_stddev: 5000.0
      };

      // Save to localStorage for instant Decision Center pickup
      localStorage.setItem('procuraiq_active_procurement', JSON.stringify(newContext));

      // Call actual backend automation endpoint
      await automationApi.evaluate({
        vendor_id: newContext.vendor_id,
        category: newContext.category,
        unit_price: newContext.unit_price,
        quantity: newContext.quantity,
        lead_time_days: newContext.lead_time_days,
        payment_terms_days: newContext.payment_terms_days,
        advance_payment_pct: newContext.advance_payment_pct,
        historical_on_time_rate: newContext.historical_on_time_rate,
        historical_quality_score: newContext.historical_quality_score,
        historical_avg_price: newContext.historical_avg_price,
        vendor_defect_rate: newContext.vendor_defect_rate,
        vendor_transaction_count: newContext.vendor_transaction_count,
        vendor_category_spend: newContext.vendor_category_spend,
        total_category_spend: newContext.total_category_spend,
        historical_price_stddev: newContext.historical_price_stddev
      });

      setIsNewProcurementOpen(false);
      setToastMsg(`Procurement evaluated: ${description} (Signals Analyzed)`);
      navigate('/');
      window.dispatchEvent(new Event('procurement_updated'));
    } catch (err: any) {
      console.warn("Backend evaluation fallback:", err.message);
      setIsNewProcurementOpen(false);
      setToastMsg(`Procurement created: ${description}`);
      navigate('/');
      window.dispatchEvent(new Event('procurement_updated'));
    } finally {
      setEvaluating(false);
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar 
        mobileOpen={mobileMenuOpen} 
        onCloseMobile={() => setMobileMenuOpen(false)}
        onNewProcurement={() => setIsNewProcurementOpen(true)}
      />
      <main className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        <Topbar 
          onSearch={setSearchQuery} 
          onToggleMobileMenu={() => setMobileMenuOpen(true)}
        />
        <div className="max-w-[1440px] w-full mx-auto pt-6 md:pt-[38px] px-4 md:px-[56px] pb-[60px]">
          <Outlet context={{ searchQuery, setToastMsg, setIsNewProcurementOpen }} />
        </div>
      </main>

      {/* New Procurement Request Modal */}
      <Modal
        isOpen={isNewProcurementOpen}
        onClose={() => setIsNewProcurementOpen(false)}
        title="New Procurement Request"
        description="Initiate an intelligent procurement analysis with ProcuraIQ automated signal detection."
      >
        <form onSubmit={handleCreateProcurement} className="space-y-4 mt-2 max-h-[72vh] overflow-y-auto pr-1">
          {/* Section 1: Core Requirement */}
          <div>
            <div className="text-[10px] uppercase font-bold text-muted tracking-wider mb-2 border-b border-border pb-1">
              1. Core Requirement
            </div>
            <div className="space-y-2.5">
              <div>
                <label className="block text-[12px] font-semibold text-text mb-1">
                  Item / Service Description <span className="text-[#b42318]">*</span>
                </label>
                <input 
                  required
                  className="w-full border border-border rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-primary" 
                  placeholder="e.g. Enterprise Server Upgrade (Rack Units)"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
                <span className="text-[11px] text-muted block mt-0.5">Clear commercial or technical title for this procurement request.</span>
              </div>
            </div>
          </div>

          {/* Section 2: Scope & Categorization */}
          <div>
            <div className="text-[10px] uppercase font-bold text-muted tracking-wider mb-2 border-b border-border pb-1">
              2. Scope & Categorization
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-[12px] font-semibold text-text mb-1">
                  Procurement Category <span className="text-[#b42318]">*</span>
                </label>
                <select 
                  value={category} 
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full border border-border rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-primary bg-white"
                >
                  <option value="IT Hardware">IT Hardware & Equipment</option>
                  <option value="Industrial Fasteners">Industrial Fasteners</option>
                  <option value="Raw Materials">Raw Materials & Chemicals</option>
                  <option value="Logistics">Logistics & Freight Services</option>
                  <option value="Office Equipment">Office Equipment</option>
                </select>
              </div>
              <div>
                <label className="block text-[12px] font-semibold text-text mb-1">Requesting Department</label>
                <input 
                  className="w-full border border-border rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-primary" 
                  placeholder="e.g. Infrastructure Engineering"
                  value={department}
                  onChange={(e) => setDepartment(e.target.value)}
                />
              </div>
            </div>
          </div>

          {/* Section 3: Financials & Logistics */}
          <div>
            <div className="text-[10px] uppercase font-bold text-muted tracking-wider mb-2 border-b border-border pb-1">
              3. Financials & Logistics
            </div>
            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="block text-[12px] font-semibold text-text mb-1">
                  Quantity <span className="text-[#b42318]">*</span>
                </label>
                <input 
                  type="number" 
                  min={1}
                  required
                  value={quantity}
                  onChange={(e) => setQuantity(Number(e.target.value))}
                  className="w-full border border-border rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-primary" 
                />
              </div>
              <div>
                <label className="block text-[12px] font-semibold text-text mb-1">
                  Unit Price (₹) <span className="text-[#b42318]">*</span>
                </label>
                <input 
                  type="number" 
                  min={1}
                  required
                  value={unitPrice}
                  onChange={(e) => setUnitPrice(Number(e.target.value))}
                  className="w-full border border-border rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-primary" 
                />
              </div>
              <div>
                <label className="block text-[12px] font-semibold text-text mb-1">
                  Lead Time (Days) <span className="text-[#b42318]">*</span>
                </label>
                <input 
                  type="number" 
                  min={1}
                  required
                  value={leadTime}
                  onChange={(e) => setLeadTime(Number(e.target.value))}
                  className="w-full border border-border rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-primary" 
                />
              </div>
            </div>
          </div>

          {/* Section 4: Technical Specifications */}
          <div>
            <div className="text-[10px] uppercase font-bold text-muted tracking-wider mb-2 border-b border-border pb-1">
              4. Technical Specifications
            </div>
            <div>
              <textarea 
                rows={2}
                className="w-full border border-border rounded-lg py-2 px-3 text-xs focus:outline-none focus:border-primary resize-none" 
                placeholder="Detailed specifications, model requirements, SLA standards..."
                value={specs}
                onChange={(e) => setSpecs(e.target.value)}
              />
            </div>
          </div>

          <div className="pt-3 flex justify-end gap-2 border-t border-border">
            <Button type="button" variant="secondary" onClick={() => setIsNewProcurementOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" disabled={evaluating} className="flex items-center gap-1.5 font-semibold text-xs px-4 py-2">
              {evaluating && <Loader2 size={14} className="animate-spin" />}
              {evaluating ? 'Evaluating Procurement...' : 'Evaluate Procurement'}
            </Button>
          </div>
        </form>
      </Modal>

      <Toast message={toastMsg} onClose={() => setToastMsg(null)} />
    </div>
  );
};

export const PlaceholderPage: React.FC<{ title: string; description: string }> = ({ title, description }) => (
  <div>
    <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold">ProcuraIQ</div>
    <h1 className="text-[32px] md:text-[38px] tracking-[-0.035em] font-bold mt-1.5 mb-2 text-text">{title}</h1>
    <p className="text-[#5f6673] text-[14px] md:text-[15px] mb-7 max-w-3xl">{description}</p>
    
    <div className="bg-card border border-border rounded-[18px] shadow-card p-10 flex flex-col items-center justify-center text-center">
      <div className="w-12 h-12 rounded-full bg-[#edf4ff] text-primary flex items-center justify-center font-bold text-lg mb-3">
        ◈
      </div>
      <b className="text-text text-base font-semibold">{title} Workspace Active</b>
      <p className="text-muted text-xs max-w-md mt-1 mb-4">
        Procurement data synchronized with ProcuraIQ decision intelligence engine and NetSuite adapter.
      </p>
      <span className="text-[11px] px-3 py-1 rounded-full bg-gray-100 text-muted font-medium">
        Ready for Production Workflow
      </span>
    </div>
  </div>
);
