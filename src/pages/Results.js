import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Eye, Download, Gavel, User, Search, Filter, ChevronDown, ChevronUp, ChevronLeft, ChevronRight } from 'lucide-react';

const Results = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [searchResults, setSearchResults] = useState([]);
  const [filteredResults, setFilteredResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showFilters, setShowFilters] = useState(false);
  const [sortBy, setSortBy] = useState('date');
  const [filterBy, setFilterBy] = useState({
    court: 'all',
    status: 'all',
    dateRange: 'all'
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);

  // Enhanced mock data with more details
  const mockSearchResults = [
    {
      caseId: 1,
      title: 'Property Dispute vs. Estate of John Doe',
      date: '2022-01-01',
      judge: 'Justice Sarah Mensah',
      lawyers: 'Kwame Asante, Legal Counsel',
      summary: 'This case involved a property dispute between Albert Kweku Obeng and the estate of John Doe. The dispute centered around the ownership of a residential property in Accra.',
      status: 'Resolved',
      court: 'High Court, Accra',
      courtType: 'High Court',
      region: 'Greater Accra'
    },
    {
      caseId: 2,
      title: 'Business Contract Dispute',
      date: '2021-02-01',
      judge: 'Justice Michael Osei',
      lawyers: 'Ama Serwaa, Legal Counsel',
      summary: 'A business contract dispute between two companies regarding the delivery of goods and payment terms. The case involved complex commercial law principles.',
      status: 'Active',
      court: 'Commercial Court, Accra',
      courtType: 'Commercial Court',
      region: 'Greater Accra'
    },
    {
      caseId: 3,
      title: 'Family Inheritance Matter',
      date: '2021-03-15',
      judge: 'Justice Comfort Asante',
      lawyers: 'Kwame Nkrumah, Legal Counsel',
      summary: 'Family dispute over inheritance of property and assets. The case involved multiple family members and required careful consideration of inheritance laws.',
      status: 'Resolved',
      court: 'Family Court, Kumasi',
      courtType: 'Family Court',
      region: 'Ashanti'
    },
    {
      caseId: 4,
      title: 'Criminal Fraud Case',
      date: '2023-05-20',
      judge: 'Justice David Owusu',
      lawyers: 'Mary Adjei, Legal Counsel',
      summary: 'Criminal case involving fraud and embezzlement of company funds. The defendant was charged with multiple counts of financial crimes.',
      status: 'Pending',
      court: 'Criminal Court, Accra',
      courtType: 'Criminal Court',
      region: 'Greater Accra'
    },
    {
      caseId: 5,
      title: 'Employment Dispute',
      date: '2023-08-10',
      judge: 'Justice Grace Appiah',
      lawyers: 'John Mensah, Legal Counsel',
      summary: 'Employment dispute regarding wrongful termination and unpaid benefits. The plaintiff seeks compensation for lost wages and damages.',
      status: 'Active',
      court: 'Labor Court, Kumasi',
      courtType: 'Labor Court',
      region: 'Ashanti'
    }
  ];

  // Filter and sort results
  useEffect(() => {
    let filtered = [...searchResults];

    // Apply filters
    if (filterBy.court !== 'all') {
      filtered = filtered.filter(result => result.courtType === filterBy.court);
    }
    if (filterBy.status !== 'all') {
      filtered = filtered.filter(result => result.status === filterBy.status);
    }

    // Apply sorting
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return new Date(b.date) - new Date(a.date);
        case 'court':
          return a.courtType.localeCompare(b.courtType);
        case 'status':
          return a.status.localeCompare(b.status);
        case 'title':
          return a.title.localeCompare(b.title);
        default:
          return 0;
      }
    });

    setFilteredResults(filtered);
    setCurrentPage(1); // Reset to first page when filters change
  }, [searchResults, filterBy, sortBy]);

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
    const searchQuery = searchParams.get('search_query');
    
    // Simulate API call
    const fetchResults = async () => {
      setLoading(true);
      // Simulate loading delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      if (searchQuery) {
        // Filter results based on search query
        const filteredResults = mockSearchResults.filter(result =>
          result.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          result.summary.toLowerCase().includes(searchQuery.toLowerCase())
        );
        setSearchResults(filteredResults);
      } else {
        setSearchResults(mockSearchResults);
      }
      
      setLoading(false);
    };

    fetchResults();
  }, [searchParams]);

  const handleViewCase = (caseId) => {
    navigate(`/case-detail?caseId=${caseId}&source=search`);
  };

  const handleDownload = (caseId) => {
    // Handle download logic
    console.log('Downloading case:', caseId);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-sky-600 mx-auto"></div>
          <p className="mt-4 text-slate-600">Searching cases...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <header className="bg-slate-900 text-white">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="h-8 w-8 rounded-full bg-sky-400 flex items-center justify-center">
                <Gavel className="h-4 w-4 text-white" />
              </div>
              <h1 className="text-xl font-bold">Dennislaw SVD</h1>
            </div>
            <nav className="hidden md:flex space-x-6">
              <button
                onClick={() => navigate('/')}
                className="hover:text-sky-400 transition-colors"
              >
                Home
              </button>
              <button
                onClick={() => navigate('/people-database')}
                className="hover:text-sky-400 transition-colors"
              >
                People Database
              </button>
              <button
                onClick={() => navigate('/advanced-search')}
                className="hover:text-sky-400 transition-colors"
              >
                Advanced Search
              </button>
              <button
                onClick={() => navigate('/about')}
                className="hover:text-sky-400 transition-colors"
              >
                About
              </button>
              <button
                onClick={() => navigate('/contact')}
                className="hover:text-sky-400 transition-colors"
              >
                Contact
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="min-h-screen bg-slate-50 py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            {/* Header */}
            <div className="mb-8">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h1 className="text-3xl font-bold text-slate-900 mb-2">Search Results</h1>
                  <p className="text-slate-600">
                    Found <span className="font-semibold">{filteredResults.length}</span> cases matching your search
                  </p>
                </div>
                <button
                  onClick={() => navigate('/')}
                  className="bg-slate-200 hover:bg-slate-300 text-slate-700 font-semibold py-3 px-6 rounded-lg transition-colors flex items-center"
                >
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Back to Search
                </button>
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
                  <option value="date">Sort by Date</option>
                  <option value="court">Sort by Court</option>
                  <option value="status">Sort by Status</option>
                  <option value="title">Sort by Title</option>
                </select>
              </div>

              {/* Collapsible Filter Options */}
              {showFilters && (
                <div className="bg-white border border-slate-200 rounded-lg p-6 mb-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Court Type Filter */}
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Court Type</label>
                      <select
                        value={filterBy.court}
                        onChange={(e) => setFilterBy({...filterBy, court: e.target.value})}
                        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
                      >
                        <option value="all">All Courts</option>
                        <option value="High Court">High Court</option>
                        <option value="Commercial Court">Commercial Court</option>
                        <option value="Family Court">Family Court</option>
                        <option value="Criminal Court">Criminal Court</option>
                        <option value="Labor Court">Labor Court</option>
                      </select>
                    </div>

                    {/* Status Filter */}
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Case Status</label>
                      <select
                        value={filterBy.status}
                        onChange={(e) => setFilterBy({...filterBy, status: e.target.value})}
                        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
                      >
                        <option value="all">All Status</option>
                        <option value="Active">Active</option>
                        <option value="Resolved">Resolved</option>
                        <option value="Pending">Pending</option>
                      </select>
                    </div>

                    {/* Date Range Filter */}
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">Date Range</label>
                      <select
                        value={filterBy.dateRange}
                        onChange={(e) => setFilterBy({...filterBy, dateRange: e.target.value})}
                        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
                      >
                        <option value="all">All Dates</option>
                        <option value="2024">2024</option>
                        <option value="2023">2023</option>
                        <option value="2022">2022</option>
                        <option value="2021">2021</option>
                      </select>
                    </div>
                  </div>

                  {/* Clear Filters Button */}
                  <div className="mt-4 flex justify-end">
                    <button
                      onClick={() => setFilterBy({court: 'all', status: 'all', dateRange: 'all'})}
                      className="text-sm text-slate-600 hover:text-slate-800 transition-colors"
                    >
                      Clear all filters
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Results */}
            {filteredResults.length === 0 ? (
              <div className="text-center py-12">
                <Search className="h-16 w-16 text-slate-300 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-slate-600 mb-2">No results found</h3>
                <p className="text-slate-500">Try adjusting your search terms or filters</p>
              </div>
            ) : (
              <div className="space-y-6">
                {currentResults.map((result) => (
                  <div
                    key={result.caseId}
                    className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <h3 className="text-xl font-semibold text-slate-900">{result.title}</h3>
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          result.status === 'Active' ? 'bg-amber-100 text-amber-700' :
                          result.status === 'Resolved' ? 'bg-emerald-100 text-emerald-700' :
                          'bg-slate-100 text-slate-700'
                        }`}>
                          {result.status}
                        </span>
                        <span className="text-sm text-slate-500">{result.date}</span>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                      <div className="flex items-center text-slate-600">
                        <Gavel className="h-4 w-4 mr-2" />
                        <span>{result.judge}</span>
                      </div>
                      <div className="flex items-center text-slate-600">
                        <User className="h-4 w-4 mr-2" />
                        <span>{result.lawyers}</span>
                      </div>
                    </div>
                    
                    <p className="text-slate-600 mb-6">{result.summary}</p>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4 text-sm text-slate-500">
                        <span>Court: <span className="font-medium text-slate-700">{result.courtType}</span></span>
                        <span>Region: <span className="font-medium text-slate-700">{result.region}</span></span>
                      </div>
                      
                      <div className="flex space-x-4">
                        <button
                          onClick={() => handleViewCase(result.caseId)}
                          className="bg-sky-500 hover:bg-sky-600 text-white font-semibold py-2 px-6 rounded-lg transition-colors flex items-center"
                        >
                          <Eye className="h-4 w-4 mr-2" />
                          View Case Details
                        </button>
                        <button
                          onClick={() => handleDownload(result.caseId)}
                          className="bg-slate-200 hover:bg-slate-300 text-slate-700 font-semibold py-2 px-6 rounded-lg transition-colors flex items-center"
                        >
                          <Download className="h-4 w-4 mr-2" />
                          Download
                        </button>
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
      </main>
    </div>
  );
};

export default Results;
