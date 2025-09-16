import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Grid, List, Search, Filter, ChevronDown, ChevronUp, ChevronLeft, ChevronRight, User, RotateCcw, Plus } from 'lucide-react';
import AuthGuard from '../components/AuthGuard';

const People = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [activeTab, setActiveTab] = useState('search'); // 'search', 'advanced', 'database'
  const [viewMode, setViewMode] = useState('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredResults, setFilteredResults] = useState([]);
  const [allPeople, setAllPeople] = useState([]); // For alphabet grouping
  const [showFilters, setShowFilters] = useState(false);
  const [sortBy, setSortBy] = useState('name');
  const [filterBy, setFilterBy] = useState({
    riskLevel: 'all',
    location: 'all',
    caseCount: 'all'
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(20);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [isLoadingSuggestions, setIsLoadingSuggestions] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [totalResults, setTotalResults] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedLetter, setSelectedLetter] = useState(null);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [loadingStatus, setLoadingStatus] = useState('');
  const [isLoadingAllPeople, setIsLoadingAllPeople] = useState(false);

  // Advanced search form data
  const [advancedFormData, setAdvancedFormData] = useState({
    firstName: '',
    lastName: '',
    idNumber: '',
    phone: '',
    email: '',
    address: '',
    caseType: '',
    court: '',
    caseStatus: '',
    dateRange: '',
    region: '',
    city: ''
  });

  // Mock data
  const mockResults = [
    {
      id: 1,
      name: 'Albert Kweku Obeng',
      idNumber: 'KL1K-DXP',
      riskLevel: 'Low',
      riskScore: 25,
      cases: 2,
      caseTypes: ['Property Dispute', 'Family Law'],
      location: 'Greater Accra',
      lastUpdated: '2 hours ago'
    },
    {
      id: 2,
      name: 'Sarah Mensah',
      idNumber: 'GH-123456789',
      riskLevel: 'Medium',
      riskScore: 65,
      cases: 5,
      caseTypes: ['Business Dispute', 'Contract Law'],
      location: 'Ashanti',
      lastUpdated: '1 day ago'
    },
    {
      id: 3,
      name: 'Kwame Asante',
      idNumber: 'GH-987654321',
      riskLevel: 'High',
      riskScore: 85,
      cases: 12,
      caseTypes: ['Criminal', 'Fraud'],
      location: 'Western',
      lastUpdated: '3 days ago'
    },
    {
      id: 4,
      name: 'Ama Serwaa',
      idNumber: 'GH-456789123',
      riskLevel: 'Low',
      riskScore: 30,
      cases: 1,
      caseTypes: ['Family Law'],
      location: 'Central',
      lastUpdated: '1 week ago'
    },
    {
      id: 5,
      name: 'John Osei',
      idNumber: 'GH-789123456',
      riskLevel: 'Medium',
      riskScore: 55,
      cases: 8,
      caseTypes: ['Business Dispute', 'Property Dispute'],
      location: 'Eastern',
      lastUpdated: '2 days ago'
    },
    {
      id: 6,
      name: 'Grace Adjei',
      idNumber: 'GH-321654987',
      riskLevel: 'High',
      riskScore: 90,
      cases: 15,
      caseTypes: ['Criminal', 'Fraud', 'Money Laundering'],
      location: 'Volta',
      lastUpdated: '4 hours ago'
    },
    {
      id: 7,
      name: 'Michael Boateng',
      idNumber: 'GH-654987321',
      riskLevel: 'Low',
      riskScore: 20,
      cases: 3,
      caseTypes: ['Contract Law'],
      location: 'Northern',
      lastUpdated: '5 days ago'
    },
    {
      id: 8,
      name: 'Patience Owusu',
      idNumber: 'GH-147258369',
      riskLevel: 'Medium',
      riskScore: 60,
      cases: 7,
      caseTypes: ['Family Law', 'Property Dispute'],
      location: 'Upper East',
      lastUpdated: '1 day ago'
    },
    {
      id: 9,
      name: 'Samuel Kofi',
      idNumber: 'GH-963852741',
      riskLevel: 'High',
      riskScore: 80,
      cases: 11,
      caseTypes: ['Criminal', 'Business Dispute'],
      location: 'Upper West',
      lastUpdated: '6 hours ago'
    },
    {
      id: 10,
      name: 'Comfort Asante',
      idNumber: 'GH-852741963',
      riskLevel: 'Low',
      riskScore: 35,
      cases: 2,
      caseTypes: ['Family Law'],
      location: 'Brong-Ahafo',
      lastUpdated: '3 days ago'
    },
    {
      id: 11,
      name: 'Daniel Nkrumah',
      idNumber: 'GH-741852963',
      riskLevel: 'Medium',
      riskScore: 70,
      cases: 9,
      caseTypes: ['Business Dispute', 'Contract Law'],
      location: 'Greater Accra',
      lastUpdated: '2 days ago'
    },
    {
      id: 12,
      name: 'Esther Ofori',
      idNumber: 'GH-159753486',
      riskLevel: 'High',
      riskScore: 95,
      cases: 18,
      caseTypes: ['Criminal', 'Fraud', 'Money Laundering', 'Drug Trafficking'],
      location: 'Ashanti',
      lastUpdated: '1 hour ago'
    }
  ];


  // Handle URL search parameters
  useEffect(() => {
    const searchFromUrl = searchParams.get('search');
    if (searchFromUrl) {
      setSearchQuery(searchFromUrl);
      setActiveTab('search');
    }
  }, [searchParams]);

  // Load all people for alphabet grouping
  const loadAllPeopleForAlphabet = async () => {
    try {
      console.log('Loading all people for alphabet grouping...');
      setIsLoadingAllPeople(true);
      setLoadingProgress(0);
      setLoadingStatus('Connecting to database...');
      
      const token = localStorage.getItem('accessToken');
      
      const headers = {
        'Content-Type': 'application/json'
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      // First, get the total count
      console.log('Getting total count...');
      setLoadingStatus('Getting total count...');
      setLoadingProgress(5);
      
      const countResponse = await fetch(`http://localhost:8000/api/people/search?page=1&limit=1`, { headers });
      if (!countResponse.ok) {
        throw new Error(`Count API failed: ${countResponse.status}`);
      }
      const countData = await countResponse.json();
      const totalPeople = countData.total || 0;
      console.log('Total people in database:', totalPeople);

      // Load all people in batches
      const allPeopleData = [];
      const batchSize = 100; // Load 100 at a time
      const totalPages = Math.ceil(totalPeople / batchSize);
      
      console.log(`Loading ${totalPeople} people in ${totalPages} batches of ${batchSize}...`);
      setLoadingStatus(`Loading ${totalPeople} people in ${totalPages} batches...`);
      setLoadingProgress(10);
      
      for (let page = 1; page <= totalPages; page++) {
        console.log(`Loading batch ${page}/${totalPages}...`);
        setLoadingStatus(`Loading batch ${page} of ${totalPages}...`);
        
        const response = await fetch(`http://localhost:8000/api/people/search?page=${page}&limit=${batchSize}`, { headers });
        
        if (response.ok) {
          const data = await response.json();
          allPeopleData.push(...(data.people || []));
          console.log(`Batch ${page} loaded: ${data.people?.length || 0} people`);
          
          // Update progress
          const progress = 10 + ((page / totalPages) * 80); // 10% to 90%
          setLoadingProgress(Math.round(progress));
        } else {
          console.error(`Batch ${page} failed:`, response.status, response.statusText);
        }
      }

      console.log(`Total people loaded: ${allPeopleData.length}`);
      setLoadingStatus('Processing data...');
      setLoadingProgress(90);
      
      const transformedResults = allPeopleData.map(person => ({
        id: person.id,
        name: person.full_name || `${person.first_name} ${person.last_name}`,
        idNumber: person.id_number || 'N/A',
        riskLevel: person.risk_level || 'Low',
        riskScore: person.risk_score || 0,
        cases: person.case_count || 0,
        caseTypes: person.case_types || [],
        location: person.region || 'N/A'
      }));

      console.log('Transformed results sample:', transformedResults.slice(0, 3));
      setAllPeople(transformedResults);
      setLoadingStatus('Complete!');
      setLoadingProgress(100);
      console.log('All people set successfully');
      
      // Hide loading after a short delay
      setTimeout(() => {
        setIsLoadingAllPeople(false);
        setLoadingProgress(0);
        setLoadingStatus('');
      }, 1000);
      
    } catch (error) {
      console.error('Error loading all people for alphabet:', error);
      setLoadingStatus('Error loading data, using fallback...');
      setLoadingProgress(0);
      
      // Fallback to sample data if API fails
      console.log('Using fallback sample data due to error...');
      const sampleData = [
        { id: 1, name: 'AARON KWESI KAITOO', idNumber: 'N/A', riskLevel: 'Low', riskScore: 0, cases: 0, caseTypes: [], location: 'UER' },
        { id: 2, name: 'AARON MFARFO', idNumber: 'N/A', riskLevel: 'Low', riskScore: 0, cases: 0, caseTypes: [], location: 'WR' },
        { id: 3, name: 'AARON MORNY GODWIN', idNumber: 'N/A', riskLevel: 'Low', riskScore: 0, cases: 0, caseTypes: [], location: 'GAR' },
        { id: 4, name: 'BENJAMIN ADJEI', idNumber: 'N/A', riskLevel: 'Medium', riskScore: 50, cases: 2, caseTypes: ['Civil'], location: 'ASR' },
        { id: 5, name: 'CHARLES OWUSU', idNumber: 'N/A', riskLevel: 'High', riskScore: 80, cases: 5, caseTypes: ['Criminal'], location: 'GAR' },
        { id: 6, name: 'DAVID MENSAH', idNumber: 'N/A', riskLevel: 'Low', riskScore: 20, cases: 1, caseTypes: ['Civil'], location: 'WR' },
        { id: 7, name: 'EMMANUEL ASANTE', idNumber: 'N/A', riskLevel: 'Medium', riskScore: 60, cases: 3, caseTypes: ['Commercial'], location: 'ER' },
        { id: 8, name: 'FRANCIS GYASI', idNumber: 'N/A', riskLevel: 'Low', riskScore: 30, cases: 1, caseTypes: ['Civil'], location: 'VR' },
        { id: 9, name: 'GEORGE APPIAH', idNumber: 'N/A', riskLevel: 'High', riskScore: 90, cases: 7, caseTypes: ['Criminal', 'Fraud'], location: 'GAR' },
        { id: 10, name: 'HENRY BOATENG', idNumber: 'N/A', riskLevel: 'Medium', riskScore: 55, cases: 2, caseTypes: ['Civil'], location: 'ASR' }
      ];
      setAllPeople(sampleData);
      console.log('Fallback sample data set due to error');
      
      setTimeout(() => {
        setIsLoadingAllPeople(false);
        setLoadingProgress(0);
        setLoadingStatus('');
      }, 2000);
    }
  };

  // Load all people for alphabet grouping on component mount
  useEffect(() => {
    console.log('Component mounted, loading all people...');
    loadAllPeopleForAlphabet();
  }, []);

  // Handle search when search query changes
  useEffect(() => {
    if (searchQuery.trim()) {
      handleSearch();
      } else {
      // If no search query, reload all people
      const loadAllPeople = async () => {
        try {
          console.log('Loading people for current page...');
          const token = localStorage.getItem('accessToken');
          
          const headers = {
            'Content-Type': 'application/json'
          };
          
          if (token) {
            headers['Authorization'] = `Bearer ${token}`;
          }

          setIsLoading(true);
          console.log('Making API call for paginated people...');
          const response = await fetch(`http://localhost:8000/api/people/search?page=${currentPage}&limit=${itemsPerPage}`, {
            headers
          });

          console.log('Paginated API response status:', response.status);
          if (response.ok) {
            const data = await response.json();
            console.log('Paginated API response data:', data);
            console.log('Number of people received:', data.people?.length || 0);
            
            const transformedResults = (data.people || []).map(person => ({
              id: person.id,
              name: person.full_name || `${person.first_name} ${person.last_name}`,
              idNumber: person.id_number || 'N/A',
              riskLevel: person.risk_level || 'Low',
              riskScore: person.risk_score || 0,
              cases: person.case_count || 0,
              caseTypes: person.case_types || [],
              location: person.region || 'N/A'
            }));

            console.log('Transformed paginated results:', transformedResults.slice(0, 3));
            setFilteredResults(transformedResults);
            setTotalResults(data.total || 0);
            setTotalPages(data.total_pages || 0);
            console.log('Paginated people set successfully');
          } else {
            console.error('Paginated API response not ok:', response.status, response.statusText);
          }
        } catch (error) {
          console.error('Error loading people:', error);
        } finally {
          setIsLoading(false);
        }
      };
      loadAllPeople();
    }
  }, [searchQuery, currentPage, itemsPerPage]);

  // Group results alphabetically
  const groupResultsAlphabetically = (peopleList) => {
    // Sort alphabetically by name
    const sortedResults = [...peopleList].sort((a, b) => {
      const nameA = (a.name || '').toLowerCase();
      const nameB = (b.name || '').toLowerCase();
      return nameA.localeCompare(nameB);
    });

    // Group by first letter
    const grouped = {};
    sortedResults.forEach(person => {
      const firstLetter = (person.name || 'Unknown').charAt(0).toUpperCase();
      if (!grouped[firstLetter]) {
        grouped[firstLetter] = [];
      }
      grouped[firstLetter].push(person);
    });

    return grouped;
  };

  // Get alphabetically grouped results for the full dataset
  // For alphabet grouping, we need all people, not just the current page
  console.log('All people for grouping:', allPeople.length);
  const groupedResults = groupResultsAlphabetically(allPeople);
  console.log('Grouped results:', Object.keys(groupedResults).map(letter => `${letter}: ${groupedResults[letter]?.length || 0}`));
  
  // Create all alphabet sections A-Z
  const allAlphabetSections = Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i));
  
  // Filter results based on selected letter
  const filteredGroupedResults = selectedLetter 
    ? { [selectedLetter]: groupedResults[selectedLetter] || [] }
    : groupedResults;
  
  const alphabetSections = selectedLetter 
    ? [selectedLetter] 
    : allAlphabetSections.filter(letter => groupedResults[letter] && groupedResults[letter].length > 0);

  // Pagination - using server-side pagination for normal view, client-side for letter filtering
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = Math.min(startIndex + itemsPerPage, totalResults);
  const currentResults = selectedLetter 
    ? filteredResults.slice(startIndex, endIndex) // Client-side pagination for letter filtering
    : filteredResults; // Server-side pagination for normal view

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleLetterClick = (letter) => {
    if (selectedLetter === letter) {
      // If clicking the same letter, clear the filter
      setSelectedLetter(null);
    } else {
      // Filter to show only people with names starting with this letter
      setSelectedLetter(letter);
      
      // Filter allPeople to show only people starting with this letter
      const filteredByLetter = allPeople.filter(person => {
        const name = (person.name || '').toLowerCase();
        return name.startsWith(letter.toLowerCase());
      });
      
      setFilteredResults(filteredByLetter);
      setTotalResults(filteredByLetter.length);
      setTotalPages(Math.ceil(filteredByLetter.length / itemsPerPage));
    }
    setCurrentPage(1); // Reset to first page when filtering
  };

  const clearLetterFilter = async () => {
    setSelectedLetter(null);
    setCurrentPage(1);
    
    // Reload all people for the current page
    try {
      const token = localStorage.getItem('accessToken');
      
      const headers = {
        'Content-Type': 'application/json'
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      setIsLoading(true);
      const response = await fetch(`http://localhost:8000/api/people/search?page=1&limit=${itemsPerPage}`, {
        headers
      });

      if (response.ok) {
        const data = await response.json();
        const transformedResults = (data.people || []).map(person => ({
          id: person.id,
          name: person.full_name || `${person.first_name} ${person.last_name}`,
          idNumber: person.id_number || 'N/A',
          riskLevel: person.risk_level || 'Low',
          riskScore: person.risk_score || 0,
          cases: person.case_count || 0,
          caseTypes: person.case_types || [],
          location: person.region || 'N/A'
        }));

        setFilteredResults(transformedResults);
        setTotalResults(data.total || 0);
        setTotalPages(data.total_pages || 0);
      }
    } catch (error) {
      console.error('Error loading people:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Reset to first page when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [filterBy, sortBy, searchQuery]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setAdvancedFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAdvancedSearch = (e) => {
    e.preventDefault();
    // Convert advanced search to regular search
    const searchTerms = [];
    if (advancedFormData.firstName) searchTerms.push(advancedFormData.firstName);
    if (advancedFormData.lastName) searchTerms.push(advancedFormData.lastName);
    if (advancedFormData.idNumber) searchTerms.push(advancedFormData.idNumber);
    
    setSearchQuery(searchTerms.join(' '));
    setActiveTab('search');
  };

  const handleResetAdvanced = () => {
    setAdvancedFormData({
      firstName: '',
      lastName: '',
      dateOfBirth: '',
      idNumber: '',
      phone: '',
      email: '',
      address: '',
      caseType: '',
      court: '',
      caseStatus: '',
      dateRange: '',
      region: '',
      city: ''
    });
  };

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


  const handleSuggestionClick = (suggestion) => {
    setSearchQuery(suggestion);
    setShowSuggestions(false);
  };

  // Handle search function
  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    if (!searchQuery.trim()) return;

    try {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        console.error('No authentication token found');
        return;
      }

      setIsLoading(true);
      const response = await fetch(`http://localhost:8000/api/people/search?query=${encodeURIComponent(searchQuery)}&page=${currentPage}&limit=${itemsPerPage}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Search results:', data);
        
        const transformedResults = (data.people || []).map(person => ({
          id: person.id,
          name: person.full_name || `${person.first_name} ${person.last_name}`,
          idNumber: person.id_number || 'N/A',
          riskLevel: person.risk_level || 'Low',
          riskScore: person.risk_score || 0,
          cases: person.case_count || 0,
          caseTypes: person.case_types || [],
          location: person.region || 'N/A'
        }));

        setFilteredResults(transformedResults);
        setTotalResults(data.total || 0);
        setTotalPages(data.total_pages || 0);
      } else {
        console.error('Search failed:', response.status);
      }
    } catch (error) {
      console.error('Error searching people:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Check authentication status on component mount
  useEffect(() => {
    const authStatus = localStorage.getItem('isAuthenticated') === 'true';
    const token = localStorage.getItem('accessToken');
    
    setIsAuthenticated(authStatus && !!token);
    
    if (!authStatus || !token) {
      console.log('User not authenticated. Please login to use search functionality.');
    } else {
      console.log('User authenticated, search functionality available');
    }
  }, []);

  // Load all people when component mounts
  useEffect(() => {
    const loadAllPeople = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        if (!token) {
          console.error('No authentication token found');
          return;
        }

        setIsLoading(true);
        const response = await fetch(`http://localhost:8000/api/people/search?page=${currentPage}&limit=${itemsPerPage}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          console.log('All people loaded:', data);
          
          // Transform API data to match component format
          const transformedResults = (data.people || []).map(person => ({
            id: person.id,
            name: person.full_name || `${person.first_name} ${person.last_name}`,
            idNumber: person.id_number || 'N/A',
            riskLevel: person.risk_level || 'Low',
            riskScore: person.risk_score || 0,
            cases: person.case_count || 0,
            caseTypes: person.case_types || [],
            location: person.region || 'N/A'
          }));

          setFilteredResults(transformedResults);
          setTotalResults(data.total || 0);
          setTotalPages(data.total_pages || 0);
        } else {
          console.error('Failed to load people:', response.status);
        }
      } catch (error) {
        console.error('Error loading people:', error);
      } finally {
        setIsLoading(false);
      }
    };

    if (isAuthenticated) {
      loadAllPeople();
    }
  }, [isAuthenticated, currentPage, itemsPerPage]);

  // Debounced search suggestions
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchQuery.trim()) {
        loadSuggestions(searchQuery);
      } else {
        setSuggestions([]);
      }
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [searchQuery]);

  // Load search suggestions from API
  const loadSuggestions = async (query) => {
    if (query.length < 2) {
      setSuggestions([]);
      return;
    }

    setIsLoadingSuggestions(true);
    try {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        console.log('No authentication token found for suggestions');
        return;
      }

      console.log('Loading suggestions for query:', query);
      const response = await fetch(`http://localhost:8000/api/people/search?query=${encodeURIComponent(query)}&limit=5`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      console.log('Suggestions response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Suggestions data:', data);
        const suggestionNames = (data.people || []).map(person => person.full_name);
        setSuggestions(suggestionNames);
      } else {
        const errorText = await response.text();
        console.error('Suggestions API error:', response.status, errorText);
      }
    } catch (error) {
      console.error('Error loading suggestions:', error);
    } finally {
      setIsLoadingSuggestions(false);
    }
  };


  return (
    <AuthGuard>
      <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">People Database</h1>
          <p className="text-slate-600">Search, filter, and manage people in the legal database</p>
        </div>

        {/* Loading Progress Bar */}
        {isLoadingAllPeople && (
          <div className="mb-8 bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-slate-900">Loading People Database</h3>
              <span className="text-sm text-slate-600">{loadingProgress}%</span>
            </div>
            
            {/* Progress Bar */}
            <div className="w-full bg-slate-200 rounded-full h-3 mb-4">
              <div 
                className="bg-blue-600 h-3 rounded-full transition-all duration-300 ease-out"
                style={{ width: `${loadingProgress}%` }}
              ></div>
            </div>
            
            {/* Status Text */}
            <div className="flex items-center justify-between">
              <p className="text-sm text-slate-600">{loadingStatus}</p>
              <div className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                <span className="text-xs text-slate-500">Please wait...</span>
              </div>
            </div>
          </div>
        )}

        {/* Tab Navigation */}
        <div className="mb-8">
          <div className="border-b border-slate-200">
            <nav className="-mb-px flex space-x-8">
              {[
                { id: 'search', name: 'Quick Search', icon: Search },
                { id: 'advanced', name: 'Advanced Search', icon: Filter },
                { id: 'database', name: 'Database View', icon: User }
              ].map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-2 py-2 px-1 border-b-2 font-medium text-sm ${
                      activeTab === tab.id
                        ? 'border-sky-500 text-sky-600'
                        : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    {tab.name}
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Search Tab */}
        {activeTab === 'search' && (
          <div className="mb-8">
            {!isAuthenticated && (
              <div className="mb-4 bg-amber-50 border border-amber-200 rounded-lg p-4">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-amber-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-amber-800">
                      Authentication Required
                    </h3>
                    <div className="mt-2 text-sm text-amber-700">
                      <p>Please <a href="/login" className="font-medium underline text-amber-800 hover:text-amber-900">login</a> to use the search functionality.</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <form onSubmit={handleSearch} className="space-y-4">
              <div className="relative">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
                  <input
                    type="text"
                      placeholder={isAuthenticated ? "Search for people, banks, or insurance companies..." : "Please login to search..."}
                    value={searchQuery}
                    onChange={(e) => {
                      setSearchQuery(e.target.value);
                      setShowSuggestions(e.target.value.length > 0);
                    }}
                      disabled={!isAuthenticated}
                      className={`w-full pl-10 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 ${!isAuthenticated ? 'bg-slate-100 cursor-not-allowed' : ''}`}
                  />
                </div>
                
                {/* Search Suggestions */}
                {showSuggestions && searchQuery && (
                  <div className="absolute z-10 w-full mt-1 bg-white border border-slate-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                  {isLoadingSuggestions ? (
                    <div className="px-4 py-2 text-slate-500 text-sm">Loading suggestions...</div>
                  ) : suggestions.length > 0 ? (
                    suggestions.map((suggestion, index) => (
                        <button
                          key={index}
                        type="button"
                          onClick={() => handleSuggestionClick(suggestion)}
                          className="w-full px-4 py-2 text-left hover:bg-slate-50 focus:bg-slate-50 focus:outline-none"
                        >
                          {suggestion}
                        </button>
                    ))
                  ) : (
                    <div className="px-4 py-2 text-slate-500 text-sm">No suggestions found</div>
                  )}
                  </div>
                )}
              </div>
                <div className="flex justify-end">
                  <button
                    type="submit"
                    className="inline-flex items-center gap-2 px-6 py-2 bg-sky-600 text-white font-medium rounded-lg hover:bg-sky-700 transition-colors"
                  >
                    <Search className="h-4 w-4" />
                    Search
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Advanced Search Tab */}
        {activeTab === 'advanced' && (
          <div className="mb-8">
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Advanced Search</h3>
              <form onSubmit={handleAdvancedSearch} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">First Name</label>
                    <input
                      type="text"
                      name="firstName"
                      value={advancedFormData.firstName}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Last Name</label>
                    <input
                      type="text"
                      name="lastName"
                      value={advancedFormData.lastName}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">ID Number</label>
                    <input
                      type="text"
                      name="idNumber"
                      value={advancedFormData.idNumber}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Region</label>
                    <select
                      name="region"
                      value={advancedFormData.region}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
                    >
                      <option value="">All Regions</option>
                      <option value="Greater Accra">Greater Accra</option>
                      <option value="Ashanti">Ashanti</option>
                      <option value="Western">Western</option>
                      <option value="Central">Central</option>
                      <option value="Eastern">Eastern</option>
                      <option value="Volta">Volta</option>
                      <option value="Northern">Northern</option>
                      <option value="Upper East">Upper East</option>
                      <option value="Upper West">Upper West</option>
                      <option value="Brong-Ahafo">Brong-Ahafo</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Case Type</label>
                    <select
                      name="caseType"
                      value={advancedFormData.caseType}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
                    >
                      <option value="">All Case Types</option>
                      <option value="Criminal">Criminal</option>
                      <option value="Civil">Civil</option>
                      <option value="Family">Family</option>
                      <option value="Business">Business</option>
                      <option value="Property">Property</option>
                      <option value="Contract">Contract</option>
                    </select>
                  </div>
                </div>
                <div className="flex gap-3">
                  <button
                    type="submit"
                    className="flex items-center gap-2 px-4 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 focus:ring-2 focus:ring-sky-500 focus:ring-offset-2"
                  >
                    <Search className="h-4 w-4" />
                    Search
                  </button>
                  <button
                    type="button"
                    onClick={handleResetAdvanced}
                    className="flex items-center gap-2 px-4 py-2 bg-slate-600 text-white rounded-lg hover:bg-slate-700 focus:ring-2 focus:ring-slate-500 focus:ring-offset-2"
                  >
                    <RotateCcw className="h-4 w-4" />
                    Reset
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Database Tab */}
        {activeTab === 'database' && (
          <div className="mb-8">
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-900">Database Overview</h3>
                <div className="flex items-center gap-3">
                  <button className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2">
                    <Plus className="h-4 w-4" />
                    Add Person
                  </button>
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-slate-50 rounded-lg p-4">
                  <div className="text-2xl font-bold text-slate-900">{totalResults}</div>
                  <div className="text-sm text-slate-600">Total People</div>
                </div>
                <div className="bg-emerald-50 rounded-lg p-4">
                  <div className="text-2xl font-bold text-emerald-600">
                    {filteredResults.filter(p => p.riskLevel === 'Low').length}
                  </div>
                  <div className="text-sm text-slate-600">Low Risk</div>
                </div>
                <div className="bg-amber-50 rounded-lg p-4">
                  <div className="text-2xl font-bold text-amber-600">
                    {filteredResults.filter(p => p.riskLevel === 'Medium').length}
                  </div>
                  <div className="text-sm text-slate-600">Medium Risk</div>
                </div>
                <div className="bg-red-50 rounded-lg p-4">
                  <div className="text-2xl font-bold text-red-600">
                    {filteredResults.filter(p => p.riskLevel === 'High').length}
                  </div>
                  <div className="text-sm text-slate-600">High Risk</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Results Section */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200">
          {/* Results Header */}
          <div className="px-6 py-4 border-b border-slate-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <h2 className="text-lg font-semibold text-slate-900">
                  {activeTab === 'search' ? 'Search Results' : 
                   activeTab === 'advanced' ? 'Advanced Search Results' : 
                   'People Database'}
                </h2>
                <span className="text-sm text-slate-500">
                  {filteredResults.length} {filteredResults.length === 1 ? 'person' : 'people'} found
                </span>
              </div>
              
              <div className="flex items-center gap-3">
                {/* View Toggle */}
                <div className="flex items-center bg-slate-100 rounded-lg p-1">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`p-2 rounded-md transition-colors ${
                      viewMode === 'grid' ? 'bg-white shadow-sm' : 'hover:bg-slate-200'
                    }`}
                  >
                    <Grid className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`p-2 rounded-md transition-colors ${
                      viewMode === 'list' ? 'bg-white shadow-sm' : 'hover:bg-slate-200'
                    }`}
                  >
                    <List className="h-4 w-4" />
                  </button>
                </div>

                {/* Filter Toggle */}
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="flex items-center gap-2 px-3 py-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors"
                >
                  <Filter className="h-4 w-4" />
                  Filter
                  {showFilters ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                </button>

              </div>
            </div>

            {/* Filters */}
            {showFilters && (
              <div className="mt-4 pt-4 border-t border-slate-200">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Sort By</label>
                    <select
                      value={sortBy}
                      onChange={(e) => setSortBy(e.target.value)}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
                    >
                      <option value="name">Name</option>
                      <option value="risk">Risk Level</option>
                      <option value="cases">Case Count</option>
                      <option value="location">Location</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Risk Level</label>
                    <select
                      value={filterBy.riskLevel}
                      onChange={(e) => setFilterBy(prev => ({ ...prev, riskLevel: e.target.value }))}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
                    >
                      <option value="all">All Risk Levels</option>
                      <option value="Low">Low Risk</option>
                      <option value="Medium">Medium Risk</option>
                      <option value="High">High Risk</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Location</label>
                    <select
                      value={filterBy.location}
                      onChange={(e) => setFilterBy(prev => ({ ...prev, location: e.target.value }))}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
                    >
                      <option value="all">All Locations</option>
                      <option value="Greater Accra">Greater Accra</option>
                      <option value="Ashanti">Ashanti</option>
                      <option value="Western">Western</option>
                      <option value="Central">Central</option>
                      <option value="Eastern">Eastern</option>
                      <option value="Volta">Volta</option>
                      <option value="Northern">Northern</option>
                      <option value="Upper East">Upper East</option>
                      <option value="Upper West">Upper West</option>
                      <option value="Brong-Ahafo">Brong-Ahafo</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Case Count</label>
                    <select
                      value={filterBy.caseCount}
                      onChange={(e) => setFilterBy(prev => ({ ...prev, caseCount: e.target.value }))}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
                    >
                      <option value="all">All Cases</option>
                      <option value="0-2">0-2 Cases</option>
                      <option value="3-5">3-5 Cases</option>
                      <option value="6-10">6-10 Cases</option>
                      <option value="11">11+ Cases</option>
                    </select>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Alphabet Navigation */}
          {!isLoading && (
            <div className="px-6 py-4 bg-slate-50 border-b border-slate-200">
              <div className="flex flex-wrap gap-2 justify-center">
                {allAlphabetSections.map((letter) => {
                  const hasPeople = groupedResults[letter] && groupedResults[letter].length > 0;
                  const isSelected = selectedLetter === letter;
                  
                  return (
                    <button
                      key={letter}
                      onClick={() => handleLetterClick(letter)}
                      className={`px-3 py-2 text-sm font-medium rounded-lg transition-colors border ${
                        isSelected
                          ? 'bg-blue-600 text-white border-blue-600'
                          : hasPeople
                          ? 'text-slate-600 hover:text-blue-600 hover:bg-blue-50 border-slate-200 hover:border-blue-300'
                          : 'text-slate-500 hover:text-slate-700 hover:bg-slate-100 border-slate-200 hover:border-slate-300'
                      }`}
                    >
                      {letter}
                      {hasPeople && (
                        <span className="ml-1 text-xs">
                          ({groupedResults[letter].length})
                        </span>
                      )}
                    </button>
                  );
                })}
                
                {selectedLetter && (
                  <button
                    onClick={clearLetterFilter}
                    className="px-3 py-2 text-sm font-medium text-slate-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors border border-slate-200 hover:border-red-300"
                  >
                    Clear Filter
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Filter Indicator */}
          {selectedLetter && (
            <div className="px-6 py-3 bg-blue-50 border-b border-blue-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-sm text-blue-800">
                    Showing people whose names start with "{selectedLetter}"
                  </span>
                  <span className="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded-full">
                    {filteredGroupedResults[selectedLetter]?.length || 0} people
                  </span>
                </div>
                <button
                  onClick={clearLetterFilter}
                  className="text-sm text-blue-600 hover:text-blue-800 underline"
                >
                  Show all people
                </button>
              </div>
            </div>
          )}

          {/* Results Grid/List */}
          <div className="p-6">
            {filteredResults.length === 0 && !selectedLetter ? (
              <div className="text-center py-12">
                <User className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-slate-900 mb-2">No people found</h3>
                <p className="text-slate-500">Try adjusting your search criteria or filters</p>
              </div>
            ) : selectedLetter ? (
              // Show filtered results for selected letter
              <div className="space-y-8">
                <div id={`section-${selectedLetter}`} className="space-y-4">
                  {/* Section Header */}
                  <div className="sticky top-0 bg-slate-50 border-b border-slate-200 py-3 px-4 rounded-t-lg">
                    <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-3">
                      <span className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                        {selectedLetter}
                      </span>
                      {selectedLetter}
                      <span className="text-sm font-normal text-slate-500">
                        ({currentResults.length} {currentResults.length === 1 ? 'person' : 'people'})
                      </span>
                    </h2>
                  </div>
                  
                  {/* People in this section */}
                  {currentResults.length > 0 ? (
              <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' : 'space-y-4'}>
                {currentResults.map((person) => (
                  <div
                    key={person.id}
                    className={`bg-white border border-slate-200 rounded-lg hover:shadow-md transition-shadow cursor-pointer ${
                      viewMode === 'list' ? 'flex items-center p-4' : 'p-6'
                    }`}
                    onClick={() => navigate(`/person-profile/${person.id}?source=search`)}
                  >
                    {viewMode === 'grid' ? (
                      <>
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center gap-3">
                            <div className="h-12 w-12 bg-slate-100 rounded-full flex items-center justify-center">
                              <User className="h-6 w-6 text-slate-600" />
                            </div>
                            <div>
                              <h3 className="font-semibold text-slate-900">{person.name}</h3>
                            </div>
                          </div>
                                <div className="text-right">
                                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                    person.riskLevel === 'High' ? 'bg-red-100 text-red-800' :
                                    person.riskLevel === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                                    'bg-green-100 text-green-800'
                                  }`}>
                            {person.riskLevel} Risk
                          </span>
                        </div>
                              </div>
                              
                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                                  <span className="text-slate-500">Cases:</span>
                                  <span className="font-medium">{person.cases}</span>
                          </div>
                                <div className="flex justify-between text-sm">
                                  <span className="text-slate-500">Location:</span>
                                  <span className="font-medium">{person.location}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                  <span className="text-slate-500">Risk Score:</span>
                                  <span className="font-medium">{person.riskScore}</span>
                                </div>
                              </div>
                            </>
                          ) : (
                            <>
                              <div className="flex items-center gap-4">
                                <div className="h-10 w-10 bg-slate-100 rounded-full flex items-center justify-center">
                                  <User className="h-5 w-5 text-slate-600" />
                                </div>
                                <div className="flex-1">
                                  <h3 className="font-semibold text-slate-900">{person.name}</h3>
                                  <p className="text-sm text-slate-500">{person.location}</p>
                                </div>
                                <div className="flex items-center gap-4 text-sm">
                                  <span className="text-slate-500">{person.cases} cases</span>
                                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                    person.riskLevel === 'High' ? 'bg-red-100 text-red-800' :
                                    person.riskLevel === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                                    'bg-green-100 text-green-800'
                                  }`}>
                                    {person.riskLevel} Risk
                                  </span>
                                </div>
                              </div>
                            </>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-slate-500">
                      <p>No people found starting with "{selectedLetter}"</p>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              // Show all people grouped by alphabet
              <div className="space-y-8">
                {alphabetSections.map((letter) => {
                  const peopleInSection = filteredGroupedResults[letter] || [];
                  
                  return (
                    <div key={letter} id={`section-${letter}`} className="space-y-4">
                      {/* Section Header */}
                      <div className="sticky top-0 bg-slate-50 border-b border-slate-200 py-3 px-4 rounded-t-lg">
                        <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-3">
                          <span className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                            {letter}
                          </span>
                          {letter}
                          <span className="text-sm font-normal text-slate-500">
                            ({peopleInSection.length} {peopleInSection.length === 1 ? 'person' : 'people'})
                          </span>
                        </h2>
                      </div>
                      
                      {/* People in this section */}
                      {peopleInSection.length > 0 ? (
                        <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' : 'space-y-4'}>
                          {peopleInSection.map((person) => (
                  <div
                    key={person.id}
                    className={`bg-white border border-slate-200 rounded-lg hover:shadow-md transition-shadow cursor-pointer ${
                      viewMode === 'list' ? 'flex items-center p-4' : 'p-6'
                    }`}
                    onClick={() => navigate(`/person-profile/${person.id}?source=search`)}
                  >
                    {viewMode === 'grid' ? (
                      <>
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center gap-3">
                            <div className="h-12 w-12 bg-slate-100 rounded-full flex items-center justify-center">
                              <User className="h-6 w-6 text-slate-600" />
                            </div>
                            <div>
                              <h3 className="font-semibold text-slate-900">{person.name}</h3>
                              <p className="text-sm text-slate-500">ID: {person.idNumber}</p>
                            </div>
                          </div>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ring-1 ${getRiskColor(person.riskLevel)}`}>
                            {person.riskLevel} Risk
                          </span>
                        </div>
                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span className="text-slate-500">Cases:</span>
                            <span className="text-slate-900">{person.cases}</span>
                          </div>
                          <div className="flex justify-between text-sm">
                            <span className="text-slate-500">Location:</span>
                            <span className="text-slate-900">{person.location}</span>
                          </div>
                          <div className="flex justify-between text-sm">
                            <span className="text-slate-500">Last Updated:</span>
                            <span className="text-slate-900">{person.lastUpdated}</span>
                          </div>
                        </div>
                      </>
                    ) : (
                      <>
                        <div className="h-12 w-12 bg-slate-100 rounded-full flex items-center justify-center mr-4">
                          <User className="h-6 w-6 text-slate-600" />
                        </div>
                        <div className="flex-1 grid grid-cols-1 md:grid-cols-5 gap-4">
                          <div>
                            <h3 className="font-semibold text-slate-900">{person.name}</h3>
                            <p className="text-sm text-slate-500">ID: {person.idNumber}</p>
                          </div>
                          <div>
                            <p className="text-sm text-slate-500">Cases</p>
                            <p className="text-slate-900">{person.cases}</p>
                          </div>
                          <div>
                            <p className="text-sm text-slate-500">Location</p>
                            <p className="text-slate-900">{person.location}</p>
                          </div>
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-sm text-slate-500">Risk Level</p>
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ring-1 ${getRiskColor(person.riskLevel)}`}>
                                {person.riskLevel}
                              </span>
                            </div>
                            <p className="text-sm text-slate-500">{person.lastUpdated}</p>
                          </div>
                        </div>
                      </>
                    )}
                  </div>
                ))}
                        </div>
                      ) : (
                        <div className="text-center py-8 text-slate-500">
                          <p>No people found starting with "{letter}"</p>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-8">
                <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="text-sm text-slate-500">
                    Showing {startIndex + 1} to {endIndex} of {totalResults} results
                </div>
                  
                  <div className="flex items-center gap-1 overflow-x-auto max-w-full">
                  <button
                    onClick={() => handlePageChange(currentPage - 1)}
                    disabled={currentPage === 1}
                      className="flex items-center gap-1 px-3 py-2 text-sm text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
                  >
                    <ChevronLeft className="h-4 w-4" />
                      <span className="hidden sm:inline">Previous</span>
                  </button>
                  
                    <div className="flex items-center gap-1 min-w-0">
                      {/* Show first page */}
                      {currentPage > 3 && (
                        <>
                          <button
                            onClick={() => handlePageChange(1)}
                            className="px-3 py-2 text-sm text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg"
                          >
                            1
                          </button>
                          {currentPage > 4 && <span className="px-2 text-slate-400">...</span>}
                        </>
                      )}
                      
                      {/* Show pages around current page */}
                      {Array.from({ length: totalPages }, (_, i) => i + 1)
                        .filter(page => {
                          return page >= Math.max(1, currentPage - 2) && 
                                 page <= Math.min(totalPages, currentPage + 2);
                        })
                        .map((page) => (
                      <button
                        key={page}
                        onClick={() => handlePageChange(page)}
                            className={`px-3 py-2 text-sm rounded-lg whitespace-nowrap ${
                          page === currentPage
                            ? 'bg-sky-600 text-white'
                            : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                        }`}
                      >
                        {page}
                      </button>
                    ))}
                      
                      {/* Show last page */}
                      {currentPage < totalPages - 2 && (
                        <>
                          {currentPage < totalPages - 3 && <span className="px-2 text-slate-400">...</span>}
                          <button
                            onClick={() => handlePageChange(totalPages)}
                            className="px-3 py-2 text-sm text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg"
                          >
                            {totalPages}
                          </button>
                        </>
                      )}
                  </div>
                  
                  <button
                    onClick={() => handlePageChange(currentPage + 1)}
                    disabled={currentPage === totalPages}
                      className="flex items-center gap-1 px-3 py-2 text-sm text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
                  >
                      <span className="hidden sm:inline">Next</span>
                    <ChevronRight className="h-4 w-4" />
                  </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
      </div>
    </AuthGuard>
  );
};

export default People;
