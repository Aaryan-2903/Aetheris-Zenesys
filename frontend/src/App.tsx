import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { DecisionCenter } from './pages/DecisionCenter';
import { Login } from './pages/Login';
import { Signup } from './pages/Signup';
import { Layout, PlaceholderPage } from './pages/Placeholders';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/" element={<Layout />}>
            <Route index element={<DecisionCenter />} />
            <Route path="requirement" element={<PlaceholderPage title="Requirement" description="Define and manage procurement specifications, quantities, and delivery targets." />} />
            <Route path="discovery" element={<PlaceholderPage title="Discovery" description="AI-powered supplier discovery and qualification across global vendor networks." />} />
            <Route path="comparison" element={<PlaceholderPage title="Comparison" description="Multi-dimensional vendor scorecards across price, delivery SLA, and quality risk." />} />
            <Route path="benchmark" element={<PlaceholderPage title="Benchmark" description="Real-time category price benchmarks and historic market price indices." />} />
            <Route path="savings" element={<PlaceholderPage title="Savings" description="Realized and potential cost savings tracking across business units." />} />
            <Route path="negotiation" element={<PlaceholderPage title="Negotiation" description="Strategic negotiation playbooks and leverage points generated from intelligence signals." />} />
            <Route path="approval" element={<PlaceholderPage title="Approval" description="Multi-tier enterprise approval workflows and risk mitigation compliance checks." />} />
            <Route path="po" element={<PlaceholderPage title="Purchase Order" description="Automated purchase order generation with warranty and milestone protections." />} />
            <Route path="settings" element={<PlaceholderPage title="Settings" description="Configure organization policies, risk thresholds, and ERP integrations." />} />
            <Route path="support" element={<PlaceholderPage title="Support" description="Enterprise support, knowledge base, and SLA tracking." />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
