import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Grid, List, Download, Search, Filter, ChevronDown, ChevronUp, ChevronLeft, ChevronRight } from 'lucide-react';

const PeopleResults = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [viewMode, setViewMode] = useState('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('name');
  const [filteredResults, setFilteredResults] = useState([]);
  const [showFilters, setShowFilters] = useState(false);
  const [sortBy, setSortBy] = useState('name');
  const [filterBy, setFilterBy] = useState({
    riskLevel: 'all',
    location: 'all',
    caseCount: 'all'
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(12);

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

  // Filter and sort results
  useEffect(() => {
    let filtered = [...mockResults];

    // Apply filters
    if (filterBy.riskLevel !== 'all') {
      filtered = filtered.filter(person => person.riskLevel === filterBy.riskLevel);
    }
    if (filterBy.location !== 'all') {
      filtered = filtered.filter(person => person.location === filterBy.location);
    }
    if (filterBy.caseCount !== 'all') {
      const caseCount = parseInt(filterBy.caseCount);
      filtered = filtered.filter(person => person.cases >= caseCount);
    }

    // Apply sorting
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.name.localeCompare(b.name);
        case 'risk':
          return b.riskScore - a.riskScore;
        case 'cases':
          return b.cases - a.cases;
        case 'location':
          return a.location.localeCompare(b.location);
        default:
          return 0;
      }
    });

    setFilteredResults(filtered);
    setCurrentPage(1); // Reset to first page when filters change
  }, [filterBy, sortBy]);

  // Pagination logic
  const totalPages = Math.ceil(filteredResults.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentResults = filteredResults.slice(startIndex, endIndex);

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

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
    <div>
      {/* Search Section */}
      <div className="bg-white border-b border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-slate-900 mb-2">Look Up Anyone!</h1>
            <p className="text-lg text-slate-600">Search our comprehensive database of people and legal cases</p>
          </div>
          
          {/* Search Tabs */}
          <div className="flex justify-center mb-6">
            <div className="flex rounded-lg border border-slate-200 bg-slate-50 p-1">
              {['name', 'id', 'address'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                    activeTab === tab
                      ? 'text-slate-900 bg-white shadow-sm'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {tab === 'id' ? 'ID Number' : tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>
          </div>
          
          {/* Search Form */}
          <div className="max-w-2xl mx-auto">
            <form onSubmit={handleSearch} className="flex gap-2">
              <input
                type="text"
                placeholder={`Enter ${activeTab}...`}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex-1 rounded-lg border border-slate-300 px-4 py-3 text-sm focus:border-sky-500 focus:ring-1 focus:ring-sky-500"
              />
              <button
                type="submit"
                className="rounded-lg bg-sky-600 px-6 py-3 text-sm font-medium text-white hover:bg-sky-700 transition-colors"
              >
                Search
              </button>
            </form>
            <p className="text-center text-sm text-slate-500 mt-2">{filteredResults.length} results found</p>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-slate-50 border-b border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="text-center">
              <div className="text-2xl font-bold text-slate-900">464</div>
              <div className="text-sm text-slate-600">Courts Connected</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-slate-900">16</div>
              <div className="text-sm text-slate-600">Regions Covered</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-slate-900">Daily</div>
              <div className="text-sm text-slate-600">Updated</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-4">
          {/* Filters */}
          <div className="lg:col-span-1">
            <div className="rounded-xl border border-slate-200 bg-white p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Filters</h3>
              
              {/* Risk Level */}
              <div className="mb-6">
                <h4 className="text-sm font-medium text-slate-900 mb-3">Risk Level</h4>
                <div className="space-y-2">
                  {['Criminal', 'Civil', 'Family'].map((type) => (
                    <label key={type} className="flex items-center">
                      <input
                        type="checkbox"
                        className="rounded border-slate-300 text-sky-600 focus:ring-sky-500"
                        defaultChecked={type === 'Criminal'}
                      />
                      <span className="ml-2 text-sm text-slate-700">{type}</span>
                    </label>
                  ))}
                </div>
              </div>
              
              {/* Date Range */}
              <div className="mb-6">
                <h4 className="text-sm font-medium text-slate-900 mb-3">Date Range</h4>
                <div className="space-y-2">
                  <input
                    type="date"
                    className="w-full rounded border border-slate-300 px-3 py-2 text-sm focus:border-sky-500 focus:ring-1 focus:ring-sky-500"
                  />
                  <input
                    type="date"
                    className="w-full rounded border border-slate-300 px-3 py-2 text-sm focus:border-sky-500 focus:ring-1 focus:ring-sky-500"
                  />
                </div>
              </div>
              
              {/* Location */}
              <div className="mb-6">
                <h4 className="text-sm font-medium text-slate-900 mb-3">Location</h4>
                <select className="w-full rounded border border-slate-300 px-3 py-2 text-sm focus:border-sky-500 focus:ring-1 focus:ring-sky-500">
                  <option>All Regions</option>
                  <option>Greater Accra</option>
                  <option>Ashanti</option>
                  <option>Western</option>
                </select>
              </div>
              
              <button className="w-full rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700 transition-colors">
                Apply Filters
              </button>
            </div>
          </div>
          
          {/* Results */}
          <div className="lg:col-span-3">
            {/* Results Header with View Toggle and Export */}
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-slate-900">Search Results</h2>
              <div className="flex items-center gap-3">
                {/* View Toggle */}
                <div className="flex rounded-lg border border-slate-200 bg-slate-50 p-1">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                      viewMode === 'grid'
                        ? 'text-slate-900 bg-white shadow-sm'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    <Grid className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                      viewMode === 'list'
                        ? 'text-slate-900 bg-white shadow-sm'
                        : 'text-slate-600 hover:text-slate-900'
                    }`}
                  >
                    <List className="h-4 w-4" />
                  </button>
                </div>
                
                {/* Export Button */}
                <button
                  onClick={handleExport}
                  className="inline-flex items-center gap-2 rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors"
                >
                  <Download className="h-4 w-4" />
                  Export
                </button>
              </div>
            </div>

            {/* Filter Dropdown */}
            <div className="flex items-center gap-4 mb-6">
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="inline-flex items-center gap-2 rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors"
              >
                <Filter className="h-4 w-4" />
                Filter by
                {showFilters ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
              </button>

              {/* Sort Dropdown */}
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
              >
                <option value="name">Sort by Name</option>
                <option value="risk">Sort by Risk</option>
                <option value="cases">Sort by Cases</option>
                <option value="location">Sort by Location</option>
              </select>
            </div>

            {/* Collapsible Filter Options */}
            {showFilters && (
              <div className="bg-white border border-slate-200 rounded-lg p-6 mb-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {/* Risk Level Filter */}
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Risk Level</label>
                    <select
                      value={filterBy.riskLevel}
                      onChange={(e) => setFilterBy({...filterBy, riskLevel: e.target.value})}
                      className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
                    >
                      <option value="all">All Risk Levels</option>
                      <option value="Low">Low Risk</option>
                      <option value="Medium">Medium Risk</option>
                      <option value="High">High Risk</option>
                    </select>
                  </div>

                  {/* Location Filter */}
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Location</label>
                    <select
                      value={filterBy.location}
                      onChange={(e) => setFilterBy({...filterBy, location: e.target.value})}
                      className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
                    >
                      <option value="all">All Locations</option>
                      <option value="Greater Accra">Greater Accra</option>
                      <option value="Ashanti">Ashanti</option>
                      <option value="Western">Western</option>
                      <option value="Central">Central</option>
                    </select>
                  </div>

                  {/* Case Count Filter */}
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Minimum Cases</label>
                    <select
                      value={filterBy.caseCount}
                      onChange={(e) => setFilterBy({...filterBy, caseCount: e.target.value})}
                      className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
                    >
                      <option value="all">All Cases</option>
                      <option value="1">1+ Cases</option>
                      <option value="3">3+ Cases</option>
                      <option value="5">5+ Cases</option>
                      <option value="10">10+ Cases</option>
                    </select>
                  </div>
                </div>

                {/* Clear Filters Button */}
                <div className="mt-4 flex justify-end">
                  <button
                    onClick={() => setFilterBy({riskLevel: 'all', location: 'all', caseCount: 'all'})}
                    className="text-sm text-slate-600 hover:text-slate-800 transition-colors"
                  >
                    Clear all filters
                  </button>
                </div>
              </div>
            )}

            {/* Results Display */}
            {viewMode === 'grid' ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {currentResults.map((person) => (
                  <div key={person.id} className="rounded-xl border border-slate-200 bg-white p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-semibold text-slate-900">{person.name}</h3>
                          <span className={`inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs font-semibold ring-1 ${getRiskColor(person.riskLevel)}`}>
                            <span className={`inline-block h-1.5 w-1.5 rounded-full ${getRiskColor(person.riskLevel).split(' ')[1].replace('text-', 'bg-')}`}></span>
                            {person.riskLevel} Risk
                          </span>
                        </div>
                        <p className="text-sm text-slate-600 mb-2">{person.dob} • {person.idNumber}</p>
                        <div className="flex items-center gap-4 text-sm text-slate-500">
                          <span>{person.cases} Cases</span>
                          <span>•</span>
                          <span>{person.caseTypes.join(', ')}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`text-2xl font-bold ${getRiskScoreColor(person.riskScore)}`}>
                          {person.riskScore}
                        </span>
                        <div className="text-right">
                          <div className="text-xs text-slate-500">Risk Score</div>
                          <div className="w-16 bg-slate-200 rounded-full h-1.5 mt-1">
                            <div
                              className={`h-1.5 rounded-full ${getProgressBarColor(person.riskScore)}`}
                              style={{ width: `${person.riskScore}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => navigate(`/person-profile?id=${person.id}`)}
                        className="flex-1 text-center rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700 transition-colors"
                      >
                        View Profile
                      </button>
                      <button className="px-3 py-2 text-sm font-medium text-slate-700 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors">
                        <Download className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="space-y-4">
                {currentResults.map((person) => (
                  <div key={person.id} className="rounded-xl border border-slate-200 bg-white p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-semibold text-slate-900">{person.name}</h3>
                          <span className={`inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs font-semibold ring-1 ${getRiskColor(person.riskLevel)}`}>
                            <span className={`inline-block h-1.5 w-1.5 rounded-full ${getRiskColor(person.riskLevel).split(' ')[1].replace('text-', 'bg-')}`}></span>
                            {person.riskLevel} Risk
                          </span>
                        </div>
                        <p className="text-sm text-slate-600 mb-2">{person.dob} • {person.idNumber}</p>
                        <div className="flex items-center gap-4 text-sm text-slate-500">
                          <span>{person.cases} Cases</span>
                          <span>•</span>
                          <span>{person.caseTypes.join(', ')}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2">
                          <span className={`text-2xl font-bold ${getRiskScoreColor(person.riskScore)}`}>
                            {person.riskScore}
                          </span>
                          <div className="text-right">
                            <div className="text-xs text-slate-500">Risk Score</div>
                            <div className="w-16 bg-slate-200 rounded-full h-1.5 mt-1">
                              <div
                                className={`h-1.5 rounded-full ${getProgressBarColor(person.riskScore)}`}
                                style={{ width: `${person.riskScore}%` }}
                              ></div>
                            </div>
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <button
                            onClick={() => navigate(`/person-profile?id=${person.id}`)}
                            className="rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700 transition-colors"
                          >
                            View Profile
                          </button>
                          <button className="px-3 py-2 text-sm font-medium text-slate-700 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors">
                            <Download className="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-8 flex items-center justify-between">
                <div className="text-sm text-slate-600">
                  Showing {startIndex + 1} to {Math.min(endIndex, filteredResults.length)} of {filteredResults.length} results
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
          </div>
        </div>
      </div>
    </div>
  );
};

export default PeopleResults;
