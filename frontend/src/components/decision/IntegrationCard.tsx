import React, { useEffect, useState } from 'react';
import { netsuiteApi } from '../../api/netsuite';
import type { NetSuiteStatus } from '../../api/netsuite';

export const IntegrationCard: React.FC = () => {
  const [statusData, setStatusData] = useState<NetSuiteStatus | null>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await netsuiteApi.getStatus();
        setStatusData(data);
      } catch (err) {
        setStatusData({
          status: "NOT CONNECTED",
          message: "NetSuite connection not configured.",
          mode: "CONFIGURATION REQUIRED",
          last_sync: null
        });
      }
    };

    fetchStatus();
  }, []);

  const isConfigured = statusData?.status === "READY" || statusData?.status === "CONNECTED";
  const displayStatus = statusData?.mode || statusData?.status || "SuiteCloud Ready";

  return (
    <div className="mt-4 bg-card border border-border rounded-[18px] shadow-card p-5">
      <div className="flex justify-between items-center">
        <div>
          <div className="text-[11px] uppercase tracking-[0.08em] text-muted font-bold">ERP Integration</div>
          <b className="text-[15px] font-semibold text-text mt-0.5 block">Oracle NetSuite</b>
          <div className="text-[11px] text-muted mt-0.5">{statusData?.message || "SuiteCloud Integration"}</div>
        </div>
        <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold ${
          isConfigured ? 'bg-greenbg text-green' : 'bg-[#eaf2ff] text-primary'
        }`}>
          <span className="text-[9px]">●</span> {displayStatus}
        </div>
      </div>
    </div>
  );
};
