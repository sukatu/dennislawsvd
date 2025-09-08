import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Building2, Search, Filter, Download, TrendingUp, AlertTriangle, CheckCircle, Clock, ChevronLeft, ChevronRight } from 'lucide-react';

const Banks = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const searchRef = useRef(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(9);

  // Mock bank data with logos and case statistics
  const banksData = [
    {
      id: 1,
      name: 'Ghana Commercial Bank',
      logo: '🏦',
      phone: '+233 302 666 000',
      email: 'info@gcb.com.gh',
      address: 'High Street, Accra, Ghana',
      website: 'www.gcb.com.gh',
      established: '1953',
      totalCases: 45,
      activeCases: 12,
      resolvedCases: 33,
      riskLevel: 'Medium',
      riskScore: 65,
      lastActivity: '2024-01-15',
      cases: [
        { id: 1, title: 'Loan Default Case vs. John Smith', status: 'Active', date: '2024-01-10' },
        { id: 2, title: 'Fraud Investigation - ABC Corp', status: 'Resolved', date: '2023-12-15' },
        { id: 3, title: 'Contract Dispute - XYZ Ltd', status: 'Active', date: '2024-01-05' }
      ]
    },
    {
      id: 2,
      name: 'Ecobank Ghana',
      logo: '🏛️',
      phone: '+233 302 666 100',
      email: 'info@ecobank.com.gh',
      address: 'Independence Avenue, Accra, Ghana',
      website: 'www.ecobank.com.gh',
      established: '1989',
      totalCases: 32,
      activeCases: 8,
      resolvedCases: 24,
      riskLevel: 'Low',
      riskScore: 35,
      lastActivity: '2024-01-12',
      cases: [
        { id: 4, title: 'Credit Card Fraud Case', status: 'Resolved', date: '2023-11-20' },
        { id: 5, title: 'Business Loan Dispute', status: 'Active', date: '2024-01-08' }
      ]
    },
    {
      id: 3,
      name: 'Standard Chartered Bank',
      logo: '🏢',
      phone: '+233 302 666 200',
      email: 'info@sc.com.gh',
      address: 'Oxford Street, Accra, Ghana',
      website: 'www.sc.com.gh',
      established: '1896',
      totalCases: 28,
      activeCases: 6,
      resolvedCases: 22,
      riskLevel: 'Low',
      riskScore: 28,
      lastActivity: '2024-01-14',
      cases: [
        { id: 6, title: 'Investment Fraud Investigation', status: 'Resolved', date: '2023-10-15' },
        { id: 7, title: 'Mortgage Dispute Case', status: 'Active', date: '2024-01-03' }
      ]
    },
    {
      id: 4,
      name: 'Absa Bank Ghana',
      logo: '🏪',
      phone: '+233 302 666 300',
      email: 'info@absa.com.gh',
      address: 'Liberation Road, Accra, Ghana',
      website: 'www.absa.com.gh',
      established: '2013',
      totalCases: 38,
      activeCases: 15,
      resolvedCases: 23,
      riskLevel: 'High',
      riskScore: 78,
      lastActivity: '2024-01-16',
      cases: [
        { id: 8, title: 'Money Laundering Investigation', status: 'Active', date: '2024-01-12' },
        { id: 9, title: 'Corporate Fraud Case', status: 'Active', date: '2024-01-09' },
        { id: 10, title: 'Loan Recovery Dispute', status: 'Resolved', date: '2023-12-20' }
      ]
    },
    {
      id: 5,
      name: 'Fidelity Bank Ghana',
      logo: '🏦',
      phone: '+233 302 666 400',
      email: 'info@fidelitybank.com.gh',
      address: 'Ring Road Central, Accra, Ghana',
      website: 'www.fidelitybank.com.gh',
      established: '1998',
      totalCases: 22,
      activeCases: 4,
      resolvedCases: 18,
      riskLevel: 'Low',
      riskScore: 22,
      lastActivity: '2024-01-11',
      cases: [
        { id: 11, title: 'Account Fraud Investigation', status: 'Resolved', date: '2023-09-30' },
        { id: 12, title: 'Business Account Dispute', status: 'Active', date: '2024-01-07' }
      ]
    },
    {
      id: 6,
      name: 'Zenith Bank Ghana',
      logo: '🏛️',
      phone: '+233 302 666 500',
      email: 'info@zenithbank.com.gh',
      address: 'Liberation Road, Accra, Ghana',
      website: 'www.zenithbank.com.gh',
      established: '2005',
      totalCases: 41,
      activeCases: 11,
      resolvedCases: 30,
      riskLevel: 'Medium',
      riskScore: 58,
      lastActivity: '2024-01-13',
      cases: [
        { id: 13, title: 'Corporate Loan Default', status: 'Active', date: '2024-01-06' },
        { id: 14, title: 'Investment Scam Case', status: 'Resolved', date: '2023-11-25' },
        { id: 15, title: 'Credit Facility Dispute', status: 'Active', date: '2024-01-02' }
      ]
    }
  ];

  const getRiskColor = (level) => {
    switch (level) {
      case 'Low':
        return 'bg-emerald-50 text-emerald-600 ring-emerald-200';
      case 'Medium':
        return 'bg-amber-50 text-amber-600 ring-amber-200';
      case 'High':
        return 'bg-red-50 text-red-600 ring-red-200';
      default:
        return 'bg-slate-50 text-slate-600 ring-slate-200';
    }
  };

  const getRiskScoreColor = (score) => {
    if (score <= 30) return 'text-emerald-600';
    if (score <= 70) return 'text-amber-600';
    return 'text-red-600';
  };

  // Handle search input changes
  const handleInputChange = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    
    if (value.length > 0) {
      const bankNames = banksData.map(bank => bank.name);
      const filteredSuggestions = bankNames.filter(name =>
        name.toLowerCase().includes(value.toLowerCase())
      );
      setSuggestions(filteredSuggestions.slice(0, 6)); // Limit to 6 suggestions
      setShowSuggestions(true);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  };

  // Handle suggestion selection
  const handleSuggestionClick = (suggestion) => {
    setSearchTerm(suggestion);
    setShowSuggestions(false);
  };

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const filteredBanks = banksData.filter(bank => {
    const matchesSearch = bank.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || 
      (filterStatus === 'high-risk' && bank.riskLevel === 'High') ||
      (filterStatus === 'medium-risk' && bank.riskLevel === 'Medium') ||
      (filterStatus === 'low-risk' && bank.riskLevel === 'Low');
    return matchesSearch && matchesFilter;
  });

  // Pagination logic
  const totalPages = Math.ceil(filteredBanks.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentBanks = filteredBanks.slice(startIndex, endIndex);

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Reset to first page when search or filter changes
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, filterStatus]);

  const handleBankClick = (bankId) => {
    navigate(`/bank-detail?id=${bankId}`);
  };

  const exportToCSV = () => {
    const csvContent = [
      ['Bank Name', 'Total Cases', 'Active Cases', 'Resolved Cases', 'Risk Level', 'Risk Score', 'Last Activity'],
      ...filteredBanks.map(bank => [
        bank.name,
        bank.totalCases,
        bank.activeCases,
        bank.resolvedCases,
        bank.riskLevel,
        bank.riskScore,
        bank.lastActivity
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'banks-data.csv';
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div>
      {/* Page Header */}
      <div className="bg-white border-b border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-900">Banks Database</h1>
              <p className="mt-2 text-slate-600">
                Comprehensive database of banks and their legal cases
              </p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={exportToCSV}
                className="inline-flex items-center gap-2 rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors"
              >
                <Download className="h-4 w-4" />
                Export CSV
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white border-b border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="relative flex-1 max-w-md" ref={searchRef}>
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Search banks..."
                value={searchTerm}
                onChange={handleInputChange}
                onFocus={() => searchTerm.length > 0 && setShowSuggestions(true)}
                className="w-full rounded-lg border border-slate-200 pl-10 pr-4 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
              />
              
              {/* Suggestions Dropdown */}
              {showSuggestions && suggestions.length > 0 && (
                <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-200 rounded-lg shadow-lg z-50 max-h-48 overflow-y-auto">
                  {suggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      type="button"
                      onClick={() => handleSuggestionClick(suggestion)}
                      className="w-full text-left px-4 py-3 text-sm text-slate-700 hover:bg-slate-50 border-b border-slate-100 last:border-b-0 transition-colors"
                    >
                      <div className="flex items-center gap-2">
                        <Building2 className="h-4 w-4 text-slate-400" />
                        <span>{suggestion}</span>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
            <div className="flex items-center gap-3">
              <Filter className="h-4 w-4 text-slate-400" />
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="rounded-lg border border-slate-200 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
              >
                <option value="all">All Risk Levels</option>
                <option value="high-risk">High Risk</option>
                <option value="medium-risk">Medium Risk</option>
                <option value="low-risk">Low Risk</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Banks Grid */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {currentBanks.map((bank) => (
            <div
              key={bank.id}
              onClick={() => handleBankClick(bank.id)}
              className="group cursor-pointer rounded-xl border border-slate-200 bg-white p-6 hover:border-sky-300 hover:shadow-lg transition-all duration-200"
            >
              {/* Bank Header */}
              <div className="flex items-center gap-4 mb-4">
                <div className="h-12 w-12 rounded-lg bg-sky-100 flex items-center justify-center text-2xl">
                  {bank.logo}
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-slate-900 group-hover:text-sky-600 transition-colors">
                    {bank.name}
                  </h3>
                  <p className="text-sm text-slate-500">Last activity: {bank.lastActivity}</p>
                </div>
              </div>

              {/* Risk Assessment */}
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-slate-600">Risk Level</span>
                  <span className={`inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs font-semibold ring-1 ${getRiskColor(bank.riskLevel)}`}>
                    {bank.riskLevel}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600">Risk Score</span>
                  <span className={`text-sm font-semibold ${getRiskScoreColor(bank.riskScore)}`}>
                    {bank.riskScore}/100
                  </span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-2 mt-2">
                  <div
                    className={`h-2 rounded-full ${
                      bank.riskScore <= 30 ? 'bg-emerald-500' :
                      bank.riskScore <= 70 ? 'bg-amber-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${bank.riskScore}%` }}
                  ></div>
                </div>
              </div>

              {/* Case Statistics */}
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div className="text-center">
                  <div className="text-lg font-semibold text-slate-900">{bank.totalCases}</div>
                  <div className="text-xs text-slate-500">Total Cases</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold text-amber-600">{bank.activeCases}</div>
                  <div className="text-xs text-slate-500">Active</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold text-emerald-600">{bank.resolvedCases}</div>
                  <div className="text-xs text-slate-500">Resolved</div>
                </div>
              </div>

              {/* Contact Information */}
              <div className="border-t border-slate-100 pt-4 mb-4">
                <h4 className="text-sm font-medium text-slate-600 mb-2">Contact Information</h4>
                <div className="space-y-1 text-xs text-slate-500">
                  <p><span className="font-medium">Phone:</span> {bank.phone}</p>
                  <p><span className="font-medium">Email:</span> {bank.email}</p>
                  <p><span className="font-medium">Address:</span> {bank.address}</p>
                  <p><span className="font-medium">Established:</span> {bank.established}</p>
                </div>
              </div>

              {/* Recent Cases Preview */}
              <div className="border-t border-slate-100 pt-4">
                <h4 className="text-sm font-medium text-slate-600 mb-2">Recent Cases</h4>
                <div className="space-y-2">
                  {bank.cases.slice(0, 2).map((caseItem) => (
                    <div key={caseItem.id} className="flex items-center justify-between text-xs">
                      <span className="text-slate-600 truncate flex-1">{caseItem.title}</span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        caseItem.status === 'Active' ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700'
                      }`}>
                        {caseItem.status}
                      </span>
                    </div>
                  ))}
                  {bank.cases.length > 2 && (
                    <p className="text-xs text-slate-500">+{bank.cases.length - 2} more cases</p>
                  )}
                </div>
              </div>

              {/* View Details Button */}
              <div className="mt-4 pt-4 border-t border-slate-100">
                <button className="w-full text-center text-sm font-medium text-sky-600 hover:text-sky-700 transition-colors">
                  View All Cases →
                </button>
              </div>
            </div>
          ))}
        </div>

        {filteredBanks.length === 0 && (
          <div className="text-center py-12">
            <Building2 className="h-12 w-12 text-slate-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-slate-900 mb-2">No banks found</h3>
            <p className="text-slate-600">Try adjusting your search or filter criteria.</p>
          </div>
        )}
      </div>

      {/* Summary Stats */}
      <div className="bg-white border-t border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6">
          <div className="grid grid-cols-2 gap-6 md:grid-cols-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-slate-900">{banksData.length}</div>
              <div className="text-sm text-slate-600">Total Banks</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-slate-900">
                {banksData.reduce((sum, bank) => sum + bank.totalCases, 0)}
              </div>
              <div className="text-sm text-slate-600">Total Cases</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-amber-600">
                {banksData.reduce((sum, bank) => sum + bank.activeCases, 0)}
              </div>
              <div className="text-sm text-slate-600">Active Cases</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-emerald-600">
                {banksData.reduce((sum, bank) => sum + bank.resolvedCases, 0)}
              </div>
              <div className="text-sm text-slate-600">Resolved Cases</div>
            </div>
          </div>
        </div>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="bg-white border-t border-slate-200">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div className="text-sm text-slate-600">
                Showing {startIndex + 1} to {Math.min(endIndex, filteredBanks.length)} of {filteredBanks.length} banks
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 1}
                  className="flex items-center gap-1 px-3 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <ChevronLeft className="w-4 h-4" />
                  Previous
                </button>
                
                <div className="flex items-center gap-1">
                  {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                    <button
                      key={page}
                      onClick={() => handlePageChange(page)}
                      className={`px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                        page === currentPage
                          ? 'bg-sky-600 text-white'
                          : 'text-slate-700 bg-white border border-slate-300 hover:bg-slate-50'
                      }`}
                    >
                      {page}
                    </button>
                  ))}
                </div>
                
                <button
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage === totalPages}
                  className="flex items-center gap-1 px-3 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Next
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Banks;
