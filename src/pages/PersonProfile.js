import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { ArrowLeft, Star, User, Calendar, MapPin, Mail, Building2, Phone, Shield, Clock, Users, GraduationCap, Heart, AlertCircle, CheckCircle, XCircle, Eye, EyeOff, Search, Filter, ArrowUpDown, Scale, RefreshCw, ChevronLeft, ChevronRight } from 'lucide-react';

const PersonProfile = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const searchQuery = searchParams.get('search') || '';
  
  const [personData, setPersonData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [relatedCases, setRelatedCases] = useState([]);
  const [filteredCases, setFilteredCases] = useState([]);
  const [caseSearchQuery, setCaseSearchQuery] = useState('');
  const [caseSortBy, setCaseSortBy] = useState('date');
  const [caseSortOrder, setCaseSortOrder] = useState('desc');
  const [currentPage, setCurrentPage] = useState(1);
  const [casesPerPage] = useState(10);

  // Region mapping function
  const getRegionName = (regionCode) => {
    const regionMap = {
      'GAR': 'Greater Accra Region',
      'ASR': 'Ashanti Region',
      'AR': 'Ashanti Region',
      'VR': 'Volta Region',
      'ER': 'Eastern Region',
      'WR': 'Western Region',
      'CR': 'Central Region',
      'NR': 'Northern Region',
      'UER': 'Upper East Region',
      'UWR': 'Upper West Region',
      'BR': 'Brong-Ahafo Region',
      'WNR': 'Western North Region',
      'AHR': 'Ahafo Region',
      'BER': 'Bono East Region',
      'NER': 'North East Region',
      'SR': 'Savannah Region',
      'OR': 'Oti Region',
      'gar': 'Greater Accra Region',
      'asr': 'Ashanti Region',
      'Greater Accra Region': 'Greater Accra Region',
      'Ashanti Region': 'Ashanti Region',
      'Volta Region': 'Volta Region',
      'Eastern Region': 'Eastern Region',
      'Western Region': 'Western Region',
      'Central Region': 'Central Region',
      'Northern Region': 'Northern Region',
      'Upper East Region': 'Upper East Region',
      'Upper West Region': 'Upper West Region',
      'Brong-Ahafo Region': 'Brong-Ahafo Region',
      'Western North Region': 'Western North Region',
      'Ahafo Region': 'Ahafo Region',
      'Bono East Region': 'Bono East Region',
      'North East Region': 'North East Region',
      'Savannah Region': 'Savannah Region',
      'Oti Region': 'Oti Region'
    };
    return regionMap[regionCode] || regionCode;
  };

  // Load person data
  useEffect(() => {
    const loadPersonData = async () => {
      try {
        setIsLoading(true);
        console.log('Loading person data for ID:', id);
        console.log('Search query:', searchQuery);
        console.log('URL being called:', `http://localhost:8000/api/people/${id}`);
        const token = localStorage.getItem('accessToken') || 'test-token-123';
        
        const response = await fetch(`http://localhost:8000/api/people/${id}`, {
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Person data loaded:', data);
          setPersonData(data);
        } else {
          console.log('API call failed, using fallback data');
          // Fallback to mock data
          setPersonData({
            id: id,
            full_name: searchQuery || 'Unknown Person',
            date_of_birth: 'N/A',
            occupation: 'N/A',
            gender: 'N/A',
            id_number: 'N/A',
            region: 'N/A',
            city: 'N/A',
            country: 'N/A',
            education: 'N/A',
            marital_status: 'N/A',
            phone: 'N/A',
            email: 'N/A',
            address: 'N/A',
            emergency_contact: 'N/A',
            languages: [],
            risk_level: 'N/A',
            risk_score: 0,
            total_cases: 0,
            resolved_cases: 0,
            pending_cases: 0,
            favorable_outcomes: 0,
            verification_status: 'Not Verified',
            verified_on: 'N/A'
          });
        }
      } catch (error) {
        console.error('Error loading person data:', error);
        setError('Failed to load person data');
      } finally {
        setIsLoading(false);
      }
    };

    if (id) {
      loadPersonData();
    }
  }, [id]);

  // Load related cases
  useEffect(() => {
    const loadRelatedCases = async () => {
      try {
        console.log('Loading related cases for person:', personData?.full_name);
        console.log('Search query:', searchQuery);
        const token = localStorage.getItem('accessToken') || 'test-token-123';
        const response = await fetch(`http://localhost:8000/api/case-search/search?query=${encodeURIComponent(personData?.full_name || '')}&limit=50`, {
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          console.log('API Response for related cases:', data);
          console.log('Results:', data.results);
          if (data.results && data.results.length > 0) {
            console.log('First case:', data.results[0]);
          }
          setRelatedCases(data.results || []);
          setFilteredCases(data.results || []);
        } else {
          // Fallback to mock data
          const mockCases = [
      {
        id: 1,
              title: `Sample case involving ${searchQuery || 'Unknown Person'}`,
              suit_reference_number: 'SAMPLE-001',
              court_type: 'High Court',
              date: '2024-01-01',
              presiding_judge: 'Sample Judge',
        status: 'Resolved',
        type: 'Civil'
      }
    ];
          setRelatedCases(mockCases);
          setFilteredCases(mockCases);
        }
      } catch (error) {
        console.error('Error loading related cases:', error);
      }
    };

    if (personData?.full_name) {
      loadRelatedCases();
    }
  }, [personData, searchQuery]);

  // Filter and sort cases
  useEffect(() => {
    let filtered = [...relatedCases];

    // Apply search filter
    if (caseSearchQuery) {
      filtered = filtered.filter(case_ => 
        case_.title.toLowerCase().includes(caseSearchQuery.toLowerCase()) ||
        case_.suit_number.toLowerCase().includes(caseSearchQuery.toLowerCase()) ||
        case_.judge.toLowerCase().includes(caseSearchQuery.toLowerCase())
      );
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let aValue, bValue;
      
      switch (caseSortBy) {
        case 'date':
          aValue = new Date(a.date);
          bValue = new Date(b.date);
          break;
        case 'title':
          aValue = a.title.toLowerCase();
          bValue = b.title.toLowerCase();
          break;
        case 'suit_number':
          aValue = a.suit_number.toLowerCase();
          bValue = b.suit_number.toLowerCase();
          break;
        default:
          aValue = a.title.toLowerCase();
          bValue = b.title.toLowerCase();
      }

      if (caseSortOrder === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

    setFilteredCases(filtered);
    setCurrentPage(1);
  }, [relatedCases, caseSearchQuery, caseSortBy, caseSortOrder]);

  // Pagination
  const totalPages = Math.ceil(filteredCases.length / casesPerPage);
  const startIndex = (currentPage - 1) * casesPerPage;
  const endIndex = startIndex + casesPerPage;
  const currentCases = filteredCases.slice(startIndex, endIndex);

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const clearFilters = () => {
    setCaseSearchQuery('');
    setCaseSortBy('date');
    setCaseSortOrder('desc');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-slate-600">Loading person profile...</p>
        </div>
      </div>
    );
  }

  if (error) {
  return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600">{error}</p>
            <button
            onClick={() => navigate('/people-results')}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Go Back
            </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-white border-b border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/people-results')}
                className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors"
              >
                <ArrowLeft className="h-4 w-4" />
                Back
              </button>
              <div>
                <h1 className="text-3xl font-bold text-slate-900">
                  {personData?.full_name || 'Loading...'}
                </h1>
                <p className="text-slate-600 text-lg">
                  {getRegionName(personData?.region)}
                </p>
                {searchQuery && (
                  <div className="mt-2">
                    <span className="text-sm text-slate-500">Search results for: </span>
                    <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-sm font-medium">
                      "{searchQuery}"
                    </span>
                  </div>
                )}
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${
                  personData?.risk_level === 'High' ? 'bg-red-500' :
                  personData?.risk_level === 'Medium' ? 'bg-yellow-500' : 'bg-green-500'
                }`}></div>
                <span className="text-sm font-medium text-slate-700">
                  {personData?.risk_level || 'Low'} Risk
                </span>
              </div>
              <button className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors">
                <Star className="h-4 w-4" />
                Watchlist
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          {/* Left Column - Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Personal Information */}
            <div className="bg-white rounded-lg border border-slate-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                  <User className="h-5 w-5 text-blue-600" />
                  Personal Information
                </h2>
                <button className="text-slate-400 hover:text-slate-600">
                  <RefreshCw className="h-5 w-5" />
                </button>
              </div>
              
              <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                <div className="space-y-4">
                  <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                    <div className="flex items-center space-x-2 mb-1">
                      <User className="w-4 h-4 text-blue-600" />
                      <span className="text-xs font-medium text-blue-800 uppercase tracking-wide">Full Name</span>
                    </div>
                    <p className="text-sm font-semibold text-blue-900">{personData?.full_name}</p>
                  </div>
                  
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center space-x-2 mb-1">
                      <Calendar className="w-4 h-4 text-gray-600" />
                      <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Date of Birth</span>
                    </div>
                    <p className="text-sm font-semibold text-gray-900">{personData?.date_of_birth || 'N/A'}</p>
                  </div>
                  
                  
                </div>
                
                <div className="space-y-4">
                  <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                    <div className="flex items-center space-x-2 mb-1">
                      <MapPin className="w-4 h-4 text-green-600" />
                      <span className="text-xs font-medium text-green-800 uppercase tracking-wide">Location</span>
                    </div>
                    <p className="text-sm font-semibold text-green-900">
                      {getRegionName(personData?.region)}
                    </p>
                    <p className="text-xs text-green-700">{personData?.city}, {personData?.country}</p>
                  </div>
                  
                  
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center space-x-2 mb-1">
                      <Users className="w-4 h-4 text-gray-600" />
                      <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Gender</span>
                    </div>
                    <p className="text-sm font-semibold text-gray-900">{personData?.gender || 'N/A'}</p>
                  </div>
                  
                </div>
              </div>
            </div>

            {/* Contact Information */}
            <div className="bg-white rounded-lg border border-slate-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                  <Phone className="h-5 w-5 text-blue-600" />
                  Contact Information
                </h2>
                <button className="text-slate-400 hover:text-slate-600">
                  <RefreshCw className="h-5 w-5" />
                </button>
              </div>
              
              <div className="max-w-md">
                <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                  <div className="flex items-center space-x-2 mb-1">
                    <MapPin className="w-4 h-4 text-green-600" />
                    <span className="text-xs font-medium text-green-800 uppercase tracking-wide">Address</span>
                  </div>
                  <p className="text-sm font-semibold text-green-900">{personData?.address || 'N/A'}</p>
                  <p className="text-xs text-green-700">N/A</p>
                </div>
              </div>
            </div>

            {/* Related Cases */}
            <div className="bg-white rounded-lg border border-slate-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                  <Scale className="h-5 w-5 text-blue-600" />
                  Related Cases ({filteredCases.length} of {relatedCases.length})
                </h2>
                <button className="text-slate-400 hover:text-slate-600">
                  <RefreshCw className="h-5 w-5" />
                </button>
              </div>
              
              {/* Search and Filter Controls */}
              <div className="mb-6 space-y-4">
                <div className="flex items-center gap-4">
                  <div className="flex-1">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                      <input
                        type="text"
                        placeholder="Search cases..."
                        value={caseSearchQuery}
                        onChange={(e) => setCaseSearchQuery(e.target.value)}
                        className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>
                  <select
                    value={caseSortBy}
                    onChange={(e) => setCaseSortBy(e.target.value)}
                    className="px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="date">Sort by Date</option>
                    <option value="title">Sort by Title</option>
                    <option value="suit_number">Sort by Suit Number</option>
                  </select>
                  <select
                    value={caseSortOrder}
                    onChange={(e) => setCaseSortOrder(e.target.value)}
                    className="px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="desc">Descending</option>
                    <option value="asc">Ascending</option>
                  </select>
                  <button
                    onClick={clearFilters}
                    className="px-4 py-2 text-slate-600 hover:text-slate-800 transition-colors"
                  >
                    Clear
                  </button>
                </div>
                
                {/* Case Types */}
                <div className="flex items-center gap-2">
                  <span className="text-sm text-slate-600">Case Types:</span>
                  <div className="flex gap-2">
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">Civil</span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-800 text-xs rounded-full">Criminal</span>
                  </div>
                </div>
              </div>

              {/* Cases List */}
              <div className="space-y-4">
                {currentCases.map((case_) => (
                  <div 
                    key={case_.id} 
                    className="border border-slate-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                    onClick={() => navigate(`/case-details/${case_.id}?q=${encodeURIComponent(searchQuery || personData?.full_name || '')}`)}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h3 className="font-semibold text-slate-900 mb-2">{case_.title}</h3>
                        <div className="grid grid-cols-2 gap-4 text-sm text-slate-600">
                          <div>
                            <span className="font-medium">Suit Number:</span> {case_.suit_reference_number || case_.suit_number || 'N/A'}
                          </div>
                          <div>
                            <span className="font-medium">Court:</span> {case_.court_type || case_.court || 'N/A'}
                          </div>
                          <div>
                            <span className="font-medium">Date:</span> {case_.date ? new Date(case_.date).toLocaleDateString() : 'N/A'}
                          </div>
                          <div>
                            <span className="font-medium">Judge:</span> {case_.presiding_judge || case_.judge || 'N/A'}
                          </div>
                        </div>
                      </div>
                      <div className="ml-4 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors">
                        View Case
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              {/* Pagination */}
              {totalPages > 1 && (
                <div className="mt-6 flex items-center justify-between">
                  <div className="text-sm text-slate-600">
                    Page {currentPage} of {totalPages}
                    </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handlePageChange(currentPage - 1)}
                      disabled={currentPage === 1}
                      className="px-3 py-2 text-slate-600 hover:text-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      <ChevronLeft className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => handlePageChange(currentPage + 1)}
                      disabled={currentPage === totalPages}
                      className="px-3 py-2 text-slate-600 hover:text-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      <ChevronRight className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              )}
              </div>
          </div>

          {/* Right Column - Side Panel */}
          <div className="space-y-6">
            {/* Risk Assessment */}
            <div className="bg-white rounded-lg border border-slate-200 p-6">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center gap-2 mb-4">
                <Shield className="h-5 w-5 text-blue-600" />
                Risk Assessment
              </h3>
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">
                  {personData?.risk_score || 0}%
                </div>
                <div className="text-sm text-slate-600 mb-4">Low Risk Score</div>
                <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                  <div
                    className="bg-green-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${personData?.risk_score || 0}%` }}
                  ></div>
                </div>
                <p className="text-xs text-slate-500">Based on legal history and case outcomes</p>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="bg-white rounded-lg border border-slate-200 p-6">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center gap-2 mb-4">
                <Clock className="h-5 w-5 text-blue-600" />
                Quick Stats
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Total Cases:</span>
                  <span className="text-sm font-semibold text-slate-900">{personData?.total_cases || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Resolved Cases:</span>
                  <span className="text-sm font-semibold text-slate-900">{personData?.resolved_cases || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Pending Cases:</span>
                  <span className="text-sm font-semibold text-slate-900">{personData?.pending_cases || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Favorable Outcomes:</span>
                  <span className="text-sm font-semibold text-slate-900">{personData?.favorable_outcomes || 0}</span>
                </div>
              </div>
            </div>

            {/* Verification Status */}
            <div className="bg-white rounded-lg border border-slate-200 p-6">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center gap-2 mb-4">
                <XCircle className="h-5 w-5 text-red-600" />
                Verification Status
              </h3>
              <div className="text-center">
                <div className="text-lg font-semibold text-red-600 mb-2">
                  {personData?.verification_status || 'Not Verified'}
                </div>
                <div className="text-sm text-slate-600">
                  Verified on: {personData?.verified_on || 'N/A'}
                </div>
                <div className="text-sm text-slate-600">
                  {personData?.verified_on || 'N/A'}
                    </div>
                    </div>
                  </div>

            {/* Languages */}
            <div className="bg-white rounded-lg border border-slate-200 p-6">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center gap-2 mb-4">
                <Users className="h-5 w-5 text-blue-600" />
                Languages
              </h3>
              <div className="flex flex-wrap gap-2">
                {(personData?.languages || []).map((language, index) => (
                  <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                    {language}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PersonProfile;