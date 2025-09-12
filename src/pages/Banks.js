import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Building2, Search, AlertTriangle, ChevronLeft, ChevronRight, ArrowLeft, Phone, Mail } from 'lucide-react';

const Banks = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const searchRef = useRef(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(9);
  const [banksData, setBanksData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [totalResults, setTotalResults] = useState(0);

  // Bank logo mapping
  const bankLogoMap = {
    'GCB Bank': '/banks/gcb bank.jpeg',
    'Ghana Commercial Bank': '/banks/gcb bank.jpeg',
    'Ecobank': '/banks/ecobank.jpeg',
    'Ecobank Ghana': '/banks/ecobank.jpeg',
    'Standard Chartered Bank': '/banks/stanchart.jpeg',
    'Standard Chartered Bank Ghana': '/banks/stanchart.jpeg',
    'Absa Bank': '/banks/absa.jpeg',
    'Absa Bank Ghana': '/banks/absa.jpeg',
    'Fidelity Bank': '/banks/Fidelity.jpeg',
    'Fidelity Bank Ghana': '/banks/Fidelity.jpeg',
    'Zenith Bank': '/banks/zenith.jpeg',
    'Zenith Bank Ghana': '/banks/zenith.jpeg',
    'First Atlantic Bank': '/banks/first atlantic.jpeg',
    'Ghana Exim Bank': '/banks/ghana exim bank.jpeg',
    'Ghana EXIM Bank': '/banks/ghana exim bank.jpeg',
    'GTBank': '/banks/gtbank.jpeg',
    'Guaranty Trust Bank': '/banks/gtbank.jpeg',
    'National Investment Bank': '/banks/national invenstment bank.jpeg',
    'Prudential Bank': '/banks/prudential bank.jpeg',
    'Republic Bank': '/banks/republic bank.jpeg',
    'Societe Generale Bank': '/banks/societe generale bank.jpeg',
    'The Royal Bank': '/banks/the royal bank.jpeg',
    'Universal Merchant Bank': '/banks/universal merchant bank.jpeg',
    'FBN Bank': '/banks/fbn.jpeg',
    'First Bank of Nigeria': '/banks/fbn.jpeg',
    'Access Bank': '/banks/access bank.jpeg',
    'Access Bank Ghana': '/banks/access bank.jpeg',
    'Agricultural Development Bank': '/banks/adb.jpeg',
    'Bank of Africa': '/banks/bank of africa.jpeg',
    'Bank of Ghana': '/banks/Bank of ghana.jpeg',
    'CAL Bank': '/banks/calbank.jpeg',
    'Consolidated Bank Ghana': '/banks/cbg.jpeg',
    'NIB Bank': '/banks/nib.jpeg',
    'Omnibsic Bank': '/banks/omnibsic.jpeg',
    'Stanbic Bank': '/banks/stanbic bank.jpeg',
    'Stanbic Bank Ghana': '/banks/stanbic bank.jpeg',
    'UMB Bank': '/banks/umb.jpeg',
    'ABII National Bank': '/banks/abii national.jpeg'
  };

  // Load banks data from API
  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('accessToken');
      setIsAuthenticated(!!token);
      return !!token;
    };

    if (checkAuth()) {
      loadBanksData();
    } else {
      setIsLoading(false);
    }
  }, [currentPage, itemsPerPage, searchTerm, filterStatus]); // eslint-disable-line react-hooks/exhaustive-deps

  const loadBanksData = async () => {
    try {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        console.error('No authentication token found');
        setIsLoading(false);
        return;
      }

      setIsLoading(true);
      const params = new URLSearchParams({
        page: currentPage.toString(),
        limit: itemsPerPage.toString()
      });

      if (searchTerm) {
        params.append('name', searchTerm);
      }

      const response = await fetch(`http://localhost:8000/api/banks/search?${params}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Banks data loaded:', data);
        
        const transformedBanks = (data.banks || []).map(bank => ({
          id: bank.id,
          name: bank.name,
          logo: bank.logo_url || bankLogoMap[bank.name] || '/banks/default-bank.jpeg',
          phone: bank.phone || 'N/A',
          email: bank.email || 'N/A',
          address: bank.address || 'N/A',
          website: bank.website || 'N/A',
          established: bank.established_date ? new Date(bank.established_date).getFullYear().toString() : 'N/A',
          totalCases: 0, // This would come from a separate cases API
          activeCases: 0,
          resolvedCases: 0,
          riskLevel: 'Low', // This would be calculated based on cases
          riskScore: 0,
          lastActivity: bank.updated_at ? new Date(bank.updated_at).toISOString().split('T')[0] : 'N/A',
          cases: [] // This would come from a separate cases API
        }));

        setBanksData(transformedBanks);
        // setTotalPages(data.total_pages || 0);
        setTotalResults(data.total || 0);
      } else {
        console.error('Failed to load banks data:', response.status);
      }
    } catch (error) {
      console.error('Error loading banks data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle search
  const handleSearch = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    loadBanksData();
  };

  // Handle bank click
  const handleBankClick = (bank) => {
    navigate(`/bank-detail?id=${bank.id}&name=${encodeURIComponent(bank.name)}`);
  };

  // Filter and sort banks
  const filteredBanks = banksData.filter(bank => {
    if (filterStatus === 'all') return true;
    return bank.riskLevel === filterStatus;
  });

  // Pagination
  const totalPagesCount = Math.ceil(totalResults / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;

  // Early return for loading state
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-sky-600 mx-auto"></div>
          <p className="mt-4 text-slate-600">Loading banks...</p>
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
            <p className="text-gray-600 mt-2">Please log in to view banks data</p>
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
              <h1 className="text-3xl font-bold text-gray-900">Banks</h1>
              <p className="text-gray-600 mt-1">
                {totalResults} banks found
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
                placeholder="Search banks..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-transparent"
                ref={searchRef}
              />
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

      {/* Banks Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredBanks.map((bank) => (
            <div
              key={bank.id}
              onClick={() => handleBankClick(bank)}
              className="bg-white rounded-lg shadow-sm border hover:shadow-md transition-shadow cursor-pointer"
            >
              <div className="p-6">
                <div className="flex items-center mb-4">
                  <img
                    src={bank.logo}
                    alt={bank.name}
                    className="h-12 w-12 rounded-lg object-cover mr-4"
                    onError={(e) => {
                      e.target.src = '/banks/default-bank.jpeg';
                    }}
                  />
                <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900">{bank.name}</h3>
                    <p className="text-sm text-gray-600">{bank.established}</p>
                </div>
                  <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                    bank.riskLevel === 'Low' ? 'bg-green-100 text-green-800' :
                    bank.riskLevel === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {bank.riskLevel} Risk
                </div>
              </div>

                <div className="space-y-2 mb-4">
                  <div className="flex items-center text-sm text-gray-600">
                    <Phone className="h-4 w-4 mr-2" />
                    {bank.phone}
                </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <Mail className="h-4 w-4 mr-2" />
                    {bank.email}
                </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <Building2 className="h-4 w-4 mr-2" />
                    {bank.address}
                </div>
              </div>

                <div className="border-t pt-4">
                  <div className="flex justify-between items-center text-sm text-gray-600">
                    <span>Total Cases: {bank.totalCases}</span>
                    <span>Last Activity: {bank.lastActivity}</span>
                    </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* No Results */}
        {filteredBanks.length === 0 && !isLoading && (
          <div className="text-center py-12">
            <Building2 className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No banks found</h3>
            <p className="text-gray-600">Try adjusting your search or filter criteria</p>
          </div>
        )}

        {/* Pagination */}
        {totalPagesCount > 1 && (
          <div className="mt-8 flex items-center justify-between">
            <div className="text-sm text-gray-700">
              Showing {startIndex + 1} to {Math.min(endIndex, totalResults)} of {totalResults} banks
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

export default Banks;
