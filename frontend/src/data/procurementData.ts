export const kpis = {
  potentialSavings: "₹12.4M",
  potentialSavingsTrend: "↑ 15.2% vs last quarter",
  realizedSavings: "₹8.1M",
  realizedSavingsTrend: "↑ 8.4% vs last quarter",
  financialExposure: "₹5.2L",
  financialExposureDesc: "Current active exposure",
  activeDecisions: 14,
  activeDecisionsDesc: "4 require action today"
};

export const decisionData = {
  title: "IT Hardware Procurement — Apex Parts Intl.",
  description: "ProcuraIQ found a financially exposed purchase and converted the signals into a recommended protection plan.",
  moneyAtRisk: "₹5.2L",
  status: "Before commitment",
  signals: [
    {
      id: "price",
      title: "Price anomaly",
      description: "Current quote is above the observed market benchmark."
    },
    {
      id: "delivery",
      title: "Delivery performance",
      description: "Recent supplier performance requires review before commitment."
    },
    {
      id: "exposure",
      title: "Financial exposure",
      description: "Payment and delivery terms increase downside if performance slips."
    }
  ]
};

export const protectionActions = [
  {
    id: "01",
    title: "Milestone-based payment",
    description: "Reduce upfront financial exposure."
  },
  {
    id: "02",
    title: "Delivery SLA clause",
    description: "Tie payment to delivery performance."
  },
  {
    id: "03",
    title: "Negotiate quote",
    description: "Use benchmark variance as leverage."
  }
];

export const procurementQueue = [
  {
    id: "1",
    request: "Industrial Fasteners",
    supplier: "Apex Parts Intl.",
    exposure: "₹2.1L",
    decision: "Review Price",
    status: "review"
  },
  {
    id: "2",
    request: "IT Hardware",
    supplier: "TechCorp Solutions",
    exposure: "₹1.8L",
    decision: "Proceed",
    status: "proceed"
  },
  {
    id: "3",
    request: "Raw Materials",
    supplier: "Global Mfg Inc.",
    exposure: "₹1.3L",
    decision: "Approval Required",
    status: "approval"
  },
  {
    id: "4",
    request: "Office Equipment",
    supplier: "Nexus Industries",
    exposure: "₹72K",
    decision: "Proceed",
    status: "proceed"
  }
];
