import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Star, User, Calendar, Mail, Building2, Phone, Shield, Clock, Users, GraduationCap, Heart, AlertCircle, CheckCircle, XCircle, Eye, EyeOff, Search, Filter, ArrowUpDown, Scale, RefreshCw, ChevronLeft, ChevronRight, DollarSign, Percent, BookOpen, Calculator, AlertTriangle, History, Download, MapPin, Globe } from 'lucide-react';

const BankDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [bankData, setBankData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [analyticsLoading, setAnalyticsLoading] = useState(true);
  const [caseStats, setCaseStats] = useState(null);
  const [caseStatsLoading, setCaseStatsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('manager');
  const [managementData, setManagementData] = useState([]);
  const [relatedCases, setRelatedCases] = useState([]);
  const [casesLoading, setCasesLoading] = useState(false);
  const [filteredCases, setFilteredCases] = useState([]);
  const [caseSearchQuery, setCaseSearchQuery] = useState('');
  const [caseSortBy, setCaseSortBy] = useState('date');
  const [caseSortOrder, setCaseSortOrder] = useState('desc');
  const [currentPage, setCurrentPage] = useState(1);
  const [casesPerPage] = useState(10);

  // Bank logo mapping
  const bankLogoMap = {
    'Ghana Commercial Bank': '/banks/gcb bank.jpeg',
    'GCB Bank': '/banks/gcb bank.jpeg',
    'Ecobank Ghana': '/banks/ecobank.jpeg',
    'Ecobank': '/banks/ecobank.jpeg',
    'Standard Chartered Bank': '/banks/stanchart.jpeg',
    'Stanbic Bank': '/banks/stanbic bank.jpeg',
    'Absa Bank': '/banks/absa.jpeg',
    'Access Bank': '/banks/access bank.jpeg',
    'Agricultural Development Bank': '/banks/adb.jpeg',
    'Bank of Africa': '/banks/bank of africa.jpeg',
    'Bank of Ghana': '/banks/Bank of ghana.jpeg',
    'CAL Bank': '/banks/calbank.jpeg',
    'Consolidated Bank Ghana': '/banks/cbg.jpeg',
    'First Bank of Nigeria': '/banks/fbn.jpeg',
    'Fidelity Bank': '/banks/Fidelity.jpeg',
    'First Atlantic Bank': '/banks/first atlantic.jpeg',
    'Ghana EXIM Bank': '/banks/ghana exim bank.jpeg',
    'Guaranty Trust Bank': '/banks/gtbank.jpeg',
    'National Investment Bank': '/banks/national invenstment bank.jpeg',
    'NIB Bank': '/banks/nib.jpeg',
    'Omnibsic Bank': '/banks/omnibsic.jpeg',
    'Prudential Bank': '/banks/prudential bank.jpeg',
    'Republic Bank': '/banks/republic bank.jpeg',
    'Societe Generale': '/banks/societe generale bank.jpeg',
    'The Royal Bank': '/banks/the royal bank.jpeg',
    'UMB Bank': '/banks/umb.jpeg',
    'Universal Merchant Bank': '/banks/universal merchant bank.jpeg',
    'Zenith Bank': '/banks/zenith.jpeg',
  };

  // Load bank data
  useEffect(() => {
    console.log('URL Parameters - Bank ID:', id);
    
    if (id) {
      loadBankData(id);
      loadManagementData(id);
      loadRelatedCases(id);
      loadBankAnalytics(id);
      loadBankCaseStats(id);
    }
  }, [id]);

  const loadBankData = async (bankId) => {
    try {
      setIsLoading(true);
      setError(null);
      
      console.log('loadBankData called with:', { bankId });

      const url = `http://localhost:8000/api/banks/${bankId}`;
      console.log('Using bank ID URL:', url);
      
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      console.log('Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Bank data from ID:', data);

        if (data) {
          console.log('Raw bank data received:', data);
          // Transform API data to match expected format
          const transformedData = {
            id: data.id,
            name: data.name,
            shortName: data.short_name || data.name,
            logo: data.logo_url || bankLogoMap[data.name] || '/banks/default-bank.jpeg',
            established: data.established_date ? new Date(data.established_date).getFullYear().toString() : 'N/A',
            incorporated: data.established_date ? new Date(data.established_date).toLocaleDateString('en-US', { 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            }) : 'N/A',
            headquarters: `${data.city || 'N/A'}, ${data.region || 'N/A'}`,
            address: data.address || data.head_office_address || 'N/A',
            city: data.city || 'N/A',
            region: data.region || 'N/A',
            country: data.country || 'Ghana',
            postalCode: data.postal_code || 'N/A',
            phone: data.phone || 'N/A',
            customerServicePhone: data.customer_service_phone || 'N/A',
            email: data.email || 'N/A',
            customerServiceEmail: data.customer_service_email || 'N/A',
            website: data.website || 'N/A',
            bankCode: data.bank_code || 'N/A',
            swiftCode: data.swift_code || 'N/A',
            licenseNumber: data.license_number || 'N/A',
            bankType: data.bank_type || 'N/A',
            ownershipType: data.ownership_type || 'N/A',
            rating: data.rating || 'N/A',
            totalAssets: data.total_assets || 0,
            netWorth: data.net_worth || 0,
            branchesCount: data.branches_count || 0,
            atmCount: data.atm_count || 0,
            hasMobileApp: data.has_mobile_app || false,
            hasOnlineBanking: data.has_online_banking || false,
            hasAtmServices: data.has_atm_services || false,
            hasForeignExchange: data.has_foreign_exchange || false,
            services: data.services || [],
            previousNames: data.previous_names || [],
            isVerified: data.is_verified || false,
            verificationDate: data.verification_date ? new Date(data.verification_date).toLocaleDateString('en-US', { 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            }) : 'N/A',
            verificationNotes: data.verification_notes || 'N/A',
            searchCount: data.search_count || 0,
            lastSearched: data.last_searched ? new Date(data.last_searched).toLocaleDateString('en-US', { 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            }) : 'N/A',
            status: data.status || 'Active',
            createdAt: data.created_at ? new Date(data.created_at).toLocaleDateString('en-US', { 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            }) : 'N/A',
            updatedAt: data.updated_at ? new Date(data.updated_at).toLocaleDateString('en-US', { 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            }) : 'N/A',
            // Mock data for cases - would come from separate API
            totalCases: 0,
            activeCases: 0,
            resolvedCases: 0,
            riskLevel: 'Low',
            riskScore: 0,
            lastActivity: data.updated_at ? new Date(data.updated_at).toISOString().split('T')[0] : 'N/A',
            numberOfBranches: data.branches_count || 0,
            previousNames: data.previous_names || [],
            managers: [],
            branches: [],
            cases: []
          };
          console.log('Transformed bank data:', transformedData);
          setBankData(transformedData);
          console.log('Bank data set successfully');
        } else {
          console.error('No bank data found');
          setError('Bank not found');
        }
      } else {
        console.error('Failed to fetch bank data:', response.status);
        setError(`Failed to load bank data: ${response.status}`);
      }
    } catch (error) {
      console.error('Error loading bank data:', error);
      setError('Error loading bank data');
    } finally {
      setIsLoading(false);
    }
  };

  // Load bank analytics
  const loadBankAnalytics = async (bankId) => {
    try {
      setAnalyticsLoading(true);
      const response = await fetch(`http://localhost:8000/api/banks/${bankId}/analytics`, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Bank analytics loaded:', data);
        setAnalytics(data);
      } else {
        console.error('Failed to load bank analytics:', response.status);
        setAnalytics(null);
      }
    } catch (error) {
      console.error('Error loading bank analytics:', error);
      setAnalytics(null);
    } finally {
      setAnalyticsLoading(false);
    }
  };

  // Load bank case statistics
  const loadBankCaseStats = async (bankId) => {
    try {
      setCaseStatsLoading(true);
      const response = await fetch(`http://localhost:8000/api/banks/${bankId}/case-statistics`, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Bank case stats loaded:', data);
        setCaseStats(data);
      } else {
        console.error('Failed to load bank case stats:', response.status);
        setCaseStats(null);
      }
    } catch (error) {
      console.error('Error loading bank case stats:', error);
      setCaseStats(null);
    } finally {
      setCaseStatsLoading(false);
    }
  };

  // Load management data
  const loadManagementData = async (bankId) => {
    // Sample management data - in real implementation, this would come from an API
    const sampleManagement = [
      {
        id: 1,
        name: "Dr. Ernest Kwamina Yedu Addison",
        position: "Governor",
        tenure: "2017 - Present",
        qualifications: "PhD Economics, University of Manchester",
        experience: "25+ years in banking and finance",
        profileId: 1,
        email: "governor@bog.gov.gh",
        phone: "+233 302 666 902",
        bio: "Experienced economist with extensive background in monetary policy and banking supervision."
      },
      {
        id: 2,
        name: "Mrs. Elsie Addo Awadzi",
        position: "First Deputy Governor",
        tenure: "2017 - Present", 
        qualifications: "LLM International Law, Harvard University",
        experience: "20+ years in legal and regulatory affairs",
        profileId: 2,
        email: "first.deputy@bog.gov.gh",
        phone: "+233 302 666 903",
        bio: "Legal expert with extensive experience in financial regulation and international law."
      },
      {
        id: 3,
        name: "Dr. Maxwell Opoku-Afari",
        position: "Second Deputy Governor",
        tenure: "2019 - Present",
        qualifications: "PhD Economics, University of Ghana",
        experience: "18+ years in economic research and policy",
        profileId: 3,
        email: "second.deputy@bog.gov.gh",
        phone: "+233 302 666 904",
        bio: "Economic policy expert with strong background in research and analysis."
      }
    ];
    
    setManagementData(sampleManagement);
  };

  // Load related cases
  const loadRelatedCases = async (bankId) => {
    try {
      setCasesLoading(true);
      console.log('Loading related cases for bank ID:', bankId);

      const url = `http://localhost:8000/api/banks/${bankId}/related-cases?limit=10`;
      console.log('API URL:', url);
      
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      console.log('Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Related cases loaded:', data);
        
        if (data.related_cases && data.related_cases.length > 0) {
          setRelatedCases(data.related_cases);
        } else {
          console.log('No cases found in API response');
          setRelatedCases([]);
        }
      } else {
        console.error('Failed to fetch related cases:', response.status);
        const errorText = await response.text();
        console.error('Error response:', errorText);
        setRelatedCases([]);
      }
    } catch (error) {
      console.error('Error loading related cases:', error);
      setRelatedCases([]);
    } finally {
      setCasesLoading(false);
    }
  };

  // Filter and sort cases
  const filterAndSortCases = (cases, searchQuery, sortBy, sortOrder) => {
    let filtered = cases;

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(caseItem =>
        caseItem.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        caseItem.suit_reference_number?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        caseItem.court_type?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        caseItem.area_of_law?.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Sort cases
    filtered.sort((a, b) => {
      let aValue, bValue;
      
      switch (sortBy) {
        case 'title':
          aValue = a.title || '';
          bValue = b.title || '';
          break;
        case 'court':
          aValue = a.court_type || '';
          bValue = b.court_type || '';
          break;
        case 'date':
        default:
          aValue = new Date(a.date || 0);
          bValue = new Date(b.date || 0);
          break;
      }

      if (sortOrder === 'asc') {
        return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
      } else {
        return aValue > bValue ? -1 : aValue < bValue ? 1 : 0;
      }
    });

    return filtered;
  };

  // Update filtered cases when search query, sort options, or related cases change
  useEffect(() => {
    const filtered = filterAndSortCases(relatedCases, caseSearchQuery, caseSortBy, caseSortOrder);
    setFilteredCases(filtered);
    setCurrentPage(1); // Reset to first page when filtering
  }, [relatedCases, caseSearchQuery, caseSortBy, caseSortOrder]);

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

  if (isLoading) {
  return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-sky-600 mx-auto"></div>
          <p className="mt-4 text-slate-600">Loading bank details...</p>
        </div>
      </div>
    );
  }

  if (error && !bankData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-slate-900 mb-2">Error Loading Bank</h2>
          <p className="text-slate-600 mb-4">{error}</p>
            <button
            onClick={() => navigate(-1)}
            className="inline-flex items-center gap-2 rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700 transition-colors"
            >
            <ArrowLeft className="h-4 w-4" />
            Go Back
            </button>
        </div>
      </div>
    );
  }

  if (!bankData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Building2 className="h-16 w-16 text-slate-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-slate-900 mb-2">Bank Not Found</h2>
          <p className="text-slate-600 mb-4">The requested bank could not be found.</p>
            <button
            onClick={() => navigate(-1)}
            className="inline-flex items-center gap-2 rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700 transition-colors"
            >
            <ArrowLeft className="h-4 w-4" />
            Go Back
            </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Fixed Header */}
      <div className="sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
            <button
                onClick={() => navigate(-1)}
                className="inline-flex items-center gap-2 text-slate-600 hover:text-slate-900 transition-colors"
            >
                <ArrowLeft className="h-5 w-5" />
                Back
            </button>
              <div className="h-6 w-px bg-slate-300" />
              <div className="flex items-center gap-3">
                  <img
                    src={bankData.logo}
                    alt={`${bankData.name} logo`}
                  className="h-8 w-8 rounded object-contain"
                    onError={(e) => {
                    e.target.src = '/banks/default-bank.jpeg';
                    }}
                  />
                <div>
                  <h1 className="text-lg font-semibold text-slate-900">{bankData.name}</h1>
                  <p className="text-sm text-slate-500">{bankData.status}</p>
        </div>
      </div>
            </div>
            <div className="flex items-center gap-3">
              <button className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors">
                <Download className="h-4 w-4" />
                Export
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content with top padding to account for fixed header */}
      <div className="pt-24 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          {/* Left Column - Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Bank Information */}
            <div className="bg-white rounded-lg border border-slate-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                  <Building2 className="h-5 w-5 text-blue-600" />
                  Bank Information
                </h2>
                <button className="text-slate-400 hover:text-slate-600">
                  <RefreshCw className="h-5 w-5" />
                </button>
                </div>
              
                <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                  <div className="space-y-4">
                    <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                      <div className="flex items-center space-x-2 mb-1">
                        <Building2 className="w-4 h-4 text-blue-600" />
                        <span className="text-xs font-medium text-blue-800 uppercase tracking-wide">Bank Name</span>
                      </div>
                      <p className="text-sm font-semibold text-blue-900">{bankData.name}</p>
                      {bankData.shortName && bankData.shortName !== bankData.name && (
                        <p className="text-xs text-blue-700">Short: {bankData.shortName}</p>
                      )}
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                        <Calendar className="w-4 h-4 text-gray-600" />
                        <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Established</span>
                      </div>
                      <p className="text-sm font-semibold text-gray-900">{bankData.established}</p>
                      <p className="text-xs text-gray-600">{bankData.incorporated}</p>
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                        <Shield className="w-4 h-4 text-gray-600" />
                        <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Bank Code</span>
                      </div>
                      <p className="text-sm font-semibold text-gray-900">{bankData.bankCode}</p>
                    <p className="text-xs text-gray-600">SWIFT: {bankData.swiftCode}</p>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                      <div className="flex items-center space-x-2 mb-1">
                        <MapPin className="w-4 h-4 text-green-600" />
                      <span className="text-xs font-medium text-green-800 uppercase tracking-wide">Headquarters</span>
                      </div>
                    <p className="text-sm font-semibold text-green-900">{bankData.headquarters}</p>
                    <p className="text-xs text-green-700">{bankData.address}</p>
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                      <Phone className="w-4 h-4 text-gray-600" />
                      <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Contact</span>
                      </div>
                    <p className="text-sm font-semibold text-gray-900">{bankData.phone}</p>
                    <p className="text-xs text-gray-600">{bankData.email}</p>
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                        <Globe className="w-4 h-4 text-gray-600" />
                        <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Website</span>
                      </div>
                    <a href={bankData.website} target="_blank" rel="noopener noreferrer" className="text-sm font-semibold text-blue-600 hover:text-blue-800">
                      {bankData.website}
                    </a>
                    </div>
                  </div>
                      </div>
                    </div>
                    
            {/* Tabs */}
            <div className="bg-white rounded-lg border border-slate-200">
              <div className="border-b border-slate-200">
                <nav className="flex space-x-8 px-6" aria-label="Tabs">
                  {['manager', 'board', 'secretaries', 'cases'].map((tab) => (
                <button
                      key={tab}
                      className={`py-4 px-1 border-b-2 font-medium text-sm capitalize ${
                        activeTab === tab
                          ? 'border-blue-500 text-blue-600'
                          : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                      }`}
                      onClick={() => setActiveTab(tab)}
                    >
                      {tab}
                </button>
                  ))}
                </nav>
              </div>
              
              <div className="p-6">
                {activeTab === 'manager' && (
                <div>
                    <h3 className="text-lg font-semibold text-slate-900 mb-4">Management Team</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {managementData.map((member) => (
                        <div key={member.id} className="border border-slate-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                          <div className="flex items-start space-x-4">
                            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                              <span className="text-blue-600 font-semibold text-xs">
                                {member.name.split(' ').map(n => n[0]).join('').substring(0, 2)}
                              </span>
                </div>
                            <div className="flex-1">
                              <h4 className="font-semibold text-slate-900 mb-1">{member.name}</h4>
                              <p className="text-sm font-medium text-blue-600 mb-2">{member.position}</p>
                              <div className="space-y-1 text-xs text-slate-600">
                                <p><span className="font-medium">Tenure:</span> {member.tenure}</p>
                                <p><span className="font-medium">Qualifications:</span> {member.qualifications}</p>
                                <p><span className="font-medium">Experience:</span> {member.experience}</p>
                        </div>
                      </div>
                </div>
                      </div>
                      ))}
                    </div>
                </div>
              )}
                      
                {activeTab === 'board' && (
                <div>
                    <h3 className="text-lg font-semibold text-slate-900 mb-4">Board of Directors</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {managementData.map((member) => (
                        <div key={member.id} className="border border-slate-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                          <div className="flex items-start space-x-4">
                            <div className="w-12 h-12 bg-sky-100 rounded-full flex items-center justify-center">
                              <span className="text-sky-600 font-semibold text-xs">
                                {member.name.split(' ').map(n => n[0]).join('').substring(0, 2)}
                              </span>
                </div>
                            <div className="flex-1">
                              <h4 className="font-semibold text-slate-900 mb-1">{member.name}</h4>
                              <p className="text-sm font-medium text-sky-600 mb-2">{member.position}</p>
                              <div className="space-y-1 text-xs text-slate-600">
                                <p><span className="font-medium">Tenure:</span> {member.tenure}</p>
                                <p><span className="font-medium">Qualifications:</span> {member.qualifications}</p>
                                <p><span className="font-medium">Experience:</span> {member.experience}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                        ))}
                </div>
                    
                    {/* Board Committees */}
                    <div className="mt-8">
                      <h4 className="text-lg font-semibold text-slate-900 mb-4">Board Committees</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        <div className="bg-white rounded-lg p-4">
                          <h5 className="font-medium text-slate-900 mb-2">Audit Committee</h5>
                          <p className="text-sm text-slate-600">Oversees financial reporting and internal controls</p>
                          <p className="text-xs text-slate-500 mt-2">Chair: Dr. Kwame Asante</p>
                </div>
                        <div className="bg-white rounded-lg p-4">
                          <h5 className="font-medium text-slate-900 mb-2">Risk Management Committee</h5>
                          <p className="text-sm text-slate-600">Monitors and manages operational and financial risks</p>
                          <p className="text-xs text-slate-500 mt-2">Chair: Mrs. Efua Adjei</p>
                      </div>
                        <div className="bg-white rounded-lg p-4">
                          <h5 className="font-medium text-slate-900 mb-2">Nominations Committee</h5>
                          <p className="text-sm text-slate-600">Reviews board composition and director appointments</p>
                          <p className="text-xs text-slate-500 mt-2">Chair: Dr. Kwame Asante</p>
              </div>
                        <div className="bg-white rounded-lg p-4">
                          <h5 className="font-medium text-slate-900 mb-2">Technology Committee</h5>
                          <p className="text-sm text-slate-600">Oversees digital transformation and IT strategy</p>
                          <p className="text-xs text-slate-500 mt-2">Chair: Mrs. Efua Adjei</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
                  
                {activeTab === 'secretaries' && (
                <div>
                    <h3 className="text-lg font-semibold text-slate-900 mb-4">Secretaries</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {[
                        { 
                          name: 'Ms. Grace Adjei', 
                          position: 'Company Secretary', 
                          experience: '12 years in corporate governance',
                          background: 'Former Legal Counsel at Ghana Stock Exchange',
                          qualifications: 'LLB, ICSA, ACIS'
                        },
                        { 
                          name: 'Mr. Samuel Ofori', 
                          position: 'Assistant Secretary', 
                          experience: '8 years in corporate affairs',
                          background: 'Former Corporate Affairs Officer at Ecobank',
                          qualifications: 'BA Law, ICSA Part I'
                        },
                        { 
                          name: 'Mrs. Comfort Asante', 
                          position: 'Compliance Secretary', 
                          experience: '10 years in regulatory compliance',
                          background: 'Former Compliance Officer at Bank of Ghana',
                          qualifications: 'MSc Banking, CAMS, CCO'
                        }
                      ].map((secretary, index) => (
                        <div key={index} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                          <div className="flex items-start space-x-4">
                            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                              <span className="text-green-600 font-semibold text-xs">
                                {secretary.name.split(' ').map(n => n[0]).join('').substring(0, 2)}
                              </span>
              </div>
                            <div className="flex-1">
                              <h4 className="font-semibold text-gray-900 mb-1">{secretary.name}</h4>
                              <p className="text-sm font-medium text-green-600 mb-2">{secretary.position}</p>
                              <div className="space-y-1 text-xs text-gray-600">
                                <p><span className="font-medium">Experience:</span> {secretary.experience}</p>
                                <p><span className="font-medium">Background:</span> {secretary.background}</p>
                                <p><span className="font-medium">Qualifications:</span> {secretary.qualifications}</p>
                              </div>
                            </div>
              </div>
                              </div>
                  ))}
                            </div>
                            
                    {/* Secretary Responsibilities */}
                    <div className="mt-6 bg-green-50 rounded-lg p-6">
                      <h5 className="text-lg font-semibold text-gray-900 mb-4">Secretarial Functions</h5>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="bg-white rounded-lg p-4">
                          <h6 className="font-medium text-gray-900 mb-2">Corporate Governance</h6>
                          <p className="text-sm text-gray-600">Maintains corporate records, ensures compliance with regulatory requirements, and manages board documentation</p>
                              </div>
                        <div className="bg-white rounded-lg p-4">
                          <h6 className="font-medium text-gray-900 mb-2">Regulatory Compliance</h6>
                          <p className="text-sm text-gray-600">Monitors regulatory changes, ensures timely filings, and maintains relationships with regulatory bodies</p>
                              </div>
                        <div className="bg-white rounded-lg p-4">
                          <h6 className="font-medium text-gray-900 mb-2">Board Support</h6>
                          <p className="text-sm text-gray-600">Coordinates board meetings, prepares agendas, and ensures proper documentation of board decisions</p>
                            </div>
                        <div className="bg-white rounded-lg p-4">
                          <h6 className="font-medium text-gray-900 mb-2">Shareholder Relations</h6>
                          <p className="text-sm text-gray-600">Manages shareholder communications, annual general meetings, and dividend distributions</p>
                          </div>
                            </div>
                          </div>
                    </div>
                  )}

                {activeTab === 'cases' && (
                  <div>
                    {/* Header */}
              <div className="flex items-center justify-between mb-6">
                      <h3 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                        <Scale className="h-5 w-5 text-blue-600" />
                        Related Cases ({relatedCases.length})
                      </h3>
                      <button className="text-slate-400 hover:text-slate-600">
                        <RefreshCw className="h-5 w-5" />
                </button>
              </div>
              
                    {/* Search and Filter Bar */}
                    <div className="flex flex-col sm:flex-row gap-4 mb-6">
                      <div className="flex-1 relative">
                          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                          <input
                            type="text"
                            placeholder="Search cases..."
                            value={caseSearchQuery}
                            onChange={(e) => setCaseSearchQuery(e.target.value)}
                          className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                      <div className="flex gap-2">
                <select
                            value={caseSortBy}
                            onChange={(e) => setCaseSortBy(e.target.value)}
                          className="px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          >
                            <option value="date">Sort by Date</option>
                            <option value="title">Sort by Title</option>
                          <option value="court">Sort by Court</option>
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
                            onClick={() => {
                              setCaseSearchQuery('');
                              setCaseSortBy('date');
                              setCaseSortOrder('desc');
                            }}
                          className="px-4 py-2 text-slate-600 hover:text-slate-800 transition-colors"
                          >
                          Clear
                          </button>
                        </div>
                    </div>

                    {/* Cases List */}
                  {casesLoading ? (
                    <div className="text-center py-8">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="mt-2 text-slate-600">Loading cases...</p>
                    </div>
                  ) : filteredCases.length > 0 ? (
              <div className="space-y-4">
                        {filteredCases.map((caseItem) => (
                          <div key={caseItem.id} className="bg-slate-50 rounded-lg p-4 hover:shadow-md transition-shadow">
                            <div className="flex items-start justify-between">
                      <div className="flex-1">
                                <h4 className="font-semibold text-slate-900 mb-2">{caseItem.title}</h4>
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2 text-sm text-slate-600 mb-3">
                                  <div>
                                    <span className="font-medium">Suit Number:</span> {caseItem.suit_reference_number}
                      </div>
                      <div>
                              <span className="font-medium">Court:</span> {caseItem.court_type || 'N/A'}
                      </div>
                      <div>
                                    <span className="font-medium">Date:</span> {caseItem.date ? new Date(caseItem.date).toLocaleDateString('en-US', { 
                                      year: 'numeric', 
                                      month: 'long', 
                                      day: 'numeric' 
                                    }) : 'N/A'}
                      </div>
                      <div>
                                    <span className="font-medium">Nature:</span> {caseItem.area_of_law || 'N/A'}
                      </div>
                      </div>
                                {caseItem.ai_case_outcome && (
                                  <div className="flex items-center gap-2">
                                    <span className="text-sm text-slate-600">Outcome:</span>
                                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                      caseItem.ai_case_outcome === 'WON' ? 'bg-emerald-100 text-emerald-800' :
                                      caseItem.ai_case_outcome === 'LOST' ? 'bg-red-100 text-red-800' :
                                      'bg-amber-100 text-amber-800'
                                    }`}>
                                      {caseItem.ai_case_outcome}
                                    </span>
                    </div>
                                )}
                              </div>
                              <div className="ml-4">
                        <button 
                                  onClick={() => navigate(`/case-details/${caseItem.id}`)}
                                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                                >
                                  View Case
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <Scale className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                        <p className="text-slate-500">No related cases found for this bank.</p>
                        {caseSearchQuery && (
                          <p className="text-sm text-slate-400 mt-2">Try adjusting your search criteria.</p>
                        )}
                    </div>
                  )}
                  </div>
                )}
              </div>
                        </div>
                        </div>

          {/* Right Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            {/* Risk Assessment */}
            {analytics && (
              <div className="bg-white rounded-lg border border-slate-200 p-6">
                <h3 className="text-lg font-semibold text-slate-900 flex items-center gap-2 mb-4">
                  <AlertTriangle className="h-5 w-5 text-red-600" />
                  Financial Risk Assessment
                  {analyticsLoading && <RefreshCw className="h-4 w-4 animate-spin text-red-600" />}
                </h3>
                {analyticsLoading ? (
                  <div className="space-y-3">
                    <div className="animate-pulse">
                      <div className="h-4 bg-gray-200 rounded mb-2"></div>
                      <div className="h-4 bg-gray-200 rounded mb-2"></div>
                      <div className="h-4 bg-gray-200 rounded mb-2"></div>
                  </div>
              </div>
                ) : (
                  <>
                    <div className="text-center mb-4">
                      <div className="relative w-24 h-24 mx-auto mb-2">
                        <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
                          <circle
                            cx="50"
                            cy="50"
                            r="40"
                            stroke="#e5e7eb"
                            strokeWidth="8"
                            fill="none"
                          />
                          <circle
                            cx="50"
                            cy="50"
                            r="40"
                            stroke={analytics.risk_score <= 30 ? '#10b981' : analytics.risk_score <= 70 ? '#f59e0b' : '#ef4444'}
                            strokeWidth="8"
                            fill="none"
                            strokeDasharray={`${(analytics.risk_score / 100) * 251.2} 251.2`}
                            className="transition-all duration-1000 ease-out"
                          />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center">
                          <span className={`text-2xl font-bold ${getRiskScoreColor(analytics.risk_score)}`}>
                            {analytics.risk_score}
                        </span>
                  </div>
                    </div>
                      <div className="space-y-1">
                        <p className={`text-lg font-semibold ${getRiskScoreColor(analytics.risk_score)}`}>
                          {analytics.risk_level} Risk
                        </p>
                        <p className="text-sm text-slate-600">Financial Risk Score</p>
                </div>
          </div>

                    <div className="space-y-3">
                      <div className="flex justify-between text-sm">
                        <span className="text-slate-600">Resolved:</span>
                        <span className="font-semibold text-green-600">{caseStats?.resolved_cases || 0}</span>
                </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-slate-600">Unresolved:</span>
                        <span className="font-semibold text-orange-600">{caseStats?.unresolved_cases || 0}</span>
                </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-slate-600">Mixed:</span>
                        <span className="font-semibold text-yellow-600">{caseStats?.mixed_cases || 0}</span>
              </div>
                    </div>
                    
                    {analytics.risk_factors && analytics.risk_factors.length > 0 && (
                      <div className="text-left mt-4">
                        <p className="text-xs font-medium text-slate-700 mb-2">Key Risk Factors:</p>
                        <div className="flex flex-wrap gap-1">
                          {analytics.risk_factors.slice(0, 4).map((factor, index) => (
                            <span key={index} className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded">
                              {factor}
                  </span>
                          ))}
                          {analytics.risk_factors.length > 4 && (
                            <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                              +{analytics.risk_factors.length - 4} more
                            </span>
                          )}
                </div>
                  </div>
                )}
                  </>
                )}
              </div>
            )}

            {/* Quick Stats */}
            <div className="bg-white rounded-lg border border-slate-200 p-6">
              <h3 className="text-lg font-semibold text-slate-900 flex items-center gap-2 mb-4">
                <Clock className="h-5 w-5 text-blue-600" />
                Quick Stats
                {(caseStatsLoading || analyticsLoading) && <RefreshCw className="h-4 w-4 animate-spin text-blue-600" />}
              </h3>
              {(caseStatsLoading || analyticsLoading) ? (
                <div className="space-y-3">
                  <div className="animate-pulse">
                    <div className="h-4 bg-gray-200 rounded mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded mb-2"></div>
                </div>
                </div>
              ) : (
              <div className="space-y-3">
                <div className="flex justify-between">
                    <span className="text-sm text-slate-600">Total Cases:</span>
                    <span className="text-sm font-semibold text-slate-900">{caseStats?.total_cases || 0}</span>
                </div>
                <div className="flex justify-between">
                    <span className="text-sm text-slate-600">Resolved Cases:</span>
                    <span className="text-sm font-semibold text-slate-900">{caseStats?.resolved_cases || 0}</span>
                </div>
                <div className="flex justify-between">
                    <span className="text-sm text-slate-600">Unresolved Cases:</span>
                    <span className="text-sm font-semibold text-slate-900">{caseStats?.unresolved_cases || 0}</span>
                </div>
                <div className="flex justify-between">
                    <span className="text-sm text-slate-600">Favorable Cases:</span>
                    <span className="text-sm font-semibold text-green-600">{caseStats?.favorable_cases || 0}</span>
                </div>
                <div className="flex justify-between">
                    <span className="text-sm text-slate-600">Unfavorable Cases:</span>
                    <span className="text-sm font-semibold text-red-600">{caseStats?.unfavorable_cases || 0}</span>
              </div>
                <div className="flex justify-between">
                    <span className="text-sm text-slate-600">Mixed Cases:</span>
                    <span className="text-sm font-semibold text-yellow-600">{caseStats?.mixed_cases || 0}</span>
              </div>
                <div className="flex justify-between">
                    <span className="text-sm text-slate-600">Overall Outcome:</span>
                    <span className={`text-sm font-semibold ${
                      caseStats?.case_outcome === 'Favorable' ? 'text-green-600' :
                      caseStats?.case_outcome === 'Unfavorable' ? 'text-red-600' :
                      caseStats?.case_outcome === 'Mixed' ? 'text-yellow-600' :
                      'text-gray-600'
                    }`}>
                      {caseStats?.case_outcome || 'N/A'}
                  </span>
          </div>
        </div>
              )}
      </div>

            </div>
              </div>
            </div>
    </div>
  );
};

export default BankDetail;
