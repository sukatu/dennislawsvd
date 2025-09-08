import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Download, Building2, Calendar, MapPin, Phone, Mail, TrendingUp, AlertTriangle, CheckCircle, Clock, User, Scale, FileText, Send, ChevronLeft, ChevronRight } from 'lucide-react';

const BankDetail = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [bankData, setBankData] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');
  const [sortBy, setSortBy] = useState('date');
  const [showRequestModal, setShowRequestModal] = useState(false);
  const [selectedCase, setSelectedCase] = useState(null);
  const [requestType, setRequestType] = useState('case_details');
  const [requestMessage, setRequestMessage] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(5);

  // Load bank data
  useEffect(() => {
    const bankId = searchParams.get('id');
    if (bankId) {
      // Mock bank data - in real app, this would come from API
      const mockBankData = {
    id: 1,
    name: 'Ghana Commercial Bank',
    logo: '🏦',
    established: '1953',
    headquarters: 'Accra, Ghana',
    phone: '+233 302 666 000',
    email: 'info@gcb.com.gh',
    website: 'www.gcb.com.gh',
    totalCases: 45,
    activeCases: 12,
    resolvedCases: 33,
    riskLevel: 'Medium',
    riskScore: 65,
    lastActivity: '2024-01-15',
    cases: [
      {
        id: 1,
        title: 'Loan Default Case vs. John Smith',
        caseNumber: 'GCB/2024/001',
        status: 'Active',
        date: '2024-01-10',
        type: 'Commercial Law',
        outcome: 'Pending',
        court: 'Commercial Court, Accra',
        courtType: 'Commercial Court',
        region: 'Greater Accra',
        judge: 'Justice Sarah Mensah',
        plaintiff: 'Ghana Commercial Bank',
        defendant: 'John Smith',
        description: 'Default on business loan of GHS 500,000. Bank seeking recovery of outstanding amount plus interest.',
        amount: 'GHS 500,000',
        riskLevel: 'High',
        dates: [
          { type: 'Filing', date: '2024-01-10', description: 'Case filed with court' },
          { type: 'First Hearing', date: '2024-02-15', description: 'Initial hearing scheduled' },
          { type: 'Second Hearing', date: '2024-03-20', description: 'Evidence presentation' },
          { type: 'Ruling', date: '2024-04-10', description: 'Court ruling expected' }
        ]
      },
      {
        id: 2,
        title: 'Fraud Investigation - ABC Corp',
        caseNumber: 'GCB/2023/156',
        status: 'Resolved',
        date: '2023-12-15',
        type: 'Criminal Law',
        outcome: 'Favorable',
        court: 'High Court, Accra',
        courtType: 'High Court',
        region: 'Greater Accra',
        judge: 'Justice Kwame Nkrumah',
        plaintiff: 'Ghana Commercial Bank',
        defendant: 'ABC Corporation',
        description: 'Investigation into fraudulent transactions involving corporate account. Case resolved with conviction.',
        amount: 'GHS 2,500,000',
        riskLevel: 'High',
        dates: [
          { type: 'Filing', date: '2023-08-15', description: 'Case filed with court' },
          { type: 'First Hearing', date: '2023-09-20', description: 'Initial hearing' },
          { type: 'Evidence Hearing', date: '2023-10-25', description: 'Evidence presentation' },
          { type: 'Judgment', date: '2023-12-15', description: 'Final judgment delivered' }
        ]
      },
      {
        id: 3,
        title: 'Contract Dispute - XYZ Ltd',
        caseNumber: 'GCB/2024/002',
        status: 'Active',
        date: '2024-01-05',
        type: 'Contract Law',
        outcome: 'Pending',
        court: 'Commercial Court, Accra',
        courtType: 'Commercial Court',
        region: 'Greater Accra',
        judge: 'Justice Ama Serwaa',
        plaintiff: 'XYZ Limited',
        defendant: 'Ghana Commercial Bank',
        description: 'Dispute over terms of credit facility agreement. Company claims breach of contract.',
        amount: 'GHS 1,200,000',
        riskLevel: 'Medium',
        dates: [
          { type: 'Filing', date: '2024-01-05', description: 'Case filed with court' },
          { type: 'First Hearing', date: '2024-02-12', description: 'Initial hearing scheduled' },
          { type: 'Mediation', date: '2024-03-18', description: 'Mediation session' }
        ]
      },
      {
        id: 4,
        title: 'Money Laundering Investigation',
        caseNumber: 'GCB/2023/145',
        status: 'Resolved',
        date: '2023-11-20',
        type: 'Criminal Law',
        outcome: 'Favorable',
        court: 'High Court, Accra',
        courtType: 'High Court',
        region: 'Greater Accra',
        judge: 'Justice Kofi Annan',
        plaintiff: 'State of Ghana',
        defendant: 'Multiple Parties',
        description: 'Investigation into money laundering activities through bank accounts. Successful prosecution.',
        amount: 'GHS 5,000,000',
        riskLevel: 'High',
        dates: [
          { type: 'Investigation Start', date: '2023-06-01', description: 'Investigation commenced' },
          { type: 'Arrest', date: '2023-08-15', description: 'Suspects arrested' },
          { type: 'Trial Start', date: '2023-09-10', description: 'Trial began' },
          { type: 'Judgment', date: '2023-11-20', description: 'Final judgment delivered' }
        ]
      },
      {
        id: 5,
        title: 'Credit Card Fraud Case',
        caseNumber: 'GCB/2023/134',
        status: 'Resolved',
        date: '2023-10-15',
        type: 'Criminal Law',
        outcome: 'Favorable',
        court: 'Circuit Court, Kumasi',
        courtType: 'Circuit Court',
        region: 'Ashanti',
        judge: 'Justice Nana Addo',
        plaintiff: 'Ghana Commercial Bank',
        defendant: 'Fraud Ring',
        description: 'Large-scale credit card fraud operation. Bank recovered significant portion of losses.',
        amount: 'GHS 800,000',
        riskLevel: 'Medium',
        dates: [
          { type: 'Filing', date: '2023-07-20', description: 'Case filed with court' },
          { type: 'First Hearing', date: '2023-08-25', description: 'Initial hearing' },
          { type: 'Evidence Hearing', date: '2023-09-30', description: 'Evidence presentation' },
          { type: 'Judgment', date: '2023-10-15', description: 'Final judgment delivered' }
        ]
      }
    ]
      };
      setBankData(mockBankData);
    }
  }, [searchParams]);

  // Reset to first page when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [filterStatus, sortBy]);

  // Early return for loading state - must be after all hooks
  if (!bankData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-sky-600 mx-auto"></div>
          <p className="mt-4 text-slate-600">Loading bank details...</p>
        </div>
      </div>
    );
  }

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

  const getProgressBarColor = (score) => {
    if (score <= 30) return 'bg-emerald-500';
    if (score <= 70) return 'bg-amber-500';
    return 'bg-red-500';
  };

  // Filter and sort cases
  const filteredCases = bankData?.cases.filter(caseItem => {
    if (filterStatus === 'all') return true;
    return caseItem.status === filterStatus;
  }) || [];

  const sortedCases = [...filteredCases].sort((a, b) => {
    if (sortBy === 'date') return new Date(b.date) - new Date(a.date);
    if (sortBy === 'amount') return parseFloat(b.amount.replace(/[^\d.]/g, '')) - parseFloat(a.amount.replace(/[^\d.]/g, ''));
    if (sortBy === 'risk') {
      const riskOrder = { 'High': 3, 'Medium': 2, 'Low': 1 };
      return riskOrder[b.riskLevel] - riskOrder[a.riskLevel];
    }
    if (sortBy === 'courtType') return a.courtType.localeCompare(b.courtType);
    if (sortBy === 'region') return a.region.localeCompare(b.region);
    if (sortBy === 'status') return a.status.localeCompare(b.status);
    return 0;
  });

  // Pagination logic for cases
  const totalPages = Math.ceil(sortedCases.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentCases = sortedCases.slice(startIndex, endIndex);

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const exportToCSV = () => {
    const csvContent = [
      ['Case Title', 'Case Number', 'Status', 'Date', 'Type', 'Outcome', 'Court', 'Judge', 'Amount', 'Risk Level'],
      ...sortedCases.map(caseItem => [
        caseItem.title,
        caseItem.caseNumber,
        caseItem.status,
        caseItem.date,
        caseItem.type,
        caseItem.outcome,
        caseItem.court,
        caseItem.judge,
        caseItem.amount,
        caseItem.riskLevel
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${bankData.name.replace(/\s+/g, '_')}_cases.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const handleRequestDetails = (caseItem) => {
    setSelectedCase(caseItem);
    setShowRequestModal(true);
    setRequestMessage('');
  };

  const handleSubmitRequest = () => {
    // In a real application, this would send the request to a backend API
    const requestData = {
      type: requestType,
      caseId: selectedCase.id,
      caseNumber: selectedCase.caseNumber,
      bankName: bankData.name,
      message: requestMessage,
      timestamp: new Date().toISOString()
    };

    console.log('Request submitted:', requestData);
    
    // Show success message
    alert(`Request submitted successfully!\n\nRequest Type: ${requestType === 'case_details' ? 'Case Details' : requestType === 'full_report' ? 'Full Report' : 'Legal Documents'}\nCase: ${selectedCase.caseNumber}\nBank: ${bankData.name}`);
    
    // Close modal and reset
    setShowRequestModal(false);
    setSelectedCase(null);
    setRequestMessage('');
  };

  const generateFullReport = () => {
    // Generate a comprehensive report for all cases
    const reportData = {
      bankName: bankData.name,
      totalCases: bankData.totalCases,
      activeCases: bankData.activeCases,
      resolvedCases: bankData.resolvedCases,
      riskLevel: bankData.riskLevel,
      riskScore: bankData.riskScore,
      cases: sortedCases.map(caseItem => ({
        title: caseItem.title,
        caseNumber: caseItem.caseNumber,
        status: caseItem.status,
        date: caseItem.date,
        type: caseItem.type,
        outcome: caseItem.outcome,
        court: caseItem.court,
        judge: caseItem.judge,
        amount: caseItem.amount,
        riskLevel: caseItem.riskLevel,
        description: caseItem.description
      })),
      generatedAt: new Date().toISOString()
    };

    // Create and download report
    const reportString = JSON.stringify(reportData, null, 2);
    const blob = new Blob([reportString], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${bankData.name.replace(/\s+/g, '_')}_full_report.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div>
      {/* Breadcrumb */}
      <div className="bg-white border-b border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-3">
          <nav className="flex items-center space-x-2 text-sm text-slate-600">
            <button
              onClick={() => navigate('/')}
              className="hover:text-slate-900 transition-colors"
            >
              Home
            </button>
            <span>/</span>
            <button
              onClick={() => navigate('/banks')}
              className="hover:text-slate-900 transition-colors"
            >
              Banks
            </button>
            <span>/</span>
            <span className="text-slate-900">{bankData.name}</span>
          </nav>
        </div>
      </div>

      {/* Bank Header */}
      <div className="bg-white border-b border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center gap-6">
            <div className="h-20 w-20 rounded-full bg-sky-100 flex items-center justify-center text-3xl">
              {bankData.logo}
            </div>
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-slate-900">{bankData.name}</h1>
              <p className="text-lg text-slate-600">
                Established {bankData.established} • {bankData.headquarters}
              </p>
              <div className="mt-2 flex items-center gap-4">
                <span className={`inline-flex items-center gap-1 rounded-full px-3 py-1 text-sm font-semibold ring-1 ${getRiskColor(bankData.riskLevel)}`}>
                  <span className={`inline-block h-2 w-2 rounded-full ${getRiskColor(bankData.riskLevel).split(' ')[1].replace('text-', 'bg-')}`}></span>
                  {bankData.riskLevel} Risk
                </span>
                <span className="text-sm text-slate-500">Risk Score: {bankData.riskScore}</span>
              </div>
            </div>
            <div className="flex gap-2">
              <button 
                onClick={exportToCSV}
                className="inline-flex items-center gap-2 rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors"
              >
                <Download className="h-4 w-4" />
                Export Cases
              </button>
              <button 
                onClick={generateFullReport}
                className="inline-flex items-center gap-2 rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors"
              >
                <FileText className="h-4 w-4" />
                Generate Report
              </button>
              <button className="inline-flex items-center gap-2 rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700 transition-colors">
                <TrendingUp className="h-4 w-4" />
                Add to Watchlist
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* Bank Information */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Bank Information</h2>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <div>
                  <label className="text-sm font-medium text-slate-600">Bank Name</label>
                  <p className="text-slate-900">{bankData.name}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-600">Established</label>
                  <p className="text-slate-900">{bankData.established}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-600">Headquarters</label>
                  <p className="text-slate-900">{bankData.headquarters}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-600">Phone</label>
                  <p className="text-slate-900">{bankData.phone}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-600">Email</label>
                  <p className="text-slate-900">{bankData.email}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-600">Website</label>
                  <p className="text-slate-900">{bankData.website}</p>
                </div>
              </div>
            </section>

            {/* Cases Section */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-slate-900">Legal Cases ({sortedCases.length})</h2>
                <div className="flex items-center gap-3">
                  <button
                    onClick={exportToCSV}
                    className="inline-flex items-center gap-2 rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors"
                  >
                    <Download className="h-4 w-4" />
                    Export
                  </button>
                </div>
              </div>

              {/* Filter and Sort Controls */}
              <div className="flex items-center gap-4 mb-6">
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
                >
                  <option value="all">All Cases</option>
                  <option value="Active">Active Cases</option>
                  <option value="Resolved">Resolved Cases</option>
                  <option value="Pending">Pending Cases</option>
                </select>

                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
                >
                  <option value="date">Sort by Date</option>
                  <option value="amount">Sort by Amount</option>
                  <option value="risk">Sort by Risk</option>
                  <option value="courtType">Sort by Court Type</option>
                  <option value="region">Sort by Region</option>
                  <option value="status">Sort by Case Status</option>
                </select>
              </div>

              <div className="space-y-4">
                {currentCases.map((caseItem) => (
                  <div key={caseItem.id} className="border border-slate-200 rounded-lg p-4 hover:border-sky-300 transition-colors">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <h3 className="font-medium text-slate-900 mb-1">{caseItem.title}</h3>
                        <p className="text-sm text-slate-600">Case No: {caseItem.caseNumber}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          caseItem.status === 'Active' ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700'
                        }`}>
                          {caseItem.status}
                        </span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          caseItem.riskLevel === 'High' ? 'bg-red-100 text-red-700' :
                          caseItem.riskLevel === 'Medium' ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700'
                        }`}>
                          {caseItem.riskLevel} Risk
                        </span>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm text-slate-600 mb-3">
                      <div>
                        <span className="font-medium">Type:</span> {caseItem.type}
                      </div>
                      <div>
                        <span className="font-medium">Amount:</span> {caseItem.amount}
                      </div>
                      <div>
                        <span className="font-medium">Court:</span> {caseItem.court}
                      </div>
                      <div>
                        <span className="font-medium">Judge:</span> {caseItem.judge}
                      </div>
                      <div>
                        <span className="font-medium">Plaintiff:</span> {caseItem.plaintiff}
                      </div>
                      <div>
                        <span className="font-medium">Defendant:</span> {caseItem.defendant}
                      </div>
                    </div>
                    
                    <p className="text-sm text-slate-700 mb-3">{caseItem.description}</p>
                    
                    {/* Case Timeline */}
                    {caseItem.dates && caseItem.dates.length > 0 && (
                      <div className="mb-3">
                        <h5 className="text-sm font-medium text-slate-600 mb-2">Case Timeline:</h5>
                        <div className="space-y-1">
                          {caseItem.dates.slice(0, 3).map((dateItem, dateIndex) => (
                            <div key={dateIndex} className="flex items-center gap-2 text-xs text-slate-600">
                              <span className="font-medium">{dateItem.type}:</span>
                              <span>{dateItem.date}</span>
                              <span className="text-slate-400">•</span>
                              <span className="text-slate-500">{dateItem.description}</span>
                            </div>
                          ))}
                          {caseItem.dates.length > 3 && (
                            <p className="text-xs text-slate-500">+{caseItem.dates.length - 3} more dates</p>
                          )}
                        </div>
                      </div>
                    )}
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-500">Date: {caseItem.date}</span>
                      <div className="flex items-center gap-2">
                        <button 
                          onClick={() => handleRequestDetails(caseItem)}
                          className="inline-flex items-center gap-1 px-3 py-1 bg-sky-50 text-sky-700 rounded-md hover:bg-sky-100 text-sm font-medium transition-colors"
                        >
                          <Send className="w-3 h-3" />
                          Request Details
                        </button>
                        <button 
                          onClick={() => navigate(`/case-detail?caseId=${caseItem.id}&source=bank&institutionId=1`)}
                          className="text-sky-600 hover:text-sky-700 text-sm font-medium"
                        >
                          View Full Details →
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Pagination for Cases */}
              {totalPages > 1 && (
                <div className="mt-6 flex items-center justify-between">
                  <div className="text-sm text-slate-600">
                    Showing {startIndex + 1} to {Math.min(endIndex, sortedCases.length)} of {sortedCases.length} cases
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
              )}
            </section>
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Risk Assessment */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Risk Assessment</h2>
              <div className="text-center">
                <div className={`text-3xl font-bold mb-2 ${getRiskScoreColor(bankData.riskScore)}`}>
                  {bankData.riskScore}
                </div>
                <div className="text-sm text-slate-600 mb-4">{bankData.riskLevel} Risk Score</div>
                <div className="w-full bg-slate-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${getProgressBarColor(bankData.riskScore)}`}
                    style={{ width: `${bankData.riskScore}%` }}
                  ></div>
                </div>
                <p className="text-xs text-slate-500 mt-2">Based on case history and outcomes</p>
              </div>
            </section>

            {/* Case Statistics */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Case Statistics</h2>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Total Cases</span>
                  <span className="text-sm font-medium text-slate-900">{bankData.totalCases}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Active Cases</span>
                  <span className="text-sm font-medium text-amber-600">{bankData.activeCases}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Resolved Cases</span>
                  <span className="text-sm font-medium text-emerald-600">{bankData.resolvedCases}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Resolution Rate</span>
                  <span className="text-sm font-medium text-slate-900">
                    {Math.round((bankData.resolvedCases / bankData.totalCases) * 100)}%
                  </span>
                </div>
              </div>
            </section>

            {/* Quick Actions */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Quick Actions</h2>
              <div className="space-y-3">
                <button className="w-full text-left px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                  <User className="h-4 w-4 inline mr-2" />
                  View Related People
                </button>
                <button className="w-full text-left px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                  <Scale className="h-4 w-4 inline mr-2" />
                  View Similar Cases
                </button>
                <button className="w-full text-left px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                  <TrendingUp className="h-4 w-4 inline mr-2" />
                  Risk Analysis Report
                </button>
              </div>
            </section>
          </div>
        </div>
      </div>

      {/* Request Details Modal */}
      {showRequestModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Request Case Details</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-700 mb-2">Request Type</label>
              <select
                value={requestType}
                onChange={(e) => setRequestType(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
              >
                <option value="case_details">Case Details</option>
                <option value="full_report">Full Report</option>
                <option value="legal_documents">Legal Documents</option>
              </select>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-700 mb-2">Case Information</label>
              <div className="bg-slate-50 p-3 rounded-lg text-sm">
                <p><strong>Case:</strong> {selectedCase?.caseNumber}</p>
                <p><strong>Title:</strong> {selectedCase?.title}</p>
                <p><strong>Bank:</strong> {bankData?.name}</p>
              </div>
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-slate-700 mb-2">Additional Message (Optional)</label>
              <textarea
                value={requestMessage}
                onChange={(e) => setRequestMessage(e.target.value)}
                placeholder="Please specify any additional information you need..."
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 h-20 resize-none"
              />
            </div>

            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowRequestModal(false)}
                className="px-4 py-2 text-slate-600 hover:text-slate-800 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSubmitRequest}
                className="px-4 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 transition-colors"
              >
                Submit Request
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BankDetail;
