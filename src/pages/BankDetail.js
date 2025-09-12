import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Building2, Calendar, MapPin, Phone, Mail, TrendingUp, AlertTriangle, CheckCircle, Clock, User, Scale, Eye, EyeOff, Globe, CreditCard, Smartphone, CreditCard as Atm, DollarSign, Star, Shield, Award, ExternalLink, Download, XCircle, Users, Briefcase, GraduationCap, FileText, Search, Filter, ArrowUpDown } from 'lucide-react';

const BankDetail = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [bankData, setBankData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedSections, setExpandedSections] = useState({
    basicInfo: true,
    contactInfo: true,
    services: true,
    financialInfo: true,
    management: true,
    cases: true,
    previousNames: true
  });

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
    'ABII National Bank': '/banks/abii national.jpeg'
  };
  // Management data - would come from API in real implementation
  const [managementData, setManagementData] = useState([]);
  const [relatedCases, setRelatedCases] = useState([]);
  const [filteredCases, setFilteredCases] = useState([]);
  const [casesLoading, setCasesLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [casesPerPage] = useState(10);
  const [totalCases, setTotalCases] = useState(0); // eslint-disable-line no-unused-vars
  const [caseSearchQuery, setCaseSearchQuery] = useState('');
  const [caseSortBy, setCaseSortBy] = useState('date'); // date, title, suit_number
  const [caseSortOrder, setCaseSortOrder] = useState('desc'); // asc, desc
  const [showRequestModal, setShowRequestModal] = useState(false);
  const [selectedCase, setSelectedCase] = useState(null);
  const [requestType, setRequestType] = useState('case_details');
  const [requestMessage, setRequestMessage] = useState('');

  // Load bank data
  useEffect(() => {
    const bankId = searchParams.get('id');
    const bankName = searchParams.get('name');
    
    console.log('URL Parameters - Bank ID:', bankId, 'Bank Name:', bankName);
    
    if (bankId || bankName) {
      setCurrentPage(1); // Reset pagination when bank changes
      loadBankData(bankId, bankName);
      loadManagementData(bankId, bankName);
      loadRelatedCases(bankId, bankName);
    }
  }, [searchParams]); // eslint-disable-line react-hooks/exhaustive-deps

  // eslint-disable-next-line no-unused-vars
  const getSampleCasesForBank = (bankName) => {
    if (!bankName) {
      console.log('No bank name provided');
      return [];
    }
    
    const bankNameLower = bankName.toLowerCase();
    console.log('Checking bank name:', bankNameLower);
    
    if (bankNameLower.includes('access bank') || bankNameLower.includes('access') || bankNameLower.includes('access bank ghana')) {
      console.log('Matched Access Bank');
      return [
        {
          id: 2006,
          title: "ACCESS BANK GHANA LIMITED vs. MRS. LUCKY AFI ALLOTEY T/A & ANO.",
          suit_reference_number: "SUIT NO.: BFS/284/12",
          date: "2017-11-24",
          status: "Resolved",
          court_type: "High Court",
          presiding_judge: "Justice Smith",
          protagonist: "ACCESS BANK GHANA LIMITED",
          antagonist: "MRS. LUCKY AFI ALLOTEY T/A & ANO.",
          case_summary: "A commercial dispute involving loan recovery and debt collection between Access Bank Ghana Limited and the defendants."
        },
        {
          id: 2028,
          title: "ECOBANK NIGERIA PLC vs. HISS HANDS HOUSING AGENCY AND ACCESS BANK (GHANA) LIMITED",
          suit_reference_number: "CIVIL APPEAL NO. J4/49/2016",
          date: "2017-12-06",
          status: "Active",
          court_type: "Commercial Court",
          presiding_judge: "Justice Johnson",
          protagonist: "ECOBANK NIGERIA PLC",
          antagonist: "HISS HANDS HOUSING AGENCY AND ACCESS BANK (GHANA) LIMITED",
          case_summary: "A complex commercial litigation involving multiple parties including Access Bank Ghana Limited as a defendant."
        },
        {
          id: 3846,
          title: "ACCESS BANK LTD vs. MARKET DIRECT AND OTHERS",
          suit_reference_number: "SUIT NO. CM/0048/16",
          date: "2018-05-21",
          status: "Resolved",
          court_type: "High Court",
          presiding_judge: "Justice Brown",
          protagonist: "ACCESS BANK LTD",
          antagonist: "MARKET DIRECT AND OTHERS",
          case_summary: "A commercial dispute involving breach of contract and financial obligations between Access Bank and Market Direct."
        },
        {
          id: 3847,
          title: "ACCESS BANK GH LTD vs. MARKET DIRECT AND OTHERS",
          suit_reference_number: "SUIT NO. CM/0048/16",
          date: "2018-04-21",
          status: "Resolved",
          court_type: "High Court",
          presiding_judge: "Justice Brown",
          protagonist: "ACCESS BANK GH LTD",
          antagonist: "MARKET DIRECT AND OTHERS",
          case_summary: "A commercial dispute involving breach of contract and financial obligations between Access Bank Ghana and Market Direct."
        },
        {
          id: 4173,
          title: "MARIANE QUANSAH vs. ACCESS BANK",
          suit_reference_number: "SUIT NO. INDL/63/12",
          date: "2017-01-24",
          status: "Resolved",
          court_type: "High Court",
          presiding_judge: "Justice Wilson",
          protagonist: "MARIANE QUANSAH",
          antagonist: "ACCESS BANK",
          case_summary: "A consumer dispute involving Mariane Quansah and Access Bank regarding banking services."
        },
        {
          id: 4656,
          title: "KOBBY BREW vs. ACCESS BANK GHANA LIMITED, AFS IRIC CONSULT, PETER ANNAN AND RAYMOND KOTEY",
          suit_reference_number: "SUIT NO. BFS/08/2012",
          date: "2016-11-04",
          status: "Resolved",
          court_type: "High Court",
          presiding_judge: "Justice Davis",
          protagonist: "KOBBY BREW",
          antagonist: "ACCESS BANK GHANA LIMITED, AFS IRIC CONSULT, PETER ANNAN AND RAYMOND KOTEY",
          case_summary: "A complex commercial dispute involving multiple defendants including Access Bank Ghana Limited."
        },
        {
          id: 6634,
          title: "CORNELIUS OGBU vs. ACCESS BANK (GH) LTD",
          suit_reference_number: "CIVIL APPEAL SUIT NO: H1/16/15",
          date: "2015-02-18",
          status: "Resolved",
          court_type: "Appeal Court",
          presiding_judge: "Justice Thompson",
          protagonist: "CORNELIUS OGBU",
          antagonist: "ACCESS BANK (GH) LTD",
          case_summary: "A civil appeal case involving Cornelius Ogbu and Access Bank Ghana Limited."
        }
      ];
    } else if (bankNameLower.includes('ghana commercial bank') || bankNameLower.includes('gcb') || bankNameLower.includes('commercial')) {
      console.log('Matched Ghana Commercial Bank');
      return [
        {
          id: 83,
          title: "GHANA COMMERCIAL BANK Vs. EASTERN ALLOYS COMPANY LIMITED, WORLD PRAYER CENTRE, DELA AKPEY",
          suit_reference_number: "Suit No. 83",
          date: "2018-07-04",
          status: "Resolved",
          court_type: "High Court",
          presiding_judge: "Justice Wilson",
          protagonist: "GHANA COMMERCIAL BANK",
          antagonist: "EASTERN ALLOYS COMPANY LIMITED, WORLD PRAYER CENTRE, DELA AKPEY",
          case_summary: "A commercial dispute involving loan recovery and debt collection by Ghana Commercial Bank."
        }
      ];
    } else if (bankNameLower.includes('ecobank') || bankNameLower.includes('eco')) {
      console.log('Matched Ecobank');
      return [
        {
          id: 2028,
          title: "ECOBANK NIGERIA PLC vs. HISS HANDS HOUSING AGENCY AND ACCESS BANK (GHANA) LIMITED",
          suit_reference_number: "Suit No. 2028",
          date: "2017-12-06",
          status: "Active",
          court_type: "Commercial Court",
          presiding_judge: "Justice Johnson",
          protagonist: "ECOBANK NIGERIA PLC",
          antagonist: "HISS HANDS HOUSING AGENCY AND ACCESS BANK (GHANA) LIMITED",
          case_summary: "A complex commercial litigation involving multiple parties including Ecobank Nigeria PLC."
        }
      ];
    } else if (bankNameLower.includes('bank')) {
      console.log('Matched generic bank');
      // Return some generic bank cases for any bank
      return [
        {
          id: 2006,
          title: `${bankName.toUpperCase()} vs. COMMERCIAL DISPUTE PARTY`,
          suit_reference_number: "Suit No. 2006",
          date: "2017-11-24",
          status: "Resolved",
          court_type: "High Court",
          presiding_judge: "Justice Smith",
          protagonist: bankName.toUpperCase(),
          antagonist: "COMMERCIAL DISPUTE PARTY",
          case_summary: `A commercial dispute involving ${bankName} and the defendant party.`
        },
        {
          id: 2028,
          title: `${bankName.toUpperCase()} vs. FINANCIAL SERVICES LITIGATION`,
          suit_reference_number: "Suit No. 2028",
          date: "2017-12-06",
          status: "Active",
          court_type: "Commercial Court",
          presiding_judge: "Justice Johnson",
          protagonist: bankName.toUpperCase(),
          antagonist: "FINANCIAL SERVICES LITIGATION",
          case_summary: `A financial services litigation case involving ${bankName}.`
        }
      ];
    }
    
    console.log('No bank match found');
    return [];
  };

  const loadManagementData = async (bankId, bankName) => {
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
        bio: "Legal expert specializing in financial regulation and international banking law."
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
        bio: "Renowned economist with expertise in macroeconomic policy and financial stability."
      },
      {
        id: 4,
        name: "Mr. Johnson Asiama",
        position: "Chief Executive Officer",
        tenure: "2020 - Present",
        qualifications: "MBA Finance, London Business School",
        experience: "22+ years in commercial banking",
        profileId: 4,
        email: "ceo@bank.com",
        phone: "+233 302 123 456",
        bio: "Seasoned banking executive with extensive experience in retail and corporate banking."
      }
    ];
    
    setManagementData(sampleManagement);
  };

  const loadRelatedCases = async (bankId, bankName) => {
    try {
      setCasesLoading(true);
      console.log('Loading related cases for bank:', bankName);
      console.log('Bank ID:', bankId);
      
      // For testing, create a token with user ID 1
      let token = localStorage.getItem('accessToken');
      if (!token) {
        // Create a test token with user ID 1
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzU3NjAzNzU4fQ.r0VQhhM6QMwTm8Ej8a2ENvdI6DzK06o62fUV4AbxxHM';
        console.log('Using test token for API access');
      }

                    // Simple title search - search for cases containing the bank name
                    const url = `http://localhost:8000/api/case-search/search?query=${encodeURIComponent(bankName)}&page=${currentPage}&limit=${casesPerPage}`;
      console.log('API URL:', url);
      
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      console.log('Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('API Response:', data);
        
        if (data.results && data.results.length > 0) {
          console.log(`Found ${data.results.length} cases with "${bankName}" in title`);
          setRelatedCases(data.results);
          setTotalCases(data.total || data.results.length);
        } else {
          console.log('No cases found in API response');
          setRelatedCases([]);
          setTotalCases(0);
        }
      } else {
        console.error('Failed to fetch related cases:', response.status);
        const errorText = await response.text();
        console.error('Error response:', errorText);
        setRelatedCases([]);
        setTotalCases(0);
      }
    } catch (error) {
      console.error('Error loading related cases:', error);
      setRelatedCases([]);
      setTotalCases(0);
    } finally {
      setCasesLoading(false);
    }
  };

  const handleRequestDetails = (caseItem) => {
    setSelectedCase(caseItem);
    setShowRequestModal(true);
    setRequestMessage('');
  };

  const handleSubmitRequest = () => {
    // In a real application, this would send the request to a backend API
    const requestData = {
      type: requestType,
      caseId: selectedCase.id,
      caseNumber: selectedCase.suit_reference_number,
      bankName: bankData.name,
      message: requestMessage,
      timestamp: new Date().toISOString()
    };

    console.log('Request submitted:', requestData);
    
    // Show success message
    alert(`Request submitted successfully!\n\nRequest Type: ${requestType === 'case_details' ? 'Case Details' : requestType === 'full_report' ? 'Full Report' : 'Legal Documents'}\nCase: ${selectedCase.suit_reference_number}\nBank: ${bankData.name}`);
    
    // Close modal and reset
    setShowRequestModal(false);
    setSelectedCase(null);
    setRequestMessage('');
  };

  const loadBankData = async (bankId, bankName) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const token = localStorage.getItem('accessToken');
      if (!token) {
        console.error('No authentication token found');
        setError('Authentication required');
        return;
      }

      let url;
      if (bankId) {
        url = `http://localhost:8000/api/banks/${bankId}`;
      } else if (bankName) {
        // Search for bank by name
        url = `http://localhost:8000/api/banks/search?name=${encodeURIComponent(bankName)}&limit=1`;
      }

      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        let data;
        if (bankId) {
          data = await response.json();
        } else {
          const searchResult = await response.json();
          data = searchResult.banks && searchResult.banks.length > 0 ? searchResult.banks[0] : null;
        }

        if (data) {
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
            description: data.description || 'No description available',
            notes: data.notes || 'No notes available',
            isActive: data.is_active || false,
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
          setBankData(transformedData);
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


  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
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

  const formatCurrency = (amount) => {
    if (!amount || amount === 0) return 'N/A';
    return new Intl.NumberFormat('en-GH', {
      style: 'currency',
      currency: 'GHS',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  // Filter and sort cases
  const filterAndSortCases = (cases, searchQuery, sortBy, sortOrder) => {
    let filtered = cases;

    // Filter by search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = cases.filter(caseItem => 
        caseItem.title.toLowerCase().includes(query) ||
        caseItem.suit_reference_number?.toLowerCase().includes(query) ||
        caseItem.court_type?.toLowerCase().includes(query) ||
        caseItem.presiding_judge?.toLowerCase().includes(query)
      );
    }

    // Sort cases
    filtered.sort((a, b) => {
      let aValue, bValue;
      
      switch (sortBy) {
        case 'title':
          aValue = a.title.toLowerCase();
          bValue = b.title.toLowerCase();
          break;
        case 'suit_number':
          aValue = a.suit_reference_number || '';
          bValue = b.suit_reference_number || '';
          break;
        case 'date':
        default:
          aValue = new Date(a.date || 0);
          bValue = new Date(b.date || 0);
          break;
      }

      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
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
              <div className="h-px w-8 bg-slate-300"></div>
              <div className="flex items-center gap-4">
                <div className="h-12 w-12 rounded-full bg-sky-100 flex items-center justify-center overflow-hidden">
                  <img
                    src={bankData.logo}
                    alt={`${bankData.name} logo`}
                    className="h-full w-full object-contain"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                  <div className="h-full w-full flex items-center justify-center text-xl" style={{display: 'none'}}>
                    🏦
            </div>
                </div>
                <div>
                  <h1 className="text-xl font-semibold text-slate-900">{bankData.name}</h1>
                  <p className="text-sm text-slate-600">
                    {bankData.bankCode} • {formatRegion(bankData.region)}
                  </p>
        </div>
      </div>
            </div>
            <div className="flex items-center gap-3">
                <span className={`inline-flex items-center gap-1 rounded-full px-3 py-1 text-sm font-semibold ring-1 ${getRiskColor(bankData.riskLevel)}`}>
                  <span className={`inline-block h-2 w-2 rounded-full ${getRiskColor(bankData.riskLevel).split(' ')[1].replace('text-', 'bg-')}`}></span>
                  {bankData.riskLevel} Risk
                </span>
              <button className="inline-flex items-center gap-2 rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700 transition-colors">
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
            {/* Basic Information */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                  <Building2 className="h-5 w-5 text-sky-600" />
                  Basic Information
                </h2>
                <button
                  onClick={() => toggleSection('basicInfo')}
                  className="text-slate-400 hover:text-slate-600"
                >
                  {expandedSections.basicInfo ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
                </div>
              
              {expandedSections.basicInfo && (
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
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                        <Award className="w-4 h-4 text-gray-600" />
                        <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">License Number</span>
                      </div>
                      <p className="text-sm font-semibold text-gray-900">{bankData.licenseNumber}</p>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                      <div className="flex items-center space-x-2 mb-1">
                        <MapPin className="w-4 h-4 text-green-600" />
                        <span className="text-xs font-medium text-green-800 uppercase tracking-wide">Location</span>
                      </div>
                      <p className="text-sm font-semibold text-green-900">{formatRegion(bankData.region)}</p>
                      <p className="text-xs text-green-700">{bankData.city}, {bankData.country}</p>
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                        <Building2 className="w-4 h-4 text-gray-600" />
                        <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Bank Type</span>
                      </div>
                      <p className="text-sm font-semibold text-gray-900">{bankData.bankType}</p>
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                        <User className="w-4 h-4 text-gray-600" />
                        <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Ownership</span>
                </div>
                      <p className="text-sm font-semibold text-gray-900">{bankData.ownershipType}</p>
                </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                        <Star className="w-4 h-4 text-gray-600" />
                        <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Rating</span>
                </div>
                      <p className="text-sm font-semibold text-gray-900">{bankData.rating}</p>
                </div>
                </div>
                </div>
              )}
            </section>

            {/* Previous Names */}
            {bankData.previousNames && bankData.previousNames.length > 0 && (
              <section className="rounded-xl border border-slate-200 bg-white p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                    <Clock className="h-5 w-5 text-purple-600" />
                    Previous Names
                  </h2>
                  <button
                    onClick={() => toggleSection('previousNames')}
                    className="text-slate-400 hover:text-slate-600"
                  >
                    {expandedSections.previousNames ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
                
                {expandedSections.previousNames && (
                  <div className="space-y-3">
                    <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                      <div className="flex items-center space-x-2 mb-2">
                        <Clock className="w-4 h-4 text-purple-600" />
                        <span className="text-xs font-medium text-purple-800 uppercase tracking-wide">Historical Names</span>
                      </div>
                      <div className="space-y-2">
                        {bankData.previousNames.map((name, index) => (
                          <div key={index} className="flex items-center space-x-2">
                            <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                            <span className="text-sm text-purple-900">{name}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </section>
            )}

            {/* Contact Information */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                  <Phone className="h-5 w-5 text-sky-600" />
                  Contact Information
                </h2>
                <button
                  onClick={() => toggleSection('contactInfo')}
                  className="text-slate-400 hover:text-slate-600"
                >
                  {expandedSections.contactInfo ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>

              {expandedSections.contactInfo && (
                <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
              <div className="space-y-4">
                    <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                      <div className="flex items-center space-x-2 mb-1">
                        <Phone className="w-4 h-4 text-blue-600" />
                        <span className="text-xs font-medium text-blue-800 uppercase tracking-wide">Phone</span>
                      </div>
                      <p className="text-sm font-semibold text-blue-900">{bankData.phone}</p>
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                        <Mail className="w-4 h-4 text-gray-600" />
                        <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Email</span>
                      </div>
                      <p className="text-sm font-semibold text-gray-900 break-all">{bankData.email}</p>
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                        <Globe className="w-4 h-4 text-gray-600" />
                        <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Website</span>
                      </div>
                      <p className="text-sm font-semibold text-gray-900 break-all">{bankData.website}</p>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                      <div className="flex items-center space-x-2 mb-1">
                        <MapPin className="w-4 h-4 text-green-600" />
                        <span className="text-xs font-medium text-green-800 uppercase tracking-wide">Address</span>
                      </div>
                      <p className="text-sm font-semibold text-green-900">{bankData.address}</p>
                      <p className="text-xs text-green-700">{bankData.postalCode}</p>
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                        <Phone className="w-4 h-4 text-gray-600" />
                        <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Customer Service</span>
                      </div>
                      <p className="text-sm font-semibold text-gray-900">{bankData.customerServicePhone}</p>
                      <p className="text-xs text-gray-600 break-all">{bankData.customerServiceEmail}</p>
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                        <CreditCard className="w-4 h-4 text-gray-600" />
                        <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">SWIFT Code</span>
                      </div>
                      <p className="text-sm font-semibold text-gray-900">{bankData.swiftCode}</p>
                    </div>
                  </div>
                </div>
              )}
            </section>

            {/* Services & Features */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                  <CreditCard className="h-5 w-5 text-sky-600" />
                  Services & Features
                </h2>
                <button
                  onClick={() => toggleSection('services')}
                  className="text-slate-400 hover:text-slate-600"
                >
                  {expandedSections.services ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
              
              {expandedSections.services && (
                <div className="space-y-6">
                  {/* Digital Services */}
                <div>
                    <h3 className="text-sm font-medium text-slate-700 mb-3">Digital Services</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div className={`p-4 rounded-lg border ${bankData.hasMobileApp ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'}`}>
                        <div className="flex items-center gap-3">
                          <Smartphone className={`h-5 w-5 ${bankData.hasMobileApp ? 'text-green-600' : 'text-gray-400'}`} />
                      <div>
                            <p className="text-sm font-medium text-slate-900">Mobile App</p>
                            <p className="text-xs text-slate-500">{bankData.hasMobileApp ? 'Available' : 'Not Available'}</p>
                </div>
                        </div>
                      </div>
                      
                      <div className={`p-4 rounded-lg border ${bankData.hasOnlineBanking ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'}`}>
                        <div className="flex items-center gap-3">
                          <Globe className={`h-5 w-5 ${bankData.hasOnlineBanking ? 'text-green-600' : 'text-gray-400'}`} />
                <div>
                            <p className="text-sm font-medium text-slate-900">Online Banking</p>
                            <p className="text-xs text-slate-500">{bankData.hasOnlineBanking ? 'Available' : 'Not Available'}</p>
                </div>
                      </div>
                    </div>
                    
                      <div className={`p-4 rounded-lg border ${bankData.hasAtmServices ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'}`}>
                        <div className="flex items-center gap-3">
                          <Atm className={`h-5 w-5 ${bankData.hasAtmServices ? 'text-green-600' : 'text-gray-400'}`} />
                <div>
                            <p className="text-sm font-medium text-slate-900">ATM Services</p>
                            <p className="text-xs text-slate-500">{bankData.hasAtmServices ? 'Available' : 'Not Available'}</p>
                </div>
                        </div>
                      </div>
                      
                      <div className={`p-4 rounded-lg border ${bankData.hasForeignExchange ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'}`}>
                        <div className="flex items-center gap-3">
                          <DollarSign className={`h-5 w-5 ${bankData.hasForeignExchange ? 'text-green-600' : 'text-gray-400'}`} />
                <div>
                            <p className="text-sm font-medium text-slate-900">Foreign Exchange</p>
                            <p className="text-xs text-slate-500">{bankData.hasForeignExchange ? 'Available' : 'Not Available'}</p>
                </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Services List */}
                  {bankData.services && bankData.services.length > 0 && (
                <div>
                      <h3 className="text-sm font-medium text-slate-700 mb-3">Additional Services</h3>
                      <div className="flex flex-wrap gap-2">
                        {bankData.services.map((service, index) => (
                          <span key={index} className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-sky-100 text-sky-800">
                            {service}
                          </span>
                        ))}
                </div>
              </div>
                  )}
                </div>
              )}
            </section>

            {/* Financial Information */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                  <DollarSign className="h-5 w-5 text-sky-600" />
                  Financial Information
                </h2>
                <button
                  onClick={() => toggleSection('financialInfo')}
                  className="text-slate-400 hover:text-slate-600"
                >
                  {expandedSections.financialInfo ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
                </div>

              {expandedSections.financialInfo && (
                <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                  <div className="space-y-4">
                    <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                      <div className="flex items-center space-x-2 mb-1">
                        <DollarSign className="w-4 h-4 text-blue-600" />
                        <span className="text-xs font-medium text-blue-800 uppercase tracking-wide">Total Assets</span>
                      </div>
                      <p className="text-sm font-semibold text-blue-900">{formatCurrency(bankData.totalAssets)}</p>
              </div>

                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                        <TrendingUp className="w-4 h-4 text-gray-600" />
                        <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Net Worth</span>
                      </div>
                      <p className="text-sm font-semibold text-gray-900">{formatCurrency(bankData.netWorth)}</p>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                      <div className="flex items-center space-x-2 mb-1">
                        <Building2 className="w-4 h-4 text-green-600" />
                        <span className="text-xs font-medium text-green-800 uppercase tracking-wide">Branches</span>
                      </div>
                      <p className="text-sm font-semibold text-green-900">{bankData.branchesCount}</p>
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center space-x-2 mb-1">
                        <Atm className="w-4 h-4 text-gray-600" />
                        <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">ATM Count</span>
                      </div>
                      <p className="text-sm font-semibold text-gray-900">{bankData.atmCount}</p>
                    </div>
                  </div>
                </div>
              )}
            </section>

            {/* Management Team */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                  <Users className="h-5 w-5 text-sky-600" />
                  Management Team
                </h2>
                <button
                  onClick={() => toggleSection('management')}
                  className="text-slate-400 hover:text-slate-600"
                >
                  {expandedSections.management ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
              
              {expandedSections.management && (
                <div className="space-y-6">
                  {managementData.map((executive) => (
                    <div key={executive.id} className="bg-slate-50 rounded-lg p-6 border border-slate-200 hover:border-sky-300 transition-colors">
                      <div className="flex items-start gap-4">
                        <div className="h-16 w-16 rounded-full bg-sky-100 flex items-center justify-center flex-shrink-0">
                          <User className="h-8 w-8 text-sky-600" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <h3 className="text-lg font-semibold text-slate-900 mb-1">{executive.name}</h3>
                              <p className="text-sm font-medium text-sky-600 mb-2">{executive.position}</p>
                              <div className="flex items-center gap-4 text-xs text-slate-500 mb-3">
                                <span className="flex items-center gap-1">
                                  <Clock className="h-3 w-3" />
                                  {executive.tenure}
                                </span>
                                <span className="flex items-center gap-1">
                                  <Briefcase className="h-3 w-3" />
                                  {executive.experience}
                                </span>
                              </div>
                            </div>
                            <button
                              onClick={() => navigate(`/person-profile/${executive.profileId}`)}
                              className="ml-4 inline-flex items-center gap-1 px-3 py-1 bg-sky-50 text-sky-700 rounded-md hover:bg-sky-100 text-sm font-medium transition-colors"
                            >
                              <User className="h-3 w-3" />
                              View Profile
                            </button>
              </div>

                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                            <div className="space-y-2">
                              <div className="flex items-center gap-2">
                                <GraduationCap className="h-4 w-4 text-slate-400" />
                                <span className="text-sm font-medium text-slate-600">Qualifications:</span>
                              </div>
                              <p className="text-sm text-slate-700 ml-6">{executive.qualifications}</p>
                            </div>
                            
                            <div className="space-y-2">
                              <div className="flex items-center gap-2">
                                <Mail className="h-4 w-4 text-slate-400" />
                                <span className="text-sm font-medium text-slate-600">Contact:</span>
                              </div>
                              <div className="ml-6 space-y-1">
                                <p className="text-sm text-slate-700">{executive.email}</p>
                                <p className="text-sm text-slate-700">{executive.phone}</p>
                              </div>
                            </div>
                          </div>
                          
                          <div className="mt-4">
                            <div className="flex items-center gap-2 mb-2">
                              <FileText className="h-4 w-4 text-slate-400" />
                              <span className="text-sm font-medium text-slate-600">Bio:</span>
                            </div>
                            <p className="text-sm text-slate-700 ml-6">{executive.bio}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {managementData.length === 0 && (
                    <div className="text-center py-8">
                      <Users className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                      <p className="text-slate-500">No management information available</p>
                    </div>
                  )}
                </div>
              )}
            </section>

            {/* Related Cases */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                  <Scale className="h-5 w-5 text-sky-600" />
                  Related Cases ({filteredCases.length} of {relatedCases.length})
                </h2>
                <button
                  onClick={() => toggleSection('cases')}
                  className="text-slate-400 hover:text-slate-600"
                >
                  {expandedSections.cases ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
              
              {expandedSections.cases && (
                <div className="space-y-4">
                  {/* Search and Filter Controls */}
                  {relatedCases.length > 0 && (
                    <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {/* Search Input */}
                        <div className="relative">
                          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                          <input
                            type="text"
                            placeholder="Search cases..."
                            value={caseSearchQuery}
                            onChange={(e) => setCaseSearchQuery(e.target.value)}
                            className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-sky-500 focus:border-sky-500 text-sm"
                          />
                        </div>
                        
                        {/* Sort By */}
                        <div className="relative">
                          <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                <select
                            value={caseSortBy}
                            onChange={(e) => setCaseSortBy(e.target.value)}
                            className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-sky-500 focus:border-sky-500 text-sm appearance-none bg-white"
                          >
                            <option value="date">Sort by Date</option>
                            <option value="title">Sort by Title</option>
                            <option value="suit_number">Sort by Suit Number</option>
                </select>
                        </div>

                        {/* Sort Order */}
                        <div className="relative">
                          <ArrowUpDown className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                <select
                            value={caseSortOrder}
                            onChange={(e) => setCaseSortOrder(e.target.value)}
                            className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-sky-500 focus:border-sky-500 text-sm appearance-none bg-white"
                          >
                            <option value="desc">Newest First</option>
                            <option value="asc">Oldest First</option>
                </select>
                        </div>
              </div>

                      {/* Clear Filters */}
                      {(caseSearchQuery || caseSortBy !== 'date' || caseSortOrder !== 'desc') && (
                        <div className="mt-3 flex justify-end">
                          <button
                            onClick={() => {
                              setCaseSearchQuery('');
                              setCaseSortBy('date');
                              setCaseSortOrder('desc');
                            }}
                            className="text-sm text-slate-600 hover:text-slate-800 underline"
                          >
                            Clear all filters
                          </button>
                        </div>
                      )}
                    </div>
                  )}

                  {casesLoading ? (
                    <div className="text-center py-8">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-sky-600 mx-auto"></div>
                      <p className="mt-2 text-slate-600">Loading related cases...</p>
                    </div>
                  ) : filteredCases.length > 0 ? (
              <div className="space-y-4">
                      {filteredCases
                        .slice((currentPage - 1) * casesPerPage, currentPage * casesPerPage)
                        .map((caseItem) => (
                  <div key={caseItem.id} className="border border-slate-200 rounded-lg p-4 hover:border-sky-300 transition-colors">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <h3 className="font-medium text-slate-900 mb-1">{caseItem.title}</h3>
                              <p className="text-sm text-slate-600">Suit No: {caseItem.suit_reference_number}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                    caseItem.status === 'Active' ? 'bg-amber-100 text-amber-700' : 
                                    caseItem.status === 'Resolved' ? 'bg-emerald-100 text-emerald-700' : 
                                    'bg-slate-100 text-slate-700'
                        }`}>
                          {caseItem.status}
                        </span>
                              <span className="text-xs text-slate-500">
                                {caseItem.date ? new Date(caseItem.date).toLocaleDateString('en-US', { 
                                  year: 'numeric', 
                                  month: 'short', 
                                  day: 'numeric' 
                                }) : 'N/A'}
                        </span>
                      </div>
                    </div>
                    
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-600 mb-3">
                      <div>
                              <span className="font-medium">Court:</span> {caseItem.court_type || 'N/A'}
                      </div>
                      <div>
                              <span className="font-medium">Judge:</span> {caseItem.presiding_judge || 'N/A'}
                      </div>
                      <div>
                              <span className="font-medium">Plaintiff:</span> {caseItem.protagonist || 'N/A'}
                      </div>
                      <div>
                              <span className="font-medium">Defendant:</span> {caseItem.antagonist || 'N/A'}
                      </div>
                    </div>
                    
                          {caseItem.case_summary && (
                            <p className="text-sm text-slate-700 mb-3 line-clamp-2">
                              {caseItem.case_summary.length > 150 
                                ? `${caseItem.case_summary.substring(0, 150)}...` 
                                : caseItem.case_summary
                              }
                            </p>
                    )}
                    
                    <div className="flex items-center justify-between">
                            <span className="text-sm text-slate-500">
                              Case ID: {caseItem.id}
                            </span>
                      <div className="flex items-center gap-2">
                        <button 
                          onClick={() => handleRequestDetails(caseItem)}
                          className="inline-flex items-center gap-1 px-3 py-1 bg-sky-50 text-sky-700 rounded-md hover:bg-sky-100 text-sm font-medium transition-colors"
                        >
                                <FileText className="w-3 h-3" />
                          Request Details
                        </button>
                        <button 
                                onClick={() => navigate(`/case-details/${caseItem.id}?q=${encodeURIComponent(bankData.name)}`)}
                          className="text-sky-600 hover:text-sky-700 text-sm font-medium"
                        >
                          View Full Details →
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
                  ) : relatedCases.length > 0 ? (
                    <div className="text-center py-8">
                      <Search className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                      <p className="text-slate-500">No cases match your search criteria</p>
                      <p className="text-sm text-slate-400 mt-1">Try adjusting your search terms or filters</p>
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <Scale className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                      <p className="text-slate-500">No related cases found</p>
                      <p className="text-sm text-slate-400 mt-1">Cases involving this bank will appear here</p>
                    </div>
                  )}
                  
                  {/* Pagination Controls */}
                  {filteredCases.length > 0 && filteredCases.length > casesPerPage && (
                    <div className="flex items-center justify-between mt-6 pt-4 border-t border-slate-200">
                  <div className="text-sm text-slate-600">
                        Showing {((currentPage - 1) * casesPerPage) + 1} to {Math.min(currentPage * casesPerPage, filteredCases.length)} of {filteredCases.length} cases
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                          onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                      disabled={currentPage === 1}
                          className="px-3 py-1 text-sm border border-slate-300 rounded-md hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Previous
                    </button>
                        <span className="px-3 py-1 text-sm text-slate-600">
                          Page {currentPage} of {Math.ceil(filteredCases.length / casesPerPage)}
                        </span>
                        <button
                          onClick={() => setCurrentPage(prev => Math.min(Math.ceil(filteredCases.length / casesPerPage), prev + 1))}
                          disabled={currentPage >= Math.ceil(filteredCases.length / casesPerPage)}
                          className="px-3 py-1 text-sm border border-slate-300 rounded-md hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Next
                    </button>
                  </div>
                    </div>
                  )}
                </div>
              )}
            </section>
          </div>

          {/* Right Column - Sidebar */}
          <div className="space-y-6">
            {/* Risk Assessment */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-sky-600" />
                Risk Assessment
              </h2>
              <div className="text-center">
                <div className={`text-3xl font-bold mb-2 ${getRiskScoreColor(bankData.riskScore)}`}>
                  {bankData.riskScore}%
                </div>
                <div className="text-sm text-slate-600 mb-4">{bankData.riskLevel} Risk Score</div>
                <div className="w-full bg-slate-200 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full ${getProgressBarColor(bankData.riskScore)}`}
                    style={{ width: `${bankData.riskScore}%` }}
                  ></div>
                </div>
                <p className="text-xs text-slate-500 mt-2">Based on case history and outcomes</p>
              </div>
            </section>

            {/* Verification Status */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
                {bankData.isVerified ? (
                  <CheckCircle className="h-5 w-5 text-green-600" />
                ) : (
                  <XCircle className="h-5 w-5 text-red-600" />
                )}
                Verification Status
              </h2>
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  {bankData.isVerified ? (
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  ) : (
                    <XCircle className="h-4 w-4 text-red-600" />
                  )}
                  <span className="text-sm font-medium text-slate-900">
                    {bankData.isVerified ? 'Verified' : 'Not Verified'}
                  </span>
                </div>
                {bankData.verificationDate && (
                  <div className="text-xs text-slate-500">
                    Verified on: {bankData.verificationDate}
                  </div>
                )}
                {bankData.verificationNotes && (
                  <div className="text-xs text-slate-500">
                    {bankData.verificationNotes}
                  </div>
                )}
              </div>
            </section>

            {/* Quick Stats */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
                <Clock className="h-5 w-5 text-sky-600" />
                Quick Stats
              </h2>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Search Count</span>
                  <span className="text-sm font-medium text-slate-900">{bankData.searchCount}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Last Searched</span>
                  <span className="text-sm font-medium text-slate-900">{bankData.lastSearched || 'Never'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Status</span>
                  <span className={`text-sm font-medium ${
                    bankData.isActive ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {bankData.isActive ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Created</span>
                  <span className="text-sm font-medium text-slate-900">{bankData.createdAt}</span>
                </div>
              </div>
            </section>

            {/* Quick Actions */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-sky-600" />
                Quick Actions
              </h2>
              <div className="space-y-3">
                <button className="w-full text-left px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                  <User className="h-4 w-4 inline mr-2" />
                  View Related People
                </button>
                <button className="w-full text-left px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                  <Scale className="h-4 w-4 inline mr-2" />
                  View Similar Cases
                </button>
                <button className="w-full text-left px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                  <Download className="h-4 w-4 inline mr-2" />
                  Download Report
                </button>
                <button className="w-full text-left px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                  <ExternalLink className="h-4 w-4 inline mr-2" />
                  Visit Website
                </button>
              </div>
            </section>
          </div>
        </div>
      </div>

      {/* Request Details Modal */}
      {showRequestModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Request Case Details</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-700 mb-2">Request Type</label>
              <select
                value={requestType}
                onChange={(e) => setRequestType(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
              >
                <option value="case_details">Case Details</option>
                <option value="full_report">Full Report</option>
                <option value="legal_documents">Legal Documents</option>
              </select>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-700 mb-2">Case Information</label>
              <div className="bg-slate-50 p-3 rounded-lg text-sm">
                <p><strong>Case:</strong> {selectedCase?.suit_reference_number}</p>
                <p><strong>Title:</strong> {selectedCase?.title}</p>
                <p><strong>Bank:</strong> {bankData?.name}</p>
              </div>
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-slate-700 mb-2">Additional Message (Optional)</label>
              <textarea
                value={requestMessage}
                onChange={(e) => setRequestMessage(e.target.value)}
                placeholder="Please specify any additional information you need..."
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 h-20 resize-none"
              />
            </div>

            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowRequestModal(false)}
                className="px-4 py-2 text-slate-600 hover:text-slate-800 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSubmitRequest}
                className="px-4 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 transition-colors"
              >
                Submit Request
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BankDetail;
