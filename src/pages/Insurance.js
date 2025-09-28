import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Search, AlertTriangle, ChevronLeft, ChevronRight, ArrowLeft, Phone, Mail } from 'lucide-react';

const Insurance = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const searchRef = useRef(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(9);
  const [insuranceData, setInsuranceData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchLoading, setSearchLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [totalResults, setTotalResults] = useState(0);

  // Insurance company logo mapping
  const insuranceLogoMap = {
    'SIC Insurance': '/insurances/SIC.png',
    'SIC Insurance Company': '/insurances/SIC.png',
    'Enterprise Life': '/insurances/ENTERPRISE LIFE.png',
    'Enterprise Life Insurance': '/insurances/ENTERPRISE LIFE.png',
    'MetLife Ghana': '/insurances/METROPOLITAN.jpeg',
    'Metropolitan Life Insurance': '/insurances/METROPOLITAN.jpeg',
    'Vanguard Assurance': '/insurances/VANGUARD.jpeg',
    'Ghana Reinsurance': '/insurances/ghic.png',
    'Star Assurance': '/insurances/STAR.jpeg',
    'GLICO Insurance': '/insurances/GLICO.png',
    'GLICO General Insurance': '/insurances/GLICO.png',
    'GLICO Life Insurance': '/insurances/GLICO.png',
    'Hollard Insurance': '/insurances/HOLLARD.png',
    'Old Mutual': '/insurances/OLD MUTUAL.jpeg',
    'Sanlam Allianz': '/insurances/SANLAM ALLIANZ.jpeg',
    'Prudential Insurance': '/insurances/PRUDENTIAL.png',
    'NSIA Insurance': '/insurances/NSIA.jpeg',
    'Phoenix Insurance': '/insurances/PHOENIX.png',
    'Ghana Life Insurance': '/insurances/GHANA LIFE INSURANCE.png',
    'Ghana Union Assurance': '/insurances/GHANA UNION ASSURANCE.png',
    'Coronation Insurance': '/insurances/CORONATION.png',
    'Donewell Insurance': '/insurances/DONEWELL.png',
    'Apex Insurance': '/insurances/APEX.png',
    'Bedrock Insurance': '/insurances/BEDROCK.png',
    'Beige Assure': '/insurances/BEIGE ASSURE.png',
    'Best Insurance': '/insurances/BEST.jpeg',
    'Cosmopolitan Insurance': '/insurances/COSMOPOLITAN.png',
    'Dosh Insurance': '/insurances/DOSH.jpeg',
    'Equity Insurance': '/insurances/EQUITY.jpeg',
    'Esich Life': '/insurances/ESICH LIFE.jpeg',
    'First Insurance': '/insurances/FIRST INSURANCE.jpeg',
    'Heritage Energy Insurance': '/insurances/HERITAGE ENERGY INSURANCE.png',
    'Impact Life Insurance': '/insurances/IMPACT LIFE INSURANCE.jpeg',
    'Imperial Insurance': '/insurances/IMPERIAL.jpeg',
    'Loyalty Insurance': '/insurances/LOYALTY.jpeg',
    'Millennium Insurance': '/insurances/MILLENNIUM.png',
    'Nationwide Medical': '/insurances/NATIONAWIDE MEDICAL.png',
    'Premier Insurance': '/insurances/PREMIER.png',
    'Priority Insurance': '/insurances/Priority.jpeg',
    'Provident Insurance': '/insurances/Provident.jpeg',
    'Quality Life Insurance': '/insurances/Quality.png',
    'Regency Insurance': '/insurances/RegencyNem.jpeg',
    'Serene Insurance': '/insurances/SERENE.png',
    'Star Health Insurance': '/insurances/STAR HEALTH.png',
    'Sunu Insurance': '/insurances/SUNU.png',
    'Unique Insurance': '/insurances/UNIQUE.png',
    'Vitality Insurance': '/insurances/VITALITY.jpeg',
    'ACACIA Insurance': '/insurances/ACACIA.jpeg',
    'ACE Insurance': '/insurances/ACE.png',
    'ACTVA Insurance': '/insurances/ACTVA.jpeg',
    'Asterlife Insurance': '/insurances/ASTERLIFE.htm',
    'MiLife Insurance': '/insurances/MILIFE.png',
    'Prime Insurance': '/insurances/prime.png'
  };

  // Load insurance data from API
  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('accessToken');
      setIsAuthenticated(!!token);
      return !!token;
    };

    if (checkAuth()) {
      const hasSearchOrFilter = searchTerm || filterStatus !== 'all';
      loadInsuranceData(hasSearchOrFilter);
    } else {
      setIsLoading(false);
      setSearchLoading(false);
    }
  }, [currentPage, itemsPerPage, searchTerm, filterStatus]);

  const loadInsuranceData = async (isSearch = false) => {
    try {
      if (isSearch) {
        setSearchLoading(true);
      } else {
        setIsLoading(true);
      }
      const token = localStorage.getItem('accessToken');
      if (!token) {
        console.error('No authentication token found');
        if (isSearch) {
          setSearchLoading(false);
        } else {
          setIsLoading(false);
        }
        return;
      }
      const params = new URLSearchParams({
        page: currentPage.toString(),
        limit: itemsPerPage.toString()
      });

      if (searchTerm) {
        params.append('name', searchTerm);
      }

      const response = await fetch(`http://localhost:8000/api/insurance/search?${params}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        
        const transformedInsurance = (data.insurance || []).map(company => ({
          id: company.id,
          name: company.name,
          logo: company.logo_url || insuranceLogoMap[company.name] || '/insurances/default-insurance.png',
          phone: company.phone || 'N/A',
          email: company.email || 'N/A',
          address: company.address || 'N/A',
          website: company.website || 'N/A',
          established: company.established_date ? new Date(company.established_date).getFullYear().toString() : 'N/A',
          insuranceType: company.insurance_type || 'N/A',
          totalCases: company.total_cases || 0, // Use real data from backend
          activeCases: company.total_cases || 0, // Using total cases as active for now
          resolvedCases: company.total_cases || 0, // Using total cases as resolved for now
          riskLevel: company.risk_level || 'Low', // Use real risk level from backend
          riskScore: company.risk_score || 0, // Use real risk score from backend
          successRate: company.success_rate || 0, // Use real success rate from backend
          lastActivity: company.updated_at ? new Date(company.updated_at).toISOString().split('T')[0] : 'N/A',
          cases: [] // This would come from a separate cases API
        }));

        setInsuranceData(transformedInsurance);
        setTotalResults(data.total || 0);
      } else {
        console.error('Failed to load insurance data:', response.status);
      }
    } catch (error) {
      console.error('Error loading insurance data:', error);
    } finally {
      if (isSearch) {
        setSearchLoading(false);
      } else {
        setIsLoading(false);
      }
    }
  };

  // Handle search
  const handleSearch = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    const hasSearchOrFilter = searchTerm || filterStatus !== 'all';
    loadInsuranceData(hasSearchOrFilter);
  };

  // Handle insurance click
  const handleInsuranceClick = (company) => {
    navigate(`/insurance-profile/${company.id}?name=${encodeURIComponent(company.name)}`);
  };

  // Filter and sort insurance
  const filteredInsurance = insuranceData.filter(company => {
    if (filterStatus === 'all') return true;
    return company.risk_level === filterStatus;
  });

  // Pagination
  const totalPagesCount = Math.ceil(totalResults / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;

  // Early return for loading state (only on initial load, not during search)
  if (isLoading && !searchLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-sky-600 mx-auto"></div>
          <p className="mt-4 text-slate-600">Loading insurance companies...</p>
        </div>
      </div>
    );
  }

  // Authentication check
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 mb-4">
            <AlertTriangle className="h-16 w-16 mx-auto mb-4" />
            <h2 className="text-2xl font-bold">Authentication Required</h2>
            <p className="text-gray-600 mt-2">Please log in to view insurance data</p>
          </div>
          <button
            onClick={() => navigate('/login')}
            className="bg-sky-600 text-white px-6 py-2 rounded-lg hover:bg-sky-700 transition-colors"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Insurance Companies</h1>
              <p className="text-gray-600 mt-1">
                {totalResults} insurance companies found
              </p>
            </div>
            <button
              onClick={() => navigate('/')}
              className="flex items-center text-gray-600 hover:text-gray-900"
            >
              <ArrowLeft className="h-5 w-5 mr-1" />
              Back to Home
            </button>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
          <form onSubmit={handleSearch} className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search insurance companies..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-transparent"
                ref={searchRef}
              />
              {searchLoading && (
                <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-sky-500"></div>
                </div>
              )}
            </div>
            <div className="flex gap-2">
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-transparent"
              >
                <option value="all">All Risk Levels</option>
                <option value="Low">Low Risk</option>
                <option value="Medium">Medium Risk</option>
                <option value="High">High Risk</option>
              </select>
              <button
                type="submit"
                className="px-6 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 transition-colors flex items-center"
              >
                <Search className="h-4 w-4 mr-2" />
                Search
              </button>
            </div>
          </form>
      </div>

        {/* Insurance Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredInsurance.map((company) => (
            <div
              key={company.id}
              onClick={() => handleInsuranceClick(company)}
              className="bg-white rounded-lg shadow-sm border hover:shadow-md transition-shadow cursor-pointer"
            >
              <div className="p-6">
                <div className="flex items-center mb-4">
                  <img
                    src={company.logo}
                    alt={company.name}
                    className="h-12 w-12 rounded-lg object-cover mr-4"
                    onError={(e) => {
                      e.target.src = '/insurances/default-insurance.png';
                    }}
                  />
                <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900">{company.name}</h3>
                    <p className="text-sm text-gray-600">{company.established}</p>
                </div>
                  <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                    company.riskLevel === 'Low' ? 'bg-green-100 text-green-800' :
                    company.riskLevel === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {company.riskLevel} Risk
                </div>
              </div>

                <div className="space-y-2 mb-4">
                  <div className="flex items-center text-sm text-gray-600">
                    <Phone className="h-4 w-4 mr-2" />
                    {company.phone}
                </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <Mail className="h-4 w-4 mr-2" />
                    {company.email}
                </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <Shield className="h-4 w-4 mr-2" />
                    {company.insuranceType}
                </div>
              </div>

                <div className="border-t pt-4">
                  <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
                    <div>
                      <span className="font-medium">Total Cases: {company.totalCases}</span>
                    </div>
                    <div>
                      <span className="font-medium">Success Rate: {company.successRate}%</span>
                    </div>
                    <div>
                      <span className="font-medium">Risk Score: {company.riskScore}</span>
                    </div>
                    <div>
                      <span className="font-medium">Last Activity: {company.lastActivity}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* No Results */}
        {filteredInsurance.length === 0 && !isLoading && (
          <div className="text-center py-12">
            <Shield className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No insurance companies found</h3>
            <p className="text-gray-600">Try adjusting your search or filter criteria</p>
          </div>
        )}

        {/* Pagination */}
        {totalPagesCount > 1 && (
          <div className="mt-8 flex items-center justify-between">
            <div className="text-sm text-gray-700">
              Showing {startIndex + 1} to {Math.min(endIndex, totalResults)} of {totalResults} insurance companies
            </div>
            <div className="flex items-center space-x-2">
                <button
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                className="px-3 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                <ChevronLeft className="h-4 w-4" />
                </button>
                
              <span className="px-4 py-2 text-sm font-medium text-gray-700">
                Page {currentPage} of {totalPagesCount}
              </span>
                
                <button
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPagesCount))}
                disabled={currentPage === totalPagesCount}
                className="px-3 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronRight className="h-4 w-4" />
                </button>
            </div>
          </div>
        )}
        </div>
    </div>
  );
};

export default Insurance;
