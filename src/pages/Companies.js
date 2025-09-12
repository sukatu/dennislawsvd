import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Building2, MapPin, Phone, Mail, Globe, Filter, ChevronDown, Eye, Star, Users, TrendingUp, FileText } from 'lucide-react';

const Companies = () => {
  const navigate = useNavigate();
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalResults, setTotalResults] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  
  // Filters
  const [filters, setFilters] = useState({
    city: '',
    region: '',
    company_type: '',
    industry: '',
    is_active: true
  });

  // Load companies
  const loadCompanies = async (page = 1, search = '', filterParams = {}) => {
    setLoading(true);
    setError(null);
    
    try {
      const token = localStorage.getItem('accessToken');
      const params = new URLSearchParams({
        page: page,
        limit: 20,
        ...(search && { query: search }),
        ...filterParams
      });
      
      const response = await fetch(`http://localhost:8000/api/companies/search?${params}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setCompanies(data.results || []);
        setTotalPages(data.total_pages || 1);
        setTotalResults(data.total || 0);
        setCurrentPage(data.page || 1);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to load companies');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Handle search
  const handleSearch = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    loadCompanies(1, searchQuery, filters);
  };

  // Handle filter change
  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  // Apply filters
  const applyFilters = () => {
    setCurrentPage(1);
    loadCompanies(1, searchQuery, filters);
  };

  // Clear filters
  const clearFilters = () => {
    setFilters({
      city: '',
      region: '',
      company_type: '',
      industry: '',
      is_active: true
    });
    setSearchQuery('');
    setCurrentPage(1);
    loadCompanies(1, '', {});
  };

  // Load companies on component mount
  useEffect(() => {
    loadCompanies();
  }, []);

  const formatCurrency = (amount) => {
    if (!amount || amount === 0) return 'N/A';
    return new Intl.NumberFormat('en-GH', {
      style: 'currency',
      currency: 'GHS',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const formatRegion = (regionCode) => {
    if (!regionCode) return 'N/A';

    const regionMappings = {
      'GAR': 'Greater Accra Region',
      'ASR': 'Ashanti Region',
      'UWR': 'Upper West Region',
      'UER': 'Upper East Region',
      'NR': 'Northern Region',
      'BR': 'Brong-Ahafo Region',
      'VR': 'Volta Region',
      'ER': 'Eastern Region',
      'CR': 'Central Region',
      'WR': 'Western Region',
      'WNR': 'Western North Region',
      'AHA': 'Ahafo Region',
      'BON': 'Bono Region',
      'BON_E': 'Bono East Region',
      'OTI': 'Oti Region',
      'SAV': 'Savannah Region',
      'NEA': 'North East Region'
    };

    return regionMappings[regionCode.toUpperCase()] || regionCode;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Companies Database</h1>
              <p className="text-gray-600 mt-2">
                {totalResults > 0 ? `${totalResults} companies found` : 'No companies found'}
              </p>
            </div>
            
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Filter className="w-4 h-4" />
              <span>Filters</span>
              <ChevronDown className={`w-4 h-4 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
            </button>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          {/* Search Bar */}
          <form onSubmit={handleSearch} className="mb-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search companies by name, industry, or activities..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </form>

          {/* Filters */}
          {showFilters && (
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
                <input
                  type="text"
                  value={filters.city}
                  onChange={(e) => handleFilterChange('city', e.target.value)}
                  placeholder="e.g., Accra"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Region</label>
                <select
                  value={filters.region}
                  onChange={(e) => handleFilterChange('region', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">All Regions</option>
                  <option value="GAR">Greater Accra Region</option>
                  <option value="ASR">Ashanti Region</option>
                  <option value="UWR">Upper West Region</option>
                  <option value="UER">Upper East Region</option>
                  <option value="NR">Northern Region</option>
                  <option value="BR">Brong-Ahafo Region</option>
                  <option value="VR">Volta Region</option>
                  <option value="ER">Eastern Region</option>
                  <option value="CR">Central Region</option>
                  <option value="WR">Western Region</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Company Type</label>
                <select
                  value={filters.company_type}
                  onChange={(e) => handleFilterChange('company_type', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">All Types</option>
                  <option value="Limited">Limited</option>
                  <option value="Partnership">Partnership</option>
                  <option value="Sole Proprietorship">Sole Proprietorship</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Industry</label>
                <input
                  type="text"
                  value={filters.industry}
                  onChange={(e) => handleFilterChange('industry', e.target.value)}
                  placeholder="e.g., Technology"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              
              <div className="flex items-end space-x-2">
                <button
                  onClick={applyFilters}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Apply
                </button>
                <button
                  onClick={clearFilters}
                  className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
                >
                  Clear
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Results */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-gray-600">Loading companies...</span>
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <div className="text-red-600">{error}</div>
          </div>
        ) : companies.length === 0 ? (
          <div className="text-center py-12">
            <Building2 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No companies found</p>
            <p className="text-sm text-gray-500 mt-2">Try adjusting your search terms or filters</p>
          </div>
        ) : (
          <>
            {/* Companies Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {companies.map((company) => (
                <div key={company.id} className="bg-white rounded-lg shadow-sm border hover:shadow-md transition-shadow">
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 mb-1">{company.name}</h3>
                        {company.short_name && (
                          <p className="text-sm text-gray-600 mb-2">{company.short_name}</p>
                        )}
                        <div className="flex items-center space-x-2 text-sm text-gray-600">
                          <Building2 className="w-4 h-4" />
                          <span>{company.industry || 'N/A'}</span>
                        </div>
                      </div>
                      <div className="flex items-center space-x-1">
                        {company.rating && (
                          <div className="flex items-center">
                            <Star className="w-4 h-4 text-yellow-400 fill-current" />
                            <span className="text-sm text-gray-600 ml-1">{company.rating}</span>
                          </div>
                        )}
                      </div>
                    </div>
                    
                    {/* Company Details */}
                    <div className="space-y-2 mb-4">
                      {company.city && (
                        <div className="flex items-center text-sm text-gray-600">
                          <MapPin className="w-4 h-4 mr-2" />
                          <span>{company.city}, {formatRegion(company.region)}</span>
                        </div>
                      )}
                      
                      {company.phone && (
                        <div className="flex items-center text-sm text-gray-600">
                          <Phone className="w-4 h-4 mr-2" />
                          <span>{company.phone}</span>
                        </div>
                      )}
                      
                      {company.email && (
                        <div className="flex items-center text-sm text-gray-600">
                          <Mail className="w-4 h-4 mr-2" />
                          <span>{company.email}</span>
                        </div>
                      )}
                      
                      {company.website && (
                        <div className="flex items-center text-sm text-gray-600">
                          <Globe className="w-4 h-4 mr-2" />
                          <a href={company.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800">
                            {company.website}
                          </a>
                        </div>
                      )}
                    </div>
                    
                    {/* Company Stats */}
                    <div className="grid grid-cols-2 gap-4 mb-4">
                      {company.employee_count > 0 && (
                        <div className="text-center">
                          <div className="flex items-center justify-center mb-1">
                            <Users className="w-4 h-4 text-blue-600 mr-1" />
                            <span className="text-sm font-medium text-gray-900">{company.employee_count}</span>
                          </div>
                          <p className="text-xs text-gray-600">Employees</p>
                        </div>
                      )}
                      
                      {company.annual_revenue > 0 && (
                        <div className="text-center">
                          <div className="flex items-center justify-center mb-1">
                            <TrendingUp className="w-4 h-4 text-green-600 mr-1" />
                            <span className="text-sm font-medium text-gray-900">
                              {formatCurrency(company.annual_revenue)}
                            </span>
                          </div>
                          <p className="text-xs text-gray-600">Annual Revenue</p>
                        </div>
                      )}
                    </div>
                    
                    {/* Company Description */}
                    {company.description && (
                      <p className="text-sm text-gray-700 mb-4 line-clamp-3">
                        {company.description}
                      </p>
                    )}
                    
                    {/* Business Activities */}
                    {company.business_activities && company.business_activities.length > 0 && (
                      <div className="mb-4">
                        <h4 className="text-sm font-medium text-gray-900 mb-2">Business Activities</h4>
                        <div className="flex flex-wrap gap-1">
                          {company.business_activities.slice(0, 3).map((activity, index) => (
                            <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                              {activity}
                            </span>
                          ))}
                          {company.business_activities.length > 3 && (
                            <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                              +{company.business_activities.length - 3} more
                            </span>
                          )}
                        </div>
                      </div>
                    )}
                    
                    {/* Action Buttons */}
                    <div className="flex space-x-2">
                      <button
                        onClick={() => navigate(`/company-details/${company.id}?name=${encodeURIComponent(company.name)}`)}
                        className="flex-1 flex items-center justify-center space-x-2 px-3 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm"
                      >
                        <Eye className="w-4 h-4" />
                        <span>Quick View</span>
                      </button>
                      <button
                        onClick={() => navigate(`/company-profile/${company.id}`)}
                        className="flex-1 flex items-center justify-center space-x-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
                      >
                        <FileText className="w-4 h-4" />
                        <span>Full Profile</span>
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between mt-8">
                <div className="text-sm text-gray-600">
                  Showing {((currentPage - 1) * 20) + 1} to {Math.min(currentPage * 20, totalResults)} of {totalResults} companies
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => loadCompanies(currentPage - 1, searchQuery, filters)}
                    disabled={currentPage === 1}
                    className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Previous
                  </button>
                  <span className="px-3 py-2 text-sm text-gray-600">
                    Page {currentPage} of {totalPages}
                  </span>
                  <button
                    onClick={() => loadCompanies(currentPage + 1, searchQuery, filters)}
                    disabled={currentPage >= totalPages}
                    className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Companies;
