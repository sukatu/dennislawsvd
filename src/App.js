import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import About from './pages/About';
import Contact from './pages/Contact';
import AdvancedSearch from './pages/AdvancedSearch';
import PeopleDatabase from './pages/PeopleDatabase';
import PeopleResults from './pages/PeopleResults';
import PersonProfile from './pages/PersonProfile';
import CaseDetail from './pages/CaseDetail';
import Results from './pages/Results';
import Signup from './pages/Signup';
import Specification from './pages/Specification';
import Banks from './pages/Banks';
import BankDetail from './pages/BankDetail';
import Insurance from './pages/Insurance';
import InsuranceDetail from './pages/InsuranceDetail';

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
            <Route path="/advanced-search" element={<AdvancedSearch />} />
            <Route path="/people-database" element={<PeopleDatabase />} />
            <Route path="/people-results" element={<PeopleResults />} />
            <Route path="/person-profile" element={<PersonProfile />} />
            <Route path="/case-detail" element={<CaseDetail />} />
            <Route path="/results" element={<Results />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/specification" element={<Specification />} />
            <Route path="/banks" element={<Banks />} />
            <Route path="/bank-detail" element={<BankDetail />} />
            <Route path="/insurance" element={<Insurance />} />
            <Route path="/insurance-detail" element={<InsuranceDetail />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
