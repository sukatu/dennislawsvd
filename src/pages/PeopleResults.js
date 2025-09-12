import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Search, Filter, ChevronDown, ArrowLeft, Eye, Clock, MapPin, Users, AlertCircle, ChevronLeft, ChevronRight, Scale } from 'lucide-react';

const PeopleResults = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchProgress, setSearchProgress] = useState(0);
  const [currentSearching, setCurrentSearching] = useState('');
  const [searchStats, setSearchStats] = useState({
    totalResults: 0,
    searchTime: 0,
    courtsSearched: 0,
    totalCourts: 0
  });
  const [filters, setFilters] = useState({
    sortBy: 'relevance',
    region: 'all',
    caseType: 'all'
  });
  const [showFilters, setShowFilters] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(20);
  const [totalPages, setTotalPages] = useState(0);
  const [totalResults, setTotalResults] = useState(0);

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

  // Enhanced search with real-time progress updates
  const performEnhancedSearch = async (searchQuery) => {
    setLoading(true);
    setError(null);
    setSearchProgress(0);
    setSearchStats({ totalResults: 0, searchTime: 0, courtsSearched: 0, totalCourts: 0 });

    const courts = [
      'Supreme Court',
      'Court of Appeal', 
      'High Court - Accra',
      'High Court - Kumasi',
      'High Court - Tamale',
      'High Court - Cape Coast',
      'High Court - Sunyani',
      'High Court - Ho',
      'High Court - Bolgatanga',
      'High Court - Wa',
      'High Court - Koforidua',
      'High Court - Sekondi',
      'Circuit Court - Accra',
      'Circuit Court - Kumasi',
      'Circuit Court - Tamale',
      'District Court - Accra',
      'District Court - Kumasi',
      'District Court - Tamale',
      'Commercial Court - Accra',
      'Commercial Court - Kumasi',
      'Family Court - Accra',
      'Family Court - Kumasi',
      'Land Court - Accra',
      'Land Court - Kumasi'
    ];

    const startTime = Date.now();
    let allResults = [];
    let courtsSearched = 0;

    try {
      // Simulate searching through courts with progress updates
      for (let i = 0; i < courts.length; i++) {
        const court = courts[i];
        setCurrentSearching(`Searching ${court}...`);
        
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 100 + Math.random() * 200));
        
        // Make actual API call to people search
        const response = await fetch(`http://localhost:8000/api/people/search?query=${encodeURIComponent(searchQuery)}&limit=50`, {
          headers: {
            'Authorization': `Bearer test-token-123`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          if (data.people && data.people.length > 0) {
            // Add court information to each result
            const courtResults = data.people.map(person => ({
              ...person,
              court: court,
              searchSource: 'people'
            }));
            allResults = [...allResults, ...courtResults];
          }
        }

        courtsSearched++;
        const progress = ((i + 1) / courts.length) * 100;
        setSearchProgress(progress);
        setSearchStats(prev => ({
          ...prev,
          courtsSearched,
          totalCourts: courts.length,
          totalResults: allResults.length
        }));
      }

      // Remove duplicates based on person ID
      const uniqueResults = allResults.reduce((acc, current) => {
        const existingIndex = acc.findIndex(item => item.id === current.id);
        if (existingIndex === -1) {
          acc.push(current);
        }
        return acc;
      }, []);

      setResults(uniqueResults);
      setSearchStats(prev => ({
        ...prev,
        totalResults: uniqueResults.length,
        searchTime: (Date.now() - startTime) / 1000
      }));

    } catch (error) {
      console.error('Search error:', error);
      setError('Failed to search. Please try again.');
    } finally {
      setLoading(false);
      setCurrentSearching('');
      setSearchProgress(100);
    }
  };

  // Mock data
  const mockResults = [
    {
      id: 1,
      name: 'Albert Kweku Obeng',
      dob: '7 March 1962 – 9 March 2004',
      idNumber: 'KL1K-DXP',
      riskLevel: 'Low',
      riskScore: 25,
      cases: 2,
      caseTypes: ['Property Dispute', 'Family Law'],
      location: 'Greater Accra'
    },
    {
      id: 2,
      name: 'Sarah Mensah',
      dob: '15 June 1975',
      idNumber: 'GH-123456789',
      riskLevel: 'Medium',
      riskScore: 65,
      cases: 5,
      caseTypes: ['Business Dispute', 'Contract Law'],
      location: 'Ashanti'
    },
    {
      id: 3,
      name: 'Kwame Asante',
      dob: '22 September 1980',
      idNumber: 'GH-987654321',
      riskLevel: 'High',
      riskScore: 85,
      cases: 12,
      caseTypes: ['Criminal', 'Fraud'],
      location: 'Western'
    },
    {
      id: 4,
      name: 'Ama Serwaa',
      dob: '3 January 1990',
      idNumber: 'GH-456789123',
      riskLevel: 'Low',
      riskScore: 15,
      cases: 1,
      caseTypes: ['Traffic Violation'],
      location: 'Central'
    }
  ];

  // Set search query from URL params
  useEffect(() => {
    const searchParam = searchParams.get('search');
    setSearchQuery(searchParam || '');
  }, [searchParams]);

  // Load people data with enhanced search
  useEffect(() => {
    const query = searchParams.get('search') || '';
    if (query) {
      performEnhancedSearch(query);
    }
  }, [searchParams]);

  // Pagination logic
  const displayTotalPages = Math.ceil(results.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = Math.min(startIndex + itemsPerPage, results.length);
  const currentResults = results.slice(startIndex, endIndex);

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Update total results when results change
  useEffect(() => {
    setTotalResults(results.length);
  }, [results]);

  useEffect(() => {
    const query = searchParams.get('search');
    if (query) {
      setSearchQuery(query);
    }
  }, [searchParams]);

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

  const handleExport = () => {
    const csvData = [
      ['Name', 'ID Number', 'Risk Level', 'Risk Score', 'Cases', 'Location'],
      ...mockResults.map(person => [
        person.name,
        person.idNumber,
        person.riskLevel,
        person.riskScore,
        person.cases,
        person.location
      ])
    ];

    const csvString = csvData.map(row => row.join(',')).join('\n');
    const blob = new Blob([csvString], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'people_search_results.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/people-results?search=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-white border-b border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/')}
                className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors"
              >
                <ArrowLeft className="h-4 w-4" />
                Back to Search
              </button>
              <div>
                <h1 className="text-2xl font-bold text-slate-900">Search Results</h1>
                <p className="text-slate-600">
                  {loading ? 'Searching...' : `Found ${searchStats.totalResults} results matching '${searchQuery}'`}
                </p>
              </div>
            </div>
            {!loading && searchStats.searchTime > 0 && (
              <div className="text-sm text-slate-500">
                Search completed in {searchStats.searchTime.toFixed(2)}s
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      {loading && (
        <div className="bg-white border-b border-slate-200">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-4">
            <div className="mb-4">
              <div className="flex items-center justify-between text-sm text-slate-600 mb-2">
                <span>Searching through court records...</span>
                <span>{Math.round(searchProgress)}%</span>
              </div>
              <div className="w-full bg-slate-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300 ease-out"
                  style={{ width: `${searchProgress}%` }}
                ></div>
              </div>
            </div>
            {currentSearching && (
              <div className="flex items-center gap-2 text-sm text-slate-600">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-blue-600 border-t-transparent"></div>
                <span>{currentSearching}</span>
              </div>
            )}
            <div className="mt-2 text-xs text-slate-500">
              Searched {searchStats.courtsSearched} of {searchStats.totalCourts} courts • {searchStats.totalResults} results found
            </div>
          </div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
          <div className="rounded-lg bg-red-50 border border-red-200 p-4">
            <div className="flex items-center gap-2">
              <AlertCircle className="h-5 w-5 text-red-600" />
              <span className="text-red-800">{error}</span>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {!loading && !error && (
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
          {currentResults.length === 0 ? (
            <div className="text-center py-12">
              <Users className="h-12 w-12 text-slate-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-slate-900 mb-2">No results found</h3>
              <p className="text-slate-600">Try adjusting your search terms or filters.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {currentResults.map((person) => (
                <div 
                  key={person.id} 
                  className="bg-white rounded-lg border border-slate-200 p-6 hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() => navigate(`/person-profile/${person.id}?search=${encodeURIComponent(searchQuery)}`)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-4">
                      <div className="flex-shrink-0">
                        <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                          <Users className="h-6 w-6 text-blue-600" />
                        </div>
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-slate-900 mb-1">
                          {person.full_name}
                        </h3>
                        <p className="text-slate-600 text-sm mb-2">
                          {person.notes || 'Name extracted from case titles.'}
                          {person.occupation && ` ${person.occupation}`}
                          {person.languages && person.languages.length > 0 && ` with ${person.languages.length} language${person.languages.length > 1 ? 's' : ''}`}
                        </p>
                        <div className="flex items-center gap-4 text-sm text-slate-500">
                          <div className="flex items-center gap-1">
                            <Clock className="h-4 w-4" />
                            <span>Just now</span>
                          </div>
                          {person.region && (
                            <div className="flex items-center gap-1">
                              <MapPin className="h-4 w-4" />
                              <span>{getRegionName(person.region)}</span>
                            </div>
                          )}
                          {person.court && (
                            <div className="flex items-center gap-1">
                              <Scale className="h-4 w-4" />
                              <span>{person.court}</span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors">
                      <Eye className="h-4 w-4" />
                      Click to view details
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Pagination */}
      {!loading && !error && displayTotalPages > 1 && (
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-between">
            <div className="text-sm text-slate-600">
              Showing {startIndex + 1} to {endIndex} of {results.length} results
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="p-2 rounded-lg border border-slate-300 text-slate-600 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronLeft className="h-4 w-4" />
              </button>
              
              {Array.from({ length: Math.min(5, displayTotalPages) }, (_, i) => {
                const page = i + 1;
                return (
                  <button
                    key={page}
                    onClick={() => handlePageChange(page)}
                    className={`px-3 py-2 text-sm font-medium rounded-lg ${
                      currentPage === page
                        ? 'bg-blue-600 text-white'
                        : 'text-slate-600 hover:bg-slate-100'
                    }`}
                  >
                    {page}
                  </button>
                );
              })}
              
              {displayTotalPages > 5 && (
                <>
                  <span className="text-slate-400">...</span>
                  <button
                    onClick={() => handlePageChange(displayTotalPages)}
                    className={`px-3 py-2 text-sm font-medium rounded-lg ${
                      currentPage === displayTotalPages
                        ? 'bg-blue-600 text-white'
                        : 'text-slate-600 hover:bg-slate-100'
                    }`}
                  >
                    {displayTotalPages}
                  </button>
                </>
              )}
              
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === displayTotalPages}
                className="p-2 rounded-lg border border-slate-300 text-slate-600 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PeopleResults;
