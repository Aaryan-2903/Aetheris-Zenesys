import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { DecisionCenter } from './pages/DecisionCenter';
import { Requirement } from './pages/Requirement';
import { Discovery } from './pages/Discovery';
import { Comparison } from './pages/Comparison';
import { Benchmark } from './pages/Benchmark';
import { Savings } from './pages/Savings';
import { Negotiation } from './pages/Negotiation';
import { Approval } from './pages/Approval';
import { PurchaseOrderPage } from './pages/PurchaseOrderPage';
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
            <Route path="requirement" element={<Requirement />} />
            <Route path="discovery" element={<Discovery />} />
            <Route path="comparison" element={<Comparison />} />
            <Route path="benchmark" element={<Benchmark />} />
            <Route path="savings" element={<Savings />} />
            <Route path="negotiation" element={<Negotiation />} />
            <Route path="approval" element={<Approval />} />
            <Route path="po" element={<PurchaseOrderPage />} />
            <Route path="settings" element={<PlaceholderPage title="Settings" description="Configure organization policies, risk thresholds, and ERP integrations." />} />
            <Route path="support" element={<PlaceholderPage title="Support" description="Enterprise support, knowledge base, and SLA tracking." />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
