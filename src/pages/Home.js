import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Shield, Clock, Users, Database, Building2, Banknote, Building, User } from 'lucide-react';

const Home = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [isLoadingSuggestions, setIsLoadingSuggestions] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const searchRef = useRef(null);
  const navigate = useNavigate();

  // Check authentication status on component mount
  useEffect(() => {
    const authStatus = localStorage.getItem('isAuthenticated') === 'true';
    const token = localStorage.getItem('accessToken');
    setIsAuthenticated(authStatus && !!token);
  }, []);

  // Load search suggestions from API - All entity types (people, banks, insurance, companies)
  const loadSuggestions = async (query) => {
    console.log('loadSuggestions called with query:', query);
    if (query.length < 1) {
      console.log('Query too short, clearing suggestions');
      setSuggestions([]);
      return;
    }

    console.log('Starting to load suggestions...');
    setIsLoadingSuggestions(true);
    try {
      // Use unified search endpoint for all entity types
      const url = `http://localhost:8000/api/search/quick?query=${encodeURIComponent(query)}&limit=10`;
      console.log('Making request to:', url);
      
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      console.log('Response status:', response.status);
      console.log('Response ok:', response.ok);

      let allSuggestions = [];
      
      if (response.ok) {
        const data = await response.json();
        console.log('Unified search data received:', data);
        const unifiedSuggestions = (data.suggestions || []).map(item => ({
          name: item.name,
          text: item.name,
          type: item.type,
          entity_type: item.type,
          description: item.description,
          id: item.id,
          city: item.city,
          region: item.region,
          logo_url: item.logo_url
        }));
        allSuggestions = [...unifiedSuggestions];
        console.log('Mapped suggestions:', allSuggestions);
      } else {
        console.error('API response not ok:', response.status, response.statusText);
      }
      
      setSuggestions(allSuggestions);
    } catch (error) {
      console.error('Error loading suggestions:', error);
      setSuggestions([]);
    } finally {
      setIsLoadingSuggestions(false);
    }
  };

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
  }, [searchQuery]); // eslint-disable-line react-hooks/exhaustive-deps

  // Handle search input changes
  const handleInputChange = (e) => {
    const value = e.target.value;
    setSearchQuery(value);
    setShowSuggestions(value.length > 0);
  };

  // Handle suggestion selection - All entity types
  const handleSuggestionClick = (suggestion) => {
    setSearchQuery(suggestion.text || suggestion.name || suggestion);
    setShowSuggestions(false);
    
    // Route to appropriate entity type based on suggestion type
    const entityType = suggestion.entity_type || suggestion.type;
    switch (entityType) {
      case 'people':
        navigate(`/people-results?search=${encodeURIComponent(suggestion.name)}`);
        break;
      case 'banks':
        navigate(`/bank-detail/${suggestion.id}`);
        break;
      case 'insurance':
        navigate(`/insurance-profile/${suggestion.id}`);
        break;
      case 'companies':
        navigate(`/company-profile/${suggestion.id}`);
        break;
      default:
        // Default to people results for backward compatibility
        navigate(`/people-results?search=${encodeURIComponent(suggestion.name)}`);
    }
  };


  // Handle search form submission
  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setShowSuggestions(false);
      
      if (!isAuthenticated) {
        // Redirect to login if not authenticated
        navigate('/login');
        return;
      }
      
      // Navigate to unified search results to show all entity types
      navigate(`/search-results?search=${encodeURIComponent(searchQuery)}`);
    }
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

  const features = [
    {
      icon: <Search className="h-6 w-6 text-sky-600" />,
      title: "People Name Search",
      description: "Search people by name with detailed profiles and comprehensive information from our legal database."
    },
    {
      icon: <Shield className="h-6 w-6 text-sky-600" />,
      title: "Legal History",
      description: "Get instant access to legal history and case information for any person in our database."
    },
    {
      icon: <Clock className="h-6 w-6 text-sky-600" />,
      title: "Real-time Updates",
      description: "Our database is updated daily with the latest information on people and their legal records."
    },
    {
      icon: <Shield className="h-6 w-6 text-sky-600" />,
      title: "Secure & Private",
      description: "Your searches are secure and private. We use industry-standard encryption to protect your data."
    },
    {
      icon: <Users className="h-6 w-6 text-sky-600" />,
      title: "Easy to Use",
      description: "Intuitive interface designed for both legal professionals and general users."
    },
    {
      icon: <Database className="h-6 w-6 text-sky-600" />,
      title: "24/7 Access",
      description: "Access our database anytime, anywhere with our reliable and fast platform."
    }
  ];

  return (
    <div className="bg-white dark:bg-slate-900 transition-colors duration-200">
      {/* Hero Section */}
      <section className="bg-white dark:bg-slate-900">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            {/* Logo Section */}
            <div className="flex justify-center mb-8">
              <div className="flex items-center gap-4">
                <img 
                  src="/logo.jpeg" 
                  alt="juridence logo" 
                  className="h-16 w-16 rounded-xl object-cover shadow-xl"
                />
                <div className="text-left">
          <h1 className="text-4xl font-bold text-slate-900 dark:text-white">juridence</h1>
          <p className="text-lg text-slate-600 dark:text-slate-400">Revolutionizing KYC with Legal Analytics</p>
                </div>
              </div>
            </div>
            
            <h2 className="text-3xl md:text-5xl font-bold text-slate-900 dark:text-white mb-6">
              Advanced KYC & Due Diligence Solutions
            </h2>
            
            <p className="text-xl text-slate-600 dark:text-slate-300 mb-8 max-w-3xl mx-auto">
              Empowering businesses with innovative legal analytics for comprehensive risk mitigation, compliance, and informed decision-making across Ghana's legal landscape.
            </p>
            
            {/* Authentication Notice */}
            {!isAuthenticated && (
              <div className="mb-6 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4 max-w-2xl mx-auto">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-amber-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-amber-800 dark:text-amber-200">
                      Authentication Required
                    </h3>
                    <div className="mt-2 text-sm text-amber-700 dark:text-amber-300">
                      <p>Please <a href="/login" className="font-medium underline text-amber-800 dark:text-amber-200 hover:text-amber-900 dark:hover:text-amber-100">login</a> to use the search functionality.</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Search Form */}
            <div className="max-w-2xl mx-auto mb-12">
              <div className="relative" ref={searchRef}>
                <form onSubmit={handleSearch} className="flex gap-2">
                  <div className="flex-1 relative">
                    <input
                      type="text"
                      placeholder={isAuthenticated ? "Search for people, banks, insurance, companies..." : "Please login to search..."}
                      value={searchQuery}
                      onChange={handleInputChange}
                      onFocus={() => searchQuery.length > 0 && setShowSuggestions(true)}
                      disabled={!isAuthenticated}
                      className={`w-full rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white px-4 py-3 text-sm focus:border-sky-500 focus:ring-1 focus:ring-sky-500 ${!isAuthenticated ? 'bg-slate-100 dark:bg-slate-700 cursor-not-allowed' : ''}`}
                    />
                    
                    {/* Suggestions Dropdown */}
                    {showSuggestions && (
                      <div className="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-600 rounded-lg shadow-lg z-50 max-h-60 overflow-y-auto">
                        {isLoadingSuggestions ? (
                          <div className="px-4 py-3 text-sm text-slate-500 dark:text-slate-400 text-center">
                            Loading suggestions...
                          </div>
                        ) : suggestions.length > 0 ? (
                          suggestions.map((suggestion, index) => {
                            // Get appropriate icon based on entity type
                            const getEntityIcon = (type) => {
                              switch (type) {
                                case 'people':
                                  return <User className="h-4 w-4 text-blue-500" />;
                                case 'banks':
                                  return <Building2 className="h-4 w-4 text-green-500" />;
                                case 'insurance':
                                  return <Shield className="h-4 w-4 text-purple-500" />;
                                case 'companies':
                                  return <Building className="h-4 w-4 text-orange-500" />;
                                default:
                                  return <Users className="h-4 w-4 text-gray-500" />;
                              }
                            };

                            return (
                              <button
                                key={index}
                                type="button"
                                onClick={() => handleSuggestionClick(suggestion)}
                                className="w-full text-left px-4 py-3 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 border-b border-slate-100 dark:border-slate-600 last:border-b-0 transition-colors"
                              >
                                <div className="flex items-center gap-3">
                                  {getEntityIcon(suggestion.entity_type || suggestion.type)}
                                  <div className="flex-1">
                                    <div className="font-medium">{suggestion.text || suggestion.name}</div>
                                    {suggestion.description && (
                                      <div className="text-xs text-slate-500 dark:text-slate-400">{suggestion.description}</div>
                                    )}
                                    {(suggestion.city || suggestion.region) && (
                                      <div className="text-xs text-slate-500 dark:text-slate-400">
                                        {suggestion.city && suggestion.region ? `${suggestion.city}, ${suggestion.region}` : suggestion.city || suggestion.region}
                                      </div>
                                    )}
                                  </div>
                                </div>
                              </button>
                            );
                          })
                        ) : searchQuery.length > 1 ? (
                          <div className="px-4 py-3 text-sm text-slate-500 dark:text-slate-400 text-center">
                            No suggestions found
                          </div>
                        ) : null}
                      </div>
                    )}
                  </div>
        <button
          type="submit"
          className="rounded-lg bg-brand-500 px-6 py-3 text-sm font-medium text-white hover:bg-brand-600 transition-colors"
        >
                    Search
                  </button>
                </form>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3 max-w-2xl mx-auto">
              <div className="text-center">
                <div className="text-2xl font-bold text-slate-900 dark:text-white">464</div>
                <div className="text-sm text-slate-600 dark:text-slate-400">Courts Connected</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-slate-900 dark:text-white">16</div>
                <div className="text-sm text-slate-600 dark:text-slate-400">Regions Covered</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-slate-900 dark:text-white">Daily</div>
                <div className="text-sm text-slate-600 dark:text-slate-400">Updated</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-slate-50 dark:bg-slate-800">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white">Why Choose juridence?</h2>
            <p className="mt-2 text-slate-600 dark:text-slate-300">Innovative KYC solutions designed for comprehensive due diligence and regulatory compliance</p>
          </div>
          
          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, index) => (
              <div key={index} className="bg-white dark:bg-slate-700 rounded-xl p-6 shadow-sm border border-slate-200 dark:border-slate-600 transition-colors duration-200">
                <div className="h-12 w-12 rounded-lg bg-sky-100 dark:bg-sky-900/30 flex items-center justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-2">{feature.title}</h3>
                <p className="text-slate-600 dark:text-slate-300">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-brand-500">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white mb-4">Ready to Get Started?</h2>
            <p className="text-xl text-white/90 mb-8">Join thousands of legal professionals who trust juridence for their research needs.</p>
            <div className="flex gap-4 justify-center">
              <button
                onClick={() => navigate('/results')}
                className="inline-flex items-center gap-2 rounded-lg bg-white px-6 py-3 text-sm font-medium text-brand-500 hover:bg-slate-50 transition-colors"
              >
                Start Searching
              </button>
              <button
                onClick={() => navigate('/about')}
                className="inline-flex items-center gap-2 rounded-lg border border-white px-6 py-3 text-sm font-medium text-white hover:bg-white/10 transition-colors"
              >
                Learn More
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
