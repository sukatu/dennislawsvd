import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import About from './pages/About';
import Contact from './pages/Contact';
import People from './pages/People';
import PersonProfile from './pages/PersonProfile';
import CaseDetail from './pages/CaseDetail';
import CaseDetails from './pages/CaseDetails';
import CaseSearchResults from './pages/CaseSearchResults';
import Results from './pages/Results';
import PeopleResults from './pages/PeopleResults';
import Signup from './pages/Signup';
import Login from './pages/Login';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import Banks from './pages/Banks';
import BankDetail from './pages/BankDetail';
import Insurance from './pages/Insurance';
import InsuranceDetail from './pages/InsuranceDetail';
import InsuranceProfile from './pages/InsuranceProfile';
import Companies from './pages/Companies';
import CompanyDetail from './pages/CompanyDetail';
import CompanyProfile from './pages/CompanyProfile';
import Settings from './pages/Settings';
import EnhancedSearchResults from './pages/EnhancedSearchResults';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50 text-slate-900">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/people-results" element={<PeopleResults />} />
            <Route path="/people" element={<People />} />
            <Route path="/person-profile/:id" element={<PersonProfile />} />
            <Route path="/case-detail" element={<CaseDetail />} />
            <Route path="/case-details/:caseId" element={<CaseDetails />} />
            <Route path="/case-search" element={<CaseSearchResults />} />
            <Route path="/enhanced-search" element={<EnhancedSearchResults />} />
            <Route path="/results" element={<Results />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/login" element={<Login />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route path="/banks" element={<Banks />} />
            <Route path="/bank-detail/:id" element={<BankDetail />} />
            <Route path="/insurance" element={<Insurance />} />
            <Route path="/insurance-detail" element={<InsuranceDetail />} />
            <Route path="/insurance-profile/:id" element={<InsuranceProfile />} />
            <Route path="/companies" element={<Companies />} />
            <Route path="/company-details/:id" element={<CompanyDetail />} />
            <Route path="/company-profile/:id" element={<CompanyProfile />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
