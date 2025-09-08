import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Star, Shield, Clock, Users, Database } from 'lucide-react';

const Home = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const searchRef = useRef(null);
  const navigate = useNavigate();

  // Mock suggestions data
  const mockSuggestions = [
    'Albert Kweku Obeng',
    'Sarah Mensah',
    'Kwame Asante',
    'Ama Serwaa',
    'John Smith',
    'Mary Johnson',
    'David Brown',
    'Ghana Commercial Bank',
    'Ecobank Ghana',
    'SIC Insurance Company',
    'Enterprise Insurance',
    'Accra High Court',
    'Kumasi Circuit Court',
    'Property Dispute',
    'Business Law',
    'Criminal Case',
    'Family Law',
    'Contract Dispute'
  ];

  // Handle search input changes
  const handleInputChange = (e) => {
    const value = e.target.value;
    setSearchQuery(value);
    
    if (value.length > 0) {
      const filteredSuggestions = mockSuggestions.filter(suggestion =>
        suggestion.toLowerCase().includes(value.toLowerCase())
      );
      setSuggestions(filteredSuggestions.slice(0, 8)); // Limit to 8 suggestions
      setShowSuggestions(true);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  };

  // Handle suggestion selection
  const handleSuggestionClick = (suggestion) => {
    setSearchQuery(suggestion);
    setShowSuggestions(false);
    navigate(`/people-results?search=${encodeURIComponent(suggestion)}`);
  };

  // Handle search form submission
  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setShowSuggestions(false);
      navigate(`/people-results?search=${encodeURIComponent(searchQuery)}`);
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
      title: "Comprehensive Search",
      description: "Search by name, ID number, phone, address, or any combination of criteria for accurate results."
    },
    {
      icon: <Shield className="h-6 w-6 text-sky-600" />,
      title: "Risk Assessment",
      description: "Get instant risk scores and assessments based on legal history and case outcomes."
    },
    {
      icon: <Clock className="h-6 w-6 text-sky-600" />,
      title: "Real-time Updates",
      description: "Our database is updated daily with the latest legal cases and information from courts nationwide."
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
    <div>
      {/* Hero Section */}
      <section className="bg-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-slate-900 mb-6">
              Look Up Anyone!
            </h1>
            <p className="text-xl text-slate-600 mb-8 max-w-3xl mx-auto">
              Search our comprehensive database of people and legal cases. Get instant access to legal history, risk assessments, and detailed profiles.
            </p>
            
            {/* Search Form */}
            <div className="max-w-2xl mx-auto mb-12">
              <div className="relative" ref={searchRef}>
                <form onSubmit={handleSearch} className="flex gap-2">
                  <div className="flex-1 relative">
                    <input
                      type="text"
                      placeholder="Enter name, ID number, or address..."
                      value={searchQuery}
                      onChange={handleInputChange}
                      onFocus={() => searchQuery.length > 0 && setShowSuggestions(true)}
                      className="w-full rounded-lg border border-slate-300 px-4 py-3 text-sm focus:border-sky-500 focus:ring-1 focus:ring-sky-500"
                    />
                    
                    {/* Suggestions Dropdown */}
                    {showSuggestions && suggestions.length > 0 && (
                      <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-200 rounded-lg shadow-lg z-50 max-h-60 overflow-y-auto">
                        {suggestions.map((suggestion, index) => (
                          <button
                            key={index}
                            type="button"
                            onClick={() => handleSuggestionClick(suggestion)}
                            className="w-full text-left px-4 py-3 text-sm text-slate-700 hover:bg-slate-50 border-b border-slate-100 last:border-b-0 transition-colors"
                          >
                            <div className="flex items-center gap-2">
                              <Search className="h-4 w-4 text-slate-400" />
                              <span>{suggestion}</span>
                            </div>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                  <button
                    type="submit"
                    className="rounded-lg bg-sky-600 px-6 py-3 text-sm font-medium text-white hover:bg-sky-700 transition-colors"
                  >
                    Search
                  </button>
                </form>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3 max-w-2xl mx-auto">
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
      </section>

      {/* Features Section */}
      <section className="bg-slate-50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-slate-900">Why Choose Dennislaw SVD?</h2>
            <p className="mt-2 text-slate-600">Advanced features designed for legal professionals and researchers</p>
          </div>
          
          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, index) => (
              <div key={index} className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
                <div className="h-12 w-12 rounded-lg bg-sky-100 flex items-center justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-2">{feature.title}</h3>
                <p className="text-slate-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-sky-600">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white mb-4">Ready to Get Started?</h2>
            <p className="text-xl text-sky-100 mb-8">Join thousands of legal professionals who trust Dennislaw SVD for their research needs.</p>
            <div className="flex gap-4 justify-center">
              <button
                onClick={() => navigate('/people-results')}
                className="inline-flex items-center gap-2 rounded-lg bg-white px-6 py-3 text-sm font-medium text-sky-600 hover:bg-slate-50 transition-colors"
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
