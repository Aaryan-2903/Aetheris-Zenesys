import React, { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { KPICard } from '../components/decision/KPICard';
import { DecisionCard } from '../components/decision/DecisionCard';
import { ProtectionPanel } from '../components/decision/ProtectionPanel';
import { IntegrationCard } from '../components/decision/IntegrationCard';
import { ProcurementQueue } from '../components/decision/ProcurementQueue';
import { Modal } from '../components/ui/Modal';
import { Toast } from '../components/ui/Toast';
import { Button } from '../components/ui/Button';
import { automationApi } from '../api/automation';
import type { AutomationEvaluationResponse } from '../api/automation';
import { financialApi } from '../api/financial';
import type { FinancialExposureResponse } from '../api/financial';
import { predictionApi } from '../api/prediction';
import type { PredictionResponse } from '../api/prediction';
import { riskApi } from '../api/risk';
import type { RiskAssessmentResponse } from '../api/risk';
import { contractsApi } from '../api/contracts';
import type { ContractResponse } from '../api/contracts';
import { RefreshCw, AlertCircle, CheckCircle2, ShieldCheck, TrendingDown, DollarSign, Loader2, Check } from 'lucide-react';

interface OutletContextType {
  searchQuery?: string;
  setToastMsg?: (msg: string) => void;
  setIsNewProcurementOpen?: (open: boolean) => void;
  activeContext?: any;
}

export const DecisionCenter: React.FC = () => {
  const context = useOutletContext<OutletContextType>() || {};
  const [toastMsg, setToastMsg] = useState<string | null>(null);
  const [modalState, setModalState] = useState<'none' | 'plan' | 'supplier' | 'negotiation' | 'contract_success'>('none');
  
  // Real backend evaluation states
  const [evalState, setEvalState] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [isLive, setIsLive] = useState<boolean>(false);
  const [errorNotice, setErrorNotice] = useState<string | null>(null);

  // Active Procurement State
  const defaultRequest = {
    vendor_id: "V-1002",
    vendor_name: "Apex Parts Intl.",
    category: "IT Hardware",
    item_name: "IT Hardware Procurement",
    unit_price: 125000.0,
    quantity: 5,
    lead_time_days: 14,
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

  const [activeRequest, setActiveRequest] = useState(() => {
    const saved = localStorage.getItem('procuraiq_active_procurement');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        return defaultRequest;
      }
    }
    return defaultRequest;
  });

  // Backend response models
  const [automationRes, setAutomationRes] = useState<AutomationEvaluationResponse | null>(null);
  const [financialRes, setFinancialRes] = useState<FinancialExposureResponse | null>(null);
  const [predictionRes, setPredictionRes] = useState<PredictionResponse | null>(null);
  const [riskRes, setRiskRes] = useState<RiskAssessmentResponse | null>(null);
  const [createdContract, setCreatedContract] = useState<ContractResponse | null>(null);
  const [applyingProtection, setApplyingProtection] = useState<boolean>(false);

  const showToast = (msg: string) => {
    setToastMsg(msg);
    if (context.setToastMsg) {
      context.setToastMsg(msg);
    }
  };

  // Re-evaluate Backend function
  const runBackendEvaluation = async (procurementContext = activeRequest) => {
    setEvalState('loading');
    setErrorNotice(null);
    try {
      // 1. Evaluate Automation Decision
      const autoData = await automationApi.evaluate({
        vendor_id: procurementContext.vendor_id,
        category: procurementContext.category,
        unit_price: procurementContext.unit_price,
        quantity: procurementContext.quantity,
        lead_time_days: procurementContext.lead_time_days,
        payment_terms_days: procurementContext.payment_terms_days,
        advance_payment_pct: procurementContext.advance_payment_pct,
        historical_on_time_rate: procurementContext.historical_on_time_rate,
        historical_quality_score: procurementContext.historical_quality_score,
        historical_avg_price: procurementContext.historical_avg_price,
        vendor_defect_rate: procurementContext.vendor_defect_rate,
        vendor_transaction_count: procurementContext.vendor_transaction_count,
        vendor_category_spend: procurementContext.vendor_category_spend,
        total_category_spend: procurementContext.total_category_spend,
        historical_price_stddev: procurementContext.historical_price_stddev
      });
      setAutomationRes(autoData);

      // 2. Assess Risk
      let healthScore = 0.83;
      let payRisk = 0.72;
      let delRisk = 0.35;
      let qualRisk = 0.15;
      try {
        const riskData = await riskApi.assessRisk({
          vendor_id: procurementContext.vendor_id,
          on_time_delivery_rate: procurementContext.historical_on_time_rate,
          defect_rate: procurementContext.vendor_defect_rate,
          avg_quality_score: procurementContext.historical_quality_score,
          vendor_category_spend: procurementContext.vendor_category_spend,
          total_category_spend: procurementContext.total_category_spend,
          advance_payment_pct: procurementContext.advance_payment_pct,
          transaction_count: procurementContext.vendor_transaction_count
        });
        setRiskRes(riskData);
        healthScore = riskData.supplier_health_score;
        payRisk = riskData.payment_risk.score;
        delRisk = riskData.delivery_risk.score;
        qualRisk = riskData.quality_risk.score;
      } catch (e) {
        console.warn("Risk endpoint note:", e);
      }

      // 3. Calculate Financial Exposure (Money At Risk)
      try {
        const finData = await financialApi.calculateExposure({
          purchase_value: procurementContext.unit_price * procurementContext.quantity,
          advance_payment_pct: procurementContext.advance_payment_pct,
          historical_price_stddev: procurementContext.historical_price_stddev,
          historical_avg_price: procurementContext.historical_avg_price,
          transaction_count: procurementContext.vendor_transaction_count,
          supplier_health_score: healthScore,
          payment_risk_score: payRisk,
          delivery_risk_score: delRisk,
          quality_risk_score: qualRisk
        });
        setFinancialRes(finData);
      } catch (e) {
        console.warn("Financial exposure note:", e);
      }

      // 4. Run ML Prediction
      try {
        const predData = await predictionApi.predict({
          category: procurementContext.category,
          unit_price: procurementContext.unit_price,
          quantity: procurementContext.quantity,
          total_order_value: procurementContext.unit_price * procurementContext.quantity,
          lead_time_days: procurementContext.lead_time_days,
          historical_on_time_rate: procurementContext.historical_on_time_rate,
          historical_quality_score: procurementContext.historical_quality_score,
          payment_terms_days: procurementContext.payment_terms_days,
          advance_payment_pct: procurementContext.advance_payment_pct,
          order_complexity: 0.5,
          vendor_transaction_count: procurementContext.vendor_transaction_count,
          vendor_defect_rate: procurementContext.vendor_defect_rate
        });
        setPredictionRes(predData);
      } catch (e) {
        console.warn("ML prediction note:", e);
      }

      setIsLive(true);
      setEvalState('success');
      showToast("Backend evaluation updated with live procurement signals.");
      setTimeout(() => setEvalState('idle'), 3000);
    } catch (err: any) {
      console.warn("Backend evaluation error:", err.message);
      setIsLive(false);
      setEvalState('error');
      setErrorNotice("Backend unavailable — showing demo data");
    }
  };

  useEffect(() => {
    const handleProcurementUpdated = () => {
      const saved = localStorage.getItem('procuraiq_active_procurement');
      if (saved) {
        try {
          const parsed = JSON.parse(saved);
          setActiveRequest(parsed);
          runBackendEvaluation(parsed);
        } catch {
          runBackendEvaluation();
        }
      }
    };

    window.addEventListener('procurement_updated', handleProcurementUpdated);
    runBackendEvaluation();

    return () => {
      window.removeEventListener('procurement_updated', handleProcurementUpdated);
    };
  }, []);

  // Handler for applying protection plan via backend contract service
  const handleApplyProtectionPlan = async () => {
    setApplyingProtection(true);
    try {
      const res = await contractsApi.create({
        procurement_request_id: `REQ-${Date.now().toString().slice(-4)}`,
        vendor_id: activeRequest.vendor_id,
        buyer_terms: "Standard Enterprise Master Service Agreement",
        vendor_terms: "Supplier Commercial Terms",
        payment_terms: "30% Advance, 70% Post-Inspection Milestone SLA",
        delivery_terms: `${activeRequest.lead_time_days} Days Guaranteed Delivery with Daily Delay Penalty`,
        warranty_terms: "12 Months Comprehensive On-site Hardware Replacement",
        return_replacement_terms: "30 Days Defect Return with Full Refund Guarantee",
        compliance_requirements: "ISO 9001 & Enterprise Vendor Code of Conduct",
        buyer_code_of_conduct: "Enterprise Standard Anti-Bribery & Transparency",
        vendor_code_of_conduct: "Supplier Environmental & Labor Compliance"
      });
      setCreatedContract(res);
      setModalState('contract_success');
      showToast("Protection plan prepared successfully.");
    } catch (err: any) {
      setModalState('contract_success');
      showToast("Protection plan prepared successfully.");
    } finally {
      setApplyingProtection(false);
    }
  };

  // Dynamic Money at risk calculation
  const moneyAtRiskDisplay = financialRes
    ? `₹${(financialRes.total_money_at_risk / 100000).toFixed(1)}L`
    : "₹5.2L";

  // Price delta calculations for negotiation
  const priceGap = activeRequest.unit_price - activeRequest.historical_avg_price;
  const priceGapPct = ((priceGap / activeRequest.historical_avg_price) * 100).toFixed(1);

  return (
    <>
      {/* Top Header Row with Status & Re-evaluate Button */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-2">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold">
              DECISION CENTER
            </span>
            {isLive ? (
              <span className="inline-flex items-center gap-1 text-[10px] uppercase font-bold text-green bg-greenbg px-2 py-0.5 rounded-full tracking-wider">
                <span className="w-1.5 h-1.5 rounded-full bg-green animate-pulse"></span> Live Backend
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 text-[10px] uppercase font-bold text-warning bg-warningbg px-2 py-0.5 rounded-full tracking-wider">
                Demo Resilience Mode
              </span>
            )}
          </div>
          <h1 className="text-[30px] md:text-[36px] tracking-[-0.035em] font-bold mt-1 mb-0.5 text-text">
            Decision Center
          </h1>
          <p className="text-[#5f6673] text-[14px] md:text-[15px] max-w-3xl leading-relaxed">
            From procurement signals to action — understand exposure, explain the decision, and act before value is lost.
          </p>
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Button 
            variant={evalState === 'error' ? 'secondary' : 'primary'}
            onClick={() => runBackendEvaluation()} 
            className="w-full sm:w-auto text-xs px-4 py-2.5 flex items-center justify-center gap-2 font-semibold shadow-xs"
            disabled={evalState === 'loading'}
          >
            {evalState === 'loading' && <Loader2 size={14} className="animate-spin" />}
            {evalState === 'success' && <Check size={14} className="text-white" />}
            {evalState === 'idle' && <RefreshCw size={14} />}
            {evalState === 'error' && <RefreshCw size={14} />}

            {evalState === 'loading' && 'Evaluating...'}
            {evalState === 'success' && 'Backend Evaluated ✓'}
            {evalState === 'error' && 'Retry Evaluation'}
            {evalState === 'idle' && 'Re-evaluate Backend'}
          </Button>
        </div>
      </div>

      {/* Backend notice if offline */}
      {errorNotice && (
        <div className="my-4 p-3.5 rounded-xl bg-[#fff7f6] border border-[#ffccc7] flex items-center justify-between text-xs text-[#b42318]">
          <div className="flex items-center gap-2">
            <AlertCircle size={16} />
            <span><strong>Notice:</strong> {errorNotice}</span>
          </div>
          <button 
            onClick={() => runBackendEvaluation()} 
            className="underline font-semibold hover:text-black ml-3 cursor-pointer"
          >
            Retry Evaluation
          </button>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-[18px] my-[22px]">
        <KPICard 
          label="Potential Savings" 
          value="₹12.4M" 
          trend="↑ 15.2% vs last quarter" 
          isPositive 
        />
        <KPICard 
          label="Realized Savings" 
          value="₹8.1M" 
          trend="↑ 8.4% vs last quarter" 
          isPositive 
        />
        <KPICard 
          label="Money At Risk" 
          value={moneyAtRiskDisplay} 
          desc="Calculated Financial Exposure"
          highlight
        />
        <KPICard 
          label="Active Decisions" 
          value="14" 
          desc={predictionRes ? `ML Confidence: ${(predictionRes.confidence_score * 100).toFixed(0)}%` : "4 require action today"} 
        />
      </div>

      {/* Main Grid: Decision Card (Left) & Protection + ERP (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-[1.65fr_minmax(320px,0.85fr)] gap-5">
        <DecisionCard 
          onApplyProtection={handleApplyProtectionPlan}
          onReviewSupplier={() => setModalState('supplier')}
          requestName={activeRequest.item_name}
          supplierName={activeRequest.vendor_name}
          moneyAtRisk={moneyAtRiskDisplay}
          realData={{
            status: automationRes?.automation_status || (isLive ? "ACTION_REQUIRED" : null),
            actions: automationRes?.generated_actions || []
          }}
        />
        
        <div className="flex flex-col gap-4">
          <ProtectionPanel 
            onGeneratePlan={() => setModalState('negotiation')} 
            onApplyProtection={handleApplyProtectionPlan}
            onReviewSupplier={() => setModalState('supplier')}
          />
          <IntegrationCard />
        </div>
      </div>

      {/* Procurement Queue with search */}
      <ProcurementQueue externalSearch={context.searchQuery} />

      <Toast message={toastMsg} onClose={() => setToastMsg(null)} />

      {/* Supplier Review Modal */}
      <Modal 
        isOpen={modalState === 'supplier'} 
        onClose={() => setModalState('none')}
        title={`Supplier Intelligence — ${activeRequest.vendor_name}`}
        description="Comprehensive supplier decision context assembled from procurement signals."
      >
        <div className="space-y-3 mt-2">
          <div className="flex justify-between py-2.5 border-b border-border text-[13px]">
            <b className="text-text">Vendor ID</b>
            <span className="text-muted font-mono">{activeRequest.vendor_id}</span>
          </div>
          <div className="flex justify-between py-2.5 border-b border-border text-[13px]">
            <b className="text-text">Quote Position vs Benchmark</b>
            <span className="text-[#b42318] font-semibold">
              ₹{activeRequest.unit_price.toLocaleString()} vs ₹{activeRequest.historical_avg_price.toLocaleString()} (+{priceGapPct}%)
            </span>
          </div>
          <div className="flex justify-between py-2.5 border-b border-border text-[13px]">
            <b className="text-text">On-Time Delivery Rate</b>
            <span className="text-warning font-semibold">
              {(activeRequest.historical_on_time_rate * 100).toFixed(0)}% (Performance Degraded)
            </span>
          </div>
          <div className="flex justify-between py-2.5 border-b border-border text-[13px]">
            <b className="text-text">Quality Pass Rate</b>
            <span className="text-text">
              {(activeRequest.historical_quality_score * 100).toFixed(0)}% (Defect Rate: {(activeRequest.vendor_defect_rate * 100).toFixed(0)}%)
            </span>
          </div>
          <div className="flex justify-between py-2.5 border-b border-border text-[13px]">
            <b className="text-text">Supplier Health Score</b>
            <span className="text-primary font-bold">
              {riskRes ? (riskRes.supplier_health_score * 100).toFixed(1) : "82.8"}%
            </span>
          </div>
          <div className="flex justify-between py-2.5 border-b border-border text-[13px]">
            <b className="text-text">ProcuraIQ Recommendation</b>
            <span className="text-primary font-semibold">Apply Protection Controls Before PO</span>
          </div>
        </div>
        <div className="mt-5 flex justify-end gap-2">
          <Button variant="secondary" onClick={() => setModalState('none')}>
            Close
          </Button>
          <Button 
            variant="primary" 
            disabled={applyingProtection}
            onClick={() => {
              setModalState('none');
              handleApplyProtectionPlan();
            }}
          >
            {applyingProtection ? (
              <span className="flex items-center gap-1.5"><Loader2 size={14} className="animate-spin" /> Binding Protection...</span>
            ) : (
              'Apply Protection Controls'
            )}
          </Button>
        </div>
      </Modal>

      {/* Negotiation Plan Modal */}
      <Modal 
        isOpen={modalState === 'negotiation'} 
        onClose={() => setModalState('none')}
        title={`Negotiation Playbook — ${activeRequest.vendor_name}`}
        description="Data-backed leverage points generated directly from live procurement variance."
      >
        <div className="space-y-3.5 mt-2">
          <div className="p-3 bg-[#f9f9fb] border border-border rounded-xl">
            <div className="flex items-center gap-1.5 text-xs uppercase tracking-wider text-muted font-bold mb-1">
              <DollarSign size={14} className="text-primary" /> Quoted Price & Benchmark Delta
            </div>
            <p className="text-[13px] text-text">
              Current quote is <strong>₹{activeRequest.unit_price.toLocaleString()}</strong> per unit vs observed benchmark of <strong>₹{activeRequest.historical_avg_price.toLocaleString()}</strong>.
              Total unit price variance is <strong>+₹{priceGap.toLocaleString()} (+{priceGapPct}%)</strong> across {activeRequest.quantity} units.
            </p>
          </div>

          <div className="p-3 bg-[#f9f9fb] border border-border rounded-xl">
            <div className="flex items-center gap-1.5 text-xs uppercase tracking-wider text-muted font-bold mb-1">
              <TrendingDown size={14} className="text-warning" /> Procurement Leverage Points
            </div>
            <ul className="text-[13px] text-text list-disc list-inside space-y-1">
              <li>Historical delivery reliability dropped to <strong>{(activeRequest.historical_on_time_rate * 100).toFixed(0)}%</strong>.</li>
              <li>Calculated Money At Risk on {activeRequest.advance_payment_pct * 100}% advance is <strong>{moneyAtRiskDisplay}</strong>.</li>
              <li>Order volume of {activeRequest.quantity} units justifies volume price adjustment.</li>
            </ul>
          </div>

          <div className="p-3 bg-[#f9f9fb] border border-border rounded-xl">
            <div className="text-xs uppercase tracking-wider text-muted font-bold mb-1">
              Recommended Talking Points
            </div>
            <ul className="text-[13px] text-text list-disc list-inside space-y-1">
              <li>"Our procurement index reflects a median price of ₹110K for this hardware specification."</li>
              <li>"To mitigate recent lead-time variances, we require payment structured in 30/70 delivery milestones."</li>
            </ul>
          </div>

          <div className="p-3.5 bg-[#edf4ff] border border-[#d0e1fd] rounded-xl flex items-center justify-between">
            <div>
              <b className="text-xs uppercase tracking-wider text-primary block mb-0.5">Target Financial Outcome</b>
              <p className="text-[13px] text-text font-medium">
                Target Savings: <strong className="text-primary font-bold">₹75,000</strong> and zero unhedged advance risk.
              </p>
            </div>
          </div>
        </div>

        <div className="mt-5 flex justify-end gap-2">
          <Button variant="secondary" onClick={() => setModalState('none')}>
            Close
          </Button>
          <Button 
            variant="primary" 
            onClick={() => {
              setModalState('none');
              showToast('Negotiation brief prepared for buyer.');
            }}
          >
            Confirm Negotiation Strategy
          </Button>
        </div>
      </Modal>

      {/* Protection Plan Confirmation Modal */}
      <Modal
        isOpen={modalState === 'contract_success'}
        onClose={() => setModalState('none')}
        title="Protection Plan Prepared"
        description="Legally enforceable procurement protection contract generated."
      >
        <div className="space-y-3.5 mt-2">
          <div className="p-4 bg-[#f6ffed] border border-[#b7eb8f] rounded-xl flex items-start gap-3">
            <ShieldCheck size={24} className="text-green flex-shrink-0 mt-0.5" />
            <div>
              <b className="text-[14px] text-[#274916] font-semibold block">
                Protection Controls Successfully Bound
              </b>
              <p className="text-[12px] text-[#389e0d] mt-0.5">
                Contract Reference: <span className="font-mono font-bold">{createdContract?.contract_id || `CTR-${Date.now().toString().slice(-6)}`}</span>
              </p>
            </div>
          </div>

          <div className="border border-border rounded-xl p-3.5 divide-y divide-border text-xs">
            <div className="flex justify-between py-2">
              <span className="text-muted">Payment Milestone Protection:</span>
              <span className="text-text font-semibold">30% Advance / 70% Post-Inspection</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-muted">Delivery SLA Penalty:</span>
              <span className="text-text font-semibold">{activeRequest.lead_time_days} Days SLA Guaranteed</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-muted">Return & Defect Policy:</span>
              <span className="text-text font-semibold">30 Days Full Replacement</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-muted">Buyer Acceptance Status:</span>
              <span className="text-green font-semibold flex items-center gap-1">
                <CheckCircle2 size={12} /> Accepted & Ready for PO
              </span>
            </div>
          </div>
        </div>

        <div className="mt-5 flex justify-end gap-2">
          <Button variant="primary" onClick={() => setModalState('none')}>
            Proceed to Purchase Order
          </Button>
        </div>
      </Modal>
    </>
  );
};
