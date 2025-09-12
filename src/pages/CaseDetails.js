import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { 
  ArrowLeft, 
  Calendar, 
  User, 
  Building2, 
  Scale, 
  Clock, 
  CheckCircle, 
  XCircle, 
  AlertCircle,
  AlertTriangle,
  FileText,
  Users,
  Banknote,
  Gavel,
  BookOpen,
  MapPin,
  Tag,
  ExternalLink,
  Download,
  Copy,
  ChevronDown,
  ChevronUp,
  Shield,
  Eye,
  X,
  TrendingUp,
  DollarSign,
  Percent,
  Calculator,
  History
} from 'lucide-react';

const CaseDetails = () => {
  const { caseId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [expandedSections, setExpandedSections] = useState({
    basicInfo: true,
    caseSummary: true,
    caseContent: true,
    people: false,
    riskAssessment: true,
    financialImpact: true,
    caseTimeline: true,
    conclusion: true,
    caseDocuments: true
  });

  // Get search query from URL params
  const searchParams = new URLSearchParams(location.search);
  const searchQuery = searchParams.get('q') || '';

  useEffect(() => {
    console.log('CaseDetails useEffect triggered with caseId:', caseId);
    if (caseId) {
      loadCaseDetails();
    } else {
      console.error('No caseId provided');
      setError('No case ID provided');
      setLoading(false);
    }
  }, [caseId]); // eslint-disable-line react-hooks/exhaustive-deps

  const loadCaseDetails = async () => {
    try {
      setLoading(true);
      console.log('Loading case details for caseId:', caseId);
      
      const token = localStorage.getItem('accessToken') || 'test-token-123';
      console.log('Using token:', token ? 'Present' : 'Missing');
      
      const response = await fetch(`http://localhost:8000/api/case-search/${caseId}/details`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      console.log('API Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Case data loaded:', data);
        setCaseData(data);
      } else {
        const errorText = await response.text();
        console.error('API Error:', errorText);
        setError(`Failed to load case details: ${response.status} - ${errorText}`);
      }
    } catch (err) {
      setError('Error loading case details');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch {
      return dateString;
    }
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
      'BON': 'Bono East Region',
      'OTI': 'Oti Region',
      'SAV': 'Savannah Region',
      'NEA': 'North East Region'
    };
    
    return regionMappings[regionCode.toUpperCase()] || regionCode;
  };

  const formatArray = (arr) => {
    if (!arr || !Array.isArray(arr)) return [];
    return arr;
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    // You could add a toast notification here
  };

  // Court type mapping function
  const getCourtTypeName = (courtType) => {
    if (!courtType) return 'N/A';
    
    const courtTypeMap = {
      'SC': 'Supreme Court',
      'HC': 'High Court', 
      'CA': 'Court of Appeal',
      'supreme court': 'Supreme Court',
      'high court': 'High Court',
      'court of appeal': 'Court of Appeal',
      'SUPREME COURT': 'Supreme Court',
      'HIGH COURT': 'High Court',
      'COURT OF APPEAL': 'Court of Appeal'
    };
    
    return courtTypeMap[courtType] || courtType;
  };

  const getOutcomeIcon = (outcome) => {
    switch (outcome?.toLowerCase()) {
      case 'favorable':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'unfavorable':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'mixed':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      default:
        return <Clock className="w-5 h-5 text-gray-400" />;
    }
  };

  const SectionHeader = ({ title, icon: Icon, isExpanded, onToggle }) => (
    <button
      onClick={onToggle}
      className="w-full flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100 transition-colors"
    >
      <div className="flex items-center space-x-3">
        <Icon className="w-5 h-5 text-blue-600" />
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
      </div>
      {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
    </button>
  );

  const InfoRow = ({ label, value, icon: Icon, copyable = false }) => {
    if (!value) return null;
    
    return (
      <div className="flex items-start space-x-3 py-2">
        {Icon && <Icon className="w-4 h-4 text-gray-500 mt-1 flex-shrink-0" />}
        <div className="flex-1">
          <span className="text-sm font-medium text-gray-600">{label}:</span>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-900">{value}</span>
            {copyable && (
              <button
                onClick={() => copyToClipboard(value)}
                className="p-1 hover:bg-gray-200 rounded"
                title="Copy to clipboard"
              >
                <Copy className="w-3 h-3" />
              </button>
            )}
          </div>
        </div>
      </div>
    );
  };

  const ArrayDisplay = ({ label, items, icon: Icon }) => {
    if (!items || !Array.isArray(items) || items.length === 0) return null;
    
    return (
      <div className="py-2">
        <div className="flex items-center space-x-2 mb-2">
          {Icon && <Icon className="w-4 h-4 text-gray-500" />}
          <span className="text-sm font-medium text-gray-600">{label}:</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {items.map((item, index) => (
            <span
              key={index}
              className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
            >
              {item}
            </span>
          ))}
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading case details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600">{error}</p>
          <button
            onClick={() => navigate(-1)}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  if (!caseData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">Case not found</p>
          <button
            onClick={() => navigate(-1)}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Fixed Header */}
      <div className="fixed top-0 left-0 right-0 bg-white shadow-sm border-b z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate(-1)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <div className="flex-1 min-w-0">
                <h1 className="text-xl font-bold text-gray-900 break-words leading-tight">
                  {caseData?.title || 'Case Details'}
                </h1>
                <div className="flex items-center space-x-4 text-sm text-gray-600">
                  {searchQuery && (
                    <span className="flex items-center space-x-1">
                      <span className="font-medium">Search:</span>
                      <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                        "{searchQuery}"
                      </span>
                    </span>
                  )}
                  {caseData?.suit_reference_number && (
                    <span className="flex items-center space-x-1">
                      <Scale className="w-4 h-4" />
                      <span>{caseData.suit_reference_number}</span>
                    </span>
                  )}
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              {getOutcomeIcon(caseData?.metadata?.outcome)}
              <span className="text-sm text-gray-600">
                {caseData?.metadata?.outcome || 'Unknown'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Spacer for fixed header */}
      <div className="h-24"></div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="space-y-6">
          {/* Basic Information */}
          <div className="bg-white rounded-lg shadow-sm border">
            <SectionHeader
              title="Basic Information"
              icon={FileText}
              isExpanded={expandedSections.basicInfo}
              onToggle={() => toggleSection('basicInfo')}
            />
            {expandedSections.basicInfo && (
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  
                  {/* Case Details Grid */}
                  <div className="space-y-4">
                    <div className="flex items-center space-x-2 mb-4">
                      <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Case Details</h3>
                    </div>
                    
                    <div className="space-y-3">
                      <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                        <div className="flex items-center space-x-2 mb-1">
                          <Scale className="w-4 h-4 text-blue-600" />
                          <span className="text-xs font-medium text-blue-800 uppercase tracking-wide">Suit Reference</span>
                        </div>
                        <p className="text-sm font-semibold text-blue-900 break-all">{caseData.suit_reference_number || 'N/A'}</p>
                      </div>
                      
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <div className="flex items-center space-x-2 mb-1">
                          <Calendar className="w-4 h-4 text-gray-600" />
                          <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Date</span>
                        </div>
                        <p className="text-sm font-semibold text-gray-900">{formatDate(caseData.date)}</p>
                      </div>
                      
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <div className="flex items-center space-x-2 mb-1">
                          <Calendar className="w-4 h-4 text-gray-600" />
                          <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Year</span>
                        </div>
                        <p className="text-sm font-semibold text-gray-900">{caseData.year || 'N/A'}</p>
                      </div>
                      
                    </div>
                  </div>

                  {/* Court Information Grid */}
                  <div className="space-y-4">
                    <div className="flex items-center space-x-2 mb-4">
                      <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Court Information</h3>
                    </div>
                    
                    <div className="space-y-3">
                      <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                        <div className="flex items-center space-x-2 mb-1">
                          <Building2 className="w-4 h-4 text-green-600" />
                          <span className="text-xs font-medium text-green-800 uppercase tracking-wide">Court Type</span>
                        </div>
                        <p className="text-sm font-semibold text-green-900">{getCourtTypeName(caseData.court_type)}</p>
                      </div>
                    </div>
                  </div>

                  {/* Publication & Location Grid */}
                  <div className="space-y-4">
                    <div className="flex items-center space-x-2 mb-4">
                      <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Publication & Location</h3>
                    </div>
                    
                    <div className="space-y-3">
                      <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                        <div className="flex items-center space-x-2 mb-1">
                          <BookOpen className="w-4 h-4 text-purple-600" />
                          <span className="text-xs font-medium text-purple-800 uppercase tracking-wide">Citation</span>
                        </div>
                        <p className="text-sm font-semibold text-purple-900 break-all">{caseData.citation || 'N/A'}</p>
                      </div>
                      
                      
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <div className="flex items-center space-x-2 mb-1">
                          <MapPin className="w-4 h-4 text-gray-600" />
                          <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Town</span>
                        </div>
                        <p className="text-sm font-semibold text-gray-900">{caseData.town || 'N/A'}</p>
                      </div>
                      
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <div className="flex items-center space-x-2 mb-1">
                          <MapPin className="w-4 h-4 text-gray-600" />
                          <span className="text-xs font-medium text-gray-700 uppercase tracking-wide">Region</span>
                        </div>
                        <p className="text-sm font-semibold text-gray-900">{formatRegion(caseData.region)}</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* File Downloads Section */}
                {(caseData.file_url || caseData.firebase_url) && (
                  <div className="mt-6 pt-6 border-t border-gray-200">
                    <div className="flex items-center space-x-2 mb-4">
                      <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">File Downloads</h3>
                    </div>
                    <div className="flex items-center space-x-2">
                      <ExternalLink className="w-4 h-4 text-gray-500" />
                      <span className="text-sm font-medium text-gray-600">Available Files:</span>
                      <div className="flex space-x-3">
                        {caseData.file_url && (
                          <a
                            href={caseData.file_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center px-3 py-2 bg-blue-100 text-blue-800 text-sm font-medium rounded-lg hover:bg-blue-200 transition-colors"
                          >
                            <Download className="w-4 h-4 mr-2" />
                            Download
                          </a>
                        )}
                        {caseData.firebase_url && (
                          <a
                            href={caseData.firebase_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center px-3 py-2 bg-green-100 text-green-800 text-sm font-medium rounded-lg hover:bg-green-200 transition-colors"
                          >
                            <ExternalLink className="w-4 h-4 mr-2" />
                            View Online
                          </a>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Case Summary */}
          <div className="bg-white rounded-lg shadow-sm border">
            <SectionHeader
              title="AI-Generated Case Summary"
              icon={FileText}
              isExpanded={expandedSections.caseSummary}
              onToggle={() => toggleSection('caseSummary')}
            />
            {expandedSections.caseSummary && (
              <div className="p-6">
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-l-4 border-blue-500 p-6 rounded-lg">
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                        <FileText className="w-5 h-5 text-blue-600" />
                      </div>
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-3">
                        <h3 className="text-lg font-semibold text-blue-900">Professional Case Summary</h3>
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                          AI Generated
                        </span>
                      </div>
                      <div className="text-gray-800 leading-relaxed">
                        {(() => {
                          const summary = caseData?.metadata?.case_summary || caseData?.case_summary || 'No AI-generated summary available for this case.';
                          
                          if (summary === 'No AI-generated summary available for this case.') {
                            return <div className="text-gray-500 italic">{summary}</div>;
                          }
                          
                          // Parse the structured summary
                          const sections = summary.split('|').map(section => section.trim());
                          const holding = sections.find(s => s.startsWith('HOLDING:'))?.replace('HOLDING:', '').trim();
                          const facts = sections.find(s => s.startsWith('FACTS:'))?.replace('FACTS:', '').trim();
                          const legalPrinciples = sections.find(s => s.startsWith('LEGAL PRINCIPLES:'))?.replace('LEGAL PRINCIPLES:', '').trim();
                          const outcome = sections.find(s => s.startsWith('OUTCOME:'))?.replace('OUTCOME:', '').trim();
                          
                          return (
                            <div className="space-y-4">
                              {holding && (
                                <div className="bg-white p-4 rounded-lg border-l-4 border-blue-500">
                                  <h4 className="font-semibold text-blue-900 mb-2 flex items-center">
                                    <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                                    HOLDING
                                  </h4>
                                  <p className="text-gray-700 leading-relaxed">{holding}</p>
                                </div>
                              )}
                              
                              {facts && (
                                <div className="bg-white p-4 rounded-lg border-l-4 border-green-500">
                                  <h4 className="font-semibold text-green-900 mb-2 flex items-center">
                                    <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                                    FACTS
                                  </h4>
                                  <p className="text-gray-700 leading-relaxed">{facts}</p>
                                </div>
                              )}
                              
                              {legalPrinciples && (
                                <div className="bg-white p-4 rounded-lg border-l-4 border-purple-500">
                                  <h4 className="font-semibold text-purple-900 mb-2 flex items-center">
                                    <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                                    LEGAL PRINCIPLES
                                  </h4>
                                  <p className="text-gray-700 leading-relaxed">{legalPrinciples}</p>
                                </div>
                              )}
                              
                              {outcome && (
                                <div className="bg-white p-4 rounded-lg border-l-4 border-orange-500">
                                  <h4 className="font-semibold text-orange-900 mb-2 flex items-center">
                                    <span className="w-2 h-2 bg-orange-500 rounded-full mr-2"></span>
                                    OUTCOME
                                  </h4>
                                  <p className="text-gray-700 leading-relaxed">{outcome}</p>
                                </div>
                              )}
                            </div>
                          );
                        })()}
                      </div>
                      {caseData?.metadata?.case_summary && (
                        <div className="mt-4 text-xs text-gray-500 italic">
                          This summary was generated using AI analysis of the case decision and provides a structured overview of the legal holding, key facts, legal principles, and outcome.
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* People Involved */}
          <div className="bg-white rounded-lg shadow-sm border">
            <SectionHeader
              title="People Involved"
              icon={Users}
              isExpanded={expandedSections.people}
              onToggle={() => toggleSection('people')}
            />
            {expandedSections.people && (
              <div className="p-6 space-y-4">
                <InfoRow label="Judgement By" value={caseData.judgement_by} icon={Gavel} />
                <InfoRow label="Opinion By" value={caseData.opinion_by} icon={Gavel} />
                <InfoRow label="Protagonist" value={caseData.protagonist} icon={User} />
                
                {/* Show lawyers from metadata if available, otherwise from main case data */}
                {caseData.metadata?.lawyers && formatArray(caseData.metadata.lawyers).length > 0 ? (
                  <ArrayDisplay label="Lawyers" items={formatArray(caseData.metadata.lawyers)} icon={User} />
                ) : (
                  <InfoRow label="Lawyers" value={caseData.lawyers} icon={User} />
                )}
                
                {/* Additional metadata people */}
                {caseData.metadata && (
                  <>
                    <ArrayDisplay label="Judges" items={formatArray(caseData.metadata.judges)} icon={Gavel} />
                  </>
                )}
              </div>
            )}
          </div>

          {/* Case Content */}
          <div className="bg-white rounded-lg shadow-sm border">
            <SectionHeader
              title="Case Content"
              icon={FileText}
              isExpanded={expandedSections.caseContent}
              onToggle={() => toggleSection('caseContent')}
            />
            {expandedSections.caseContent && (
              <div className="p-6 space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-medium text-gray-600">Case Content</h4>
                    <button
                      onClick={() => setIsModalOpen(true)}
                      className="inline-flex items-center space-x-2 px-3 py-1.5 bg-blue-600 text-white text-xs font-medium rounded-lg hover:bg-blue-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                    >
                      <Eye className="w-4 h-4" />
                      <span>View Full Case</span>
                    </button>
                  </div>
                  <div 
                    className="text-sm text-gray-900 leading-relaxed max-h-96 overflow-y-auto border border-gray-200 rounded-lg p-4 bg-gray-50 prose prose-sm max-w-none"
                    dangerouslySetInnerHTML={{
                      __html: caseData.summernote_content || caseData.summernote || caseData.summarnote || caseData.metadata?.case_summary || caseData.case_summary || 'No case content available'
                    }}
                  />
                </div>
                
                {/* Link to full case on dennislawgh.com */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-start space-x-3">
                    <ExternalLink className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                    <div className="flex-1">
                      <h4 className="text-sm font-medium text-blue-900 mb-1">Full Case Details</h4>
                      <p className="text-sm text-blue-700 mb-3">
                        For the complete case details, including full decision, judgement, commentary, and legal analysis, visit:
                      </p>
                      <a
                        href="https://dennislawgh.com"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        <ExternalLink className="w-4 h-4 mr-2" />
                        View on DennisLawGH.com
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Case Timeline */}
          <div className="bg-white rounded-lg shadow-sm border">
            <SectionHeader
              title="Case Timeline"
              icon={History}
              isExpanded={expandedSections.caseTimeline}
              onToggle={() => toggleSection('caseTimeline')}
            />
            {expandedSections.caseTimeline && (
              <div className="p-6">
                {caseData?.hearings && caseData.hearings.length > 0 ? (
                  <div className="flow-root">
                    <ul className="-mb-8">
                      {caseData.hearings.map((hearing, index) => (
                        <li key={hearing.id}>
                          <div className={`relative ${index < caseData.hearings.length - 1 ? 'pb-8' : ''}`}>
                            {index < caseData.hearings.length - 1 && (
                              <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true"></span>
                            )}
                            <div className="relative flex space-x-3">
                              <div>
                                <span className={`h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white ${
                                  hearing.remark === 'fj' ? 'bg-purple-500' :
                                  hearing.remark === 'fr' ? 'bg-yellow-500' :
                                  'bg-blue-500'
                                }`}>
                                  {hearing.remark === 'fj' ? <Gavel className="h-4 w-4 text-white" /> :
                                   hearing.remark === 'fr' ? <Scale className="h-4 w-4 text-white" /> :
                                   <Clock className="h-4 w-4 text-white" />}
                                </span>
                              </div>
                              <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                                <div className="flex-1">
                                  <div className="flex items-center space-x-2 mb-1">
                                    <p className="text-sm font-medium text-gray-900">
                                      {hearing.remark === 'fj' ? 'For Judgement' :
                                       hearing.remark === 'fr' ? 'For Ruling' :
                                       'For Hearing'}
                                    </p>
                                    {hearing.hearing_time && (
                                      <span className="text-xs text-gray-500">• {hearing.hearing_time}</span>
                                    )}
                                  </div>
                                  <p className="text-sm text-gray-500 mb-2">
                                    {formatDate(hearing.hearing_date)}
                                  </p>
                                  {hearing.coram && (
                                    <p className="text-xs text-gray-600 mb-2">
                                      <span className="font-medium">Coram:</span> {hearing.coram}
                                    </p>
                                  )}
                                  {hearing.proceedings && (
                                    <p className="text-xs text-gray-700 bg-gray-50 p-2 rounded">
                                      <span className="font-medium">Proceedings:</span> {hearing.proceedings}
                                    </p>
                                  )}
                                </div>
                                <div className="text-right text-sm whitespace-nowrap text-gray-500">
                                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                    hearing.remark === 'fj' ? 'bg-purple-100 text-purple-800' :
                                    hearing.remark === 'fr' ? 'bg-yellow-100 text-yellow-800' :
                                    'bg-blue-100 text-blue-800'
                                  }`}>
                                    {hearing.remark?.toUpperCase()}
                                  </span>
                                </div>
                              </div>
                            </div>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : (
                  <div className="flow-root">
                    <ul className="-mb-8">
                      {/* Case Filing */}
                      <li>
                        <div className="relative pb-8">
                          <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true"></span>
                          <div className="relative flex space-x-3">
                            <div>
                              <span className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center ring-8 ring-white">
                                <FileText className="h-4 w-4 text-white" />
                              </span>
                            </div>
                            <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                              <div>
                                <p className="text-sm font-medium text-gray-900">Case Filed</p>
                                <p className="text-sm text-gray-500">
                                  {caseData?.date ? formatDate(caseData.date) : 'N/A'}
                                </p>
                              </div>
                              <div className="text-right text-sm whitespace-nowrap text-gray-500">
                                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium">
                                  Initial Filing
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </li>

                      {/* Court Assignment */}
                      <li>
                        <div className="relative pb-8">
                          <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true"></span>
                          <div className="relative flex space-x-3">
                            <div>
                              <span className="h-8 w-8 rounded-full bg-green-500 flex items-center justify-center ring-8 ring-white">
                                <Scale className="h-4 w-4 text-white" />
                              </span>
                            </div>
                            <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                              <div>
                                <p className="text-sm font-medium text-gray-900">Court Assignment</p>
                                <p className="text-sm text-gray-500">
                                  {getCourtTypeName(caseData?.court_type)} • {caseData?.region || 'N/A'}
                                </p>
                              </div>
                              <div className="text-right text-sm whitespace-nowrap text-gray-500">
                                <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                                  Court Process
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </li>

                      {/* Case Processing */}
                      <li>
                        <div className="relative pb-8">
                          <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true"></span>
                          <div className="relative flex space-x-3">
                            <div>
                              <span className="h-8 w-8 rounded-full bg-yellow-500 flex items-center justify-center ring-8 ring-white">
                                <Clock className="h-4 w-4 text-white" />
                              </span>
                            </div>
                            <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                              <div>
                                <p className="text-sm font-medium text-gray-900">Case Processing</p>
                                <p className="text-sm text-gray-500">
                                  {caseData?.metadata?.processed_at ? formatDate(caseData.metadata.processed_at) : 'In Progress'}
                                </p>
                              </div>
                              <div className="text-right text-sm whitespace-nowrap text-gray-500">
                                <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs font-medium">
                                  {caseData?.metadata?.is_processed ? 'Processed' : 'Processing'}
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </li>

                      {/* Judgment/Resolution */}
                      <li>
                        <div className="relative">
                          <div className="relative flex space-x-3">
                            <div>
                              <span className="h-8 w-8 rounded-full bg-purple-500 flex items-center justify-center ring-8 ring-white">
                                <Gavel className="h-4 w-4 text-white" />
                              </span>
                            </div>
                            <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                              <div>
                                <p className="text-sm font-medium text-gray-900">Judgment/Resolution</p>
                                <p className="text-sm text-gray-500">
                                  {caseData?.status === 1 ? 'Judgment Delivered' : 'Case Resolved'}
                                  {caseData?.updated_at && ` • ${formatDate(caseData.updated_at)}`}
                                </p>
                              </div>
                              <div className="text-right text-sm whitespace-nowrap text-gray-500">
                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                  caseData?.status === 1
                                    ? 'bg-red-100 text-red-800'
                                    : 'bg-green-100 text-green-800'
                                }`}>
                                  {caseData?.status === 1 ? 'Judgment' : 'Resolved'}
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </li>
                    </ul>
                  </div>
                )}

                {/* Additional Timeline Information */}
                <div className="mt-6 bg-gray-50 rounded-lg p-4">
                  <h4 className="text-sm font-medium text-gray-900 mb-3">Timeline Summary</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500">Total Hearings:</span>
                      <span className="ml-2 font-medium text-gray-900">
                        {caseData?.hearings ? caseData.hearings.length : 0}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Case Duration:</span>
                      <span className="ml-2 font-medium text-gray-900">
                        {caseData?.date && caseData?.updated_at ?
                          `${Math.ceil((new Date(caseData.updated_at) - new Date(caseData.date)) / (1000 * 60 * 60 * 24))} days` :
                          'N/A'
                        }
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Current Status:</span>
                      <span className="ml-2 font-medium text-gray-900">
                        {caseData?.status === 1 ? 'Judgment Delivered' : 'Case Resolved'}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Court Type:</span>
                      <span className="ml-2 font-medium text-gray-900">
                        {getCourtTypeName(caseData?.court_type)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Risk Assessment, Affiliations & Organizations */}
          <div className="bg-white rounded-lg shadow-sm border">
            <SectionHeader
              title="Risk Assessment, Affiliations & Organizations"
              icon={Shield}
              isExpanded={expandedSections.riskAssessment}
              onToggle={() => toggleSection('riskAssessment')}
            />
            {expandedSections.riskAssessment && (
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  
                  {/* Risk Assessment Grid */}
                  <div className="space-y-4">
                    <div className="flex items-center space-x-2 mb-4">
                      <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Risk Assessment</h3>
                    </div>
                    
                    <div className="space-y-3">
                      <div className="bg-red-50 p-4 rounded-lg border-l-4 border-red-500">
                        <div className="flex items-center space-x-2 mb-1">
                          <Shield className="w-4 h-4 text-red-600" />
                          <span className="text-xs font-medium text-red-800 uppercase tracking-wide">Resolution Status</span>
                        </div>
                        <p className="text-sm font-semibold text-red-900">
                          {caseData?.metadata?.resolution_status || 'Unknown'}
                        </p>
                      </div>
                      
                      <div className="bg-orange-50 p-4 rounded-lg border-l-4 border-orange-500">
                        <div className="flex items-center space-x-2 mb-1">
                          <AlertTriangle className="w-4 h-4 text-orange-600" />
                          <span className="text-xs font-medium text-orange-800 uppercase tracking-wide">Outcome</span>
                        </div>
                        <p className="text-sm font-semibold text-orange-900">
                          {caseData?.metadata?.outcome || 'Unknown'}
                        </p>
                      </div>
                      
                      <div className="bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-500">
                        <div className="flex items-center space-x-2 mb-1">
                          <Gavel className="w-4 h-4 text-yellow-600" />
                          <span className="text-xs font-medium text-yellow-800 uppercase tracking-wide">Decision Type</span>
                        </div>
                        <p className="text-sm font-semibold text-yellow-900">
                          {caseData?.metadata?.decision_type || 'N/A'}
                        </p>
                      </div>
                    </div>
                  </div>


                  {/* Insurance & Financial Grid */}
                  <div className="space-y-4">
                    <div className="flex items-center space-x-2 mb-4">
                      <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Insurance & Financial</h3>
                    </div>
                    
                    <div className="space-y-3">
                      <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                        <div className="flex items-center space-x-2 mb-2">
                          <Shield className="w-4 h-4 text-purple-600" />
                          <span className="text-xs font-medium text-purple-800 uppercase tracking-wide">Insurance Involved</span>
                        </div>
                        <div className="text-sm text-purple-900">
                          {caseData?.metadata?.insurance_involved && formatArray(caseData.metadata.insurance_involved).length > 0 ? (
                            <div className="space-y-1">
                              {formatArray(caseData.metadata.insurance_involved).map((insurance, index) => (
                                <div key={index} className="px-2 py-1 bg-purple-100 rounded text-xs">
                                  {insurance}
                                </div>
                              ))}
                            </div>
                          ) : (
                            <span className="text-gray-500">No insurance involved</span>
                          )}
                        </div>
                      </div>
                      
                      <div className="bg-gray-50 p-4 rounded-lg border-l-4 border-gray-500">
                        <div className="flex items-center space-x-2 mb-1">
                          <Banknote className="w-4 h-4 text-gray-600" />
                          <span className="text-xs font-medium text-gray-800 uppercase tracking-wide">Monetary Amount</span>
                        </div>
                        <p className="text-sm font-semibold text-gray-900">
                          {caseData?.metadata?.monetary_amount ? `$${caseData.metadata.monetary_amount.toLocaleString()}` : 'N/A'}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Financial Impact & Subject Matter */}
          <div className="bg-white rounded-lg shadow-sm border">
            <SectionHeader
              title="Financial Impact & Subject Matter"
              icon={TrendingUp}
              isExpanded={expandedSections.financialImpact}
              onToggle={() => toggleSection('financialImpact')}
            />
            {expandedSections.financialImpact && (
              <div className="p-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  
                  {/* Financial Impact Grid */}
                  <div className="space-y-6">
                    <div className="flex items-center space-x-2 mb-4">
                      <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Financial Impact</h3>
                    </div>
                    
                    <div className="space-y-4">
                      {/* Monetary Amount */}
                      <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                        <div className="flex items-center space-x-2 mb-2">
                          <DollarSign className="w-5 h-5 text-green-600" />
                          <span className="text-sm font-medium text-green-800 uppercase tracking-wide">Monetary Amount</span>
                        </div>
                        <p className="text-lg font-bold text-green-900">
                          {caseData?.metadata?.monetary_amount ? `$${caseData.metadata.monetary_amount.toLocaleString()}` : 'N/A'}
                        </p>
                        {caseData?.metadata?.monetary_amount && (
                          <p className="text-xs text-green-700 mt-1">
                            {caseData.metadata.monetary_amount > 1000000 ? 'High Value Case' : 
                             caseData.metadata.monetary_amount > 100000 ? 'Medium Value Case' : 'Low Value Case'}
                          </p>
                        )}
                      </div>

                      {/* Financial Risk Level */}
                      <div className="bg-red-50 p-4 rounded-lg border-l-4 border-red-500">
                        <div className="flex items-center space-x-2 mb-2">
                          <AlertTriangle className="w-5 h-5 text-red-600" />
                          <span className="text-sm font-medium text-red-800 uppercase tracking-wide">Financial Risk Level</span>
                        </div>
                        <p className="text-lg font-bold text-red-900">
                          {caseData?.metadata?.monetary_amount ? 
                            (caseData.metadata.monetary_amount > 1000000 ? 'HIGH' : 
                             caseData.metadata.monetary_amount > 100000 ? 'MEDIUM' : 'LOW') : 'UNKNOWN'}
                        </p>
                        <p className="text-xs text-red-700 mt-1">
                          Based on monetary amount involved
                        </p>
                      </div>

                      {/* Interest Rate (if applicable) */}
                      <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                        <div className="flex items-center space-x-2 mb-2">
                          <Percent className="w-5 h-5 text-blue-600" />
                          <span className="text-sm font-medium text-blue-800 uppercase tracking-wide">Interest Rate</span>
                        </div>
                        <p className="text-lg font-bold text-blue-900">
                          {caseData?.metadata?.interest_rate ? `${caseData.metadata.interest_rate}%` : 'N/A'}
                        </p>
                        <p className="text-xs text-blue-700 mt-1">
                          Applicable interest rate for financial calculations
                        </p>
                      </div>

                    </div>
                  </div>

                  {/* Subject Matter Grid */}
                  <div className="space-y-6">
                    <div className="flex items-center space-x-2 mb-4">
                      <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                      <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">Subject Matter</h3>
                    </div>
                    
                    <div className="space-y-4">
                      {/* Subject Matter */}
                      <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                        <div className="flex items-center space-x-2 mb-2">
                          <BookOpen className="w-5 h-5 text-blue-600" />
                          <span className="text-sm font-medium text-blue-800 uppercase tracking-wide">Subject Matter</span>
                        </div>
                        <p className="text-sm font-semibold text-blue-900">
                          {caseData?.subject_matter || caseData?.metadata?.subject_matter || 'N/A'}
                        </p>
                      </div>


                      {/* Legal Issues */}
                      <div className="bg-orange-50 p-4 rounded-lg border-l-4 border-orange-500">
                        <div className="flex items-center space-x-2 mb-2">
                          <Scale className="w-5 h-5 text-orange-600" />
                          <span className="text-sm font-medium text-orange-800 uppercase tracking-wide">Legal Issues</span>
                        </div>
                        <div className="text-sm text-orange-900">
                          {caseData?.metadata?.legal_issues && formatArray(caseData.metadata.legal_issues).length > 0 ? (
                            <div className="space-y-1">
                              {formatArray(caseData.metadata.legal_issues).map((issue, index) => (
                                <div key={index} className="px-2 py-1 bg-orange-100 rounded text-xs">
                                  {issue}
                                </div>
                              ))}
                            </div>
                          ) : (
                            <span className="text-gray-500">No specific legal issues identified</span>
                          )}
                        </div>
                      </div>

                      {/* Financial Terms */}
                      <div className="bg-teal-50 p-4 rounded-lg border-l-4 border-teal-500">
                        <div className="flex items-center space-x-2 mb-2">
                          <Calculator className="w-5 h-5 text-teal-600" />
                          <span className="text-sm font-medium text-teal-800 uppercase tracking-wide">Financial Terms</span>
                        </div>
                        <div className="text-sm text-teal-900">
                          {caseData?.metadata?.financial_terms && formatArray(caseData.metadata.financial_terms).length > 0 ? (
                            <div className="space-y-1">
                              {formatArray(caseData.metadata.financial_terms).map((term, index) => (
                                <div key={index} className="px-2 py-1 bg-teal-100 rounded text-xs">
                                  {term}
                                </div>
                              ))}
                            </div>
                          ) : (
                            <span className="text-gray-500">No specific financial terms identified</span>
                          )}
                        </div>
                      </div>

                      {/* Board Resolution */}
                      <div className="bg-gray-50 p-4 rounded-lg border-l-4 border-gray-500">
                        <div className="flex items-center space-x-2 mb-2">
                          <FileText className="w-5 h-5 text-gray-600" />
                          <span className="text-sm font-medium text-gray-800 uppercase tracking-wide">Board Resolution</span>
                        </div>
                        <p className="text-sm text-gray-900">
                          {caseData?.board_resolution || caseData?.metadata?.board_resolution || 'N/A'}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Standalone Fields */}
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                
                {/* Outcome */}
                <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                  <div className="flex items-center space-x-2 mb-1">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span className="text-xs font-medium text-green-800 uppercase tracking-wide">Outcome</span>
                  </div>
                  <p className="text-sm font-semibold text-green-900">
                    {caseData?.metadata?.outcome || 'Unknown'}
                  </p>
                </div>

                {/* Relevance Score */}
                <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                  <div className="flex items-center space-x-2 mb-1">
                    <Tag className="w-4 h-4 text-blue-600" />
                    <span className="text-xs font-medium text-blue-800 uppercase tracking-wide">Relevance Score</span>
                  </div>
                  <p className="text-sm font-semibold text-blue-900">
                    {caseData?.metadata?.relevance_score ? caseData.metadata.relevance_score.toFixed(2) : 'N/A'}
                  </p>
                </div>

                {/* Processed */}
                <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                  <div className="flex items-center space-x-2 mb-1">
                    <CheckCircle className="w-4 h-4 text-purple-600" />
                    <span className="text-xs font-medium text-purple-800 uppercase tracking-wide">Processed</span>
                  </div>
                  <p className="text-sm font-semibold text-purple-900">
                    {caseData?.metadata?.is_processed ? 'Yes' : 'No'}
                  </p>
                </div>

                {/* Processed At */}
                <div className="bg-orange-50 p-4 rounded-lg border-l-4 border-orange-500">
                  <div className="flex items-center space-x-2 mb-1">
                    <Calendar className="w-4 h-4 text-orange-600" />
                    <span className="text-xs font-medium text-orange-800 uppercase tracking-wide">Processed At</span>
                  </div>
                  <p className="text-sm font-semibold text-orange-900">
                    {caseData?.metadata?.processed_at ? formatDate(caseData.metadata.processed_at) : 'N/A'}
                  </p>
                </div>

              </div>
            </div>
          </div>

          {/* Conclusion of the Court */}
          <div className="bg-white rounded-lg shadow-sm border">
            <SectionHeader
              title="Conclusion of the Court"
              icon={Gavel}
              isExpanded={expandedSections.conclusion}
              onToggle={() => toggleSection('conclusion')}
            />
            {expandedSections.conclusion && (
              <div className="p-6">
                <div className="space-y-4">
                  <div className="bg-amber-50 p-6 rounded-lg border-l-4 border-amber-500">
                    <div className="flex items-center space-x-2 mb-3">
                      <Gavel className="w-5 h-5 text-amber-600" />
                      <span className="text-sm font-semibold text-amber-800 uppercase tracking-wide">Court's Conclusion</span>
                    </div>
                    <div className="prose prose-sm max-w-none">
                      <div 
                        className="text-gray-900 leading-relaxed"
                        dangerouslySetInnerHTML={{
                          __html: caseData?.conclusion || caseData?.court_order || caseData?.final_orders || 'No conclusion available'
                        }}
                      />
                    </div>
                  </div>
                  
                  {caseData?.board_resolution && (
                    <div className="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-500">
                      <div className="flex items-center space-x-2 mb-3">
                        <FileText className="w-5 h-5 text-blue-600" />
                        <span className="text-sm font-semibold text-blue-800 uppercase tracking-wide">Board Resolution</span>
                      </div>
                      <div className="prose prose-sm max-w-none">
                        <div 
                          className="text-gray-900 leading-relaxed"
                          dangerouslySetInnerHTML={{
                            __html: caseData.board_resolution
                          }}
                        />
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Case Documents */}
          <div className="bg-white rounded-lg shadow-sm border">
            <SectionHeader
              title="Case Documents"
              icon={FileText}
              isExpanded={expandedSections.caseDocuments}
              onToggle={() => toggleSection('caseDocuments')}
            />
            {expandedSections.caseDocuments && (
              <div className="p-6">
                <div className="space-y-4">
                  <div className="bg-gray-50 p-6 rounded-lg">
                    <div className="flex items-center space-x-2 mb-4">
                      <FileText className="w-5 h-5 text-gray-600" />
                      <span className="text-sm font-semibold text-gray-800 uppercase tracking-wide">Available Documents</span>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {/* Main Case Document */}
                      <div className="bg-white p-4 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors duration-200">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                            <FileText className="w-5 h-5 text-blue-600" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-gray-900 truncate">Case Judgment</p>
                            <p className="text-xs text-gray-500">PDF Document</p>
                          </div>
                        </div>
                        <div className="mt-3 flex space-x-2">
                          <button className="flex-1 inline-flex items-center justify-center space-x-1 px-3 py-1.5 bg-blue-600 text-white text-xs font-medium rounded-lg hover:bg-blue-700 transition-colors duration-200">
                            <Eye className="w-3 h-3" />
                            <span>View</span>
                          </button>
                          <button className="flex-1 inline-flex items-center justify-center space-x-1 px-3 py-1.5 bg-gray-600 text-white text-xs font-medium rounded-lg hover:bg-gray-700 transition-colors duration-200">
                            <Download className="w-3 h-3" />
                            <span>Download</span>
                          </button>
                        </div>
                      </div>

                      {/* Court Order Document */}
                      {caseData?.court_order && (
                        <div className="bg-white p-4 rounded-lg border border-gray-200 hover:border-green-300 transition-colors duration-200">
                          <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                              <Gavel className="w-5 h-5 text-green-600" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium text-gray-900 truncate">Court Order</p>
                              <p className="text-xs text-gray-500">PDF Document</p>
                            </div>
                          </div>
                          <div className="mt-3 flex space-x-2">
                            <button className="flex-1 inline-flex items-center justify-center space-x-1 px-3 py-1.5 bg-green-600 text-white text-xs font-medium rounded-lg hover:bg-green-700 transition-colors duration-200">
                              <Eye className="w-3 h-3" />
                              <span>View</span>
                            </button>
                            <button className="flex-1 inline-flex items-center justify-center space-x-1 px-3 py-1.5 bg-gray-600 text-white text-xs font-medium rounded-lg hover:bg-gray-700 transition-colors duration-200">
                              <Download className="w-3 h-3" />
                              <span>Download</span>
                            </button>
                          </div>
                        </div>
                      )}

                      {/* Board Resolution Document */}
                      {caseData?.board_resolution && (
                        <div className="bg-white p-4 rounded-lg border border-gray-200 hover:border-purple-300 transition-colors duration-200">
                          <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                              <FileText className="w-5 h-5 text-purple-600" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium text-gray-900 truncate">Board Resolution</p>
                              <p className="text-xs text-gray-500">PDF Document</p>
                            </div>
                          </div>
                          <div className="mt-3 flex space-x-2">
                            <button className="flex-1 inline-flex items-center justify-center space-x-1 px-3 py-1.5 bg-purple-600 text-white text-xs font-medium rounded-lg hover:bg-purple-700 transition-colors duration-200">
                              <Eye className="w-3 h-3" />
                              <span>View</span>
                            </button>
                            <button className="flex-1 inline-flex items-center justify-center space-x-1 px-3 py-1.5 bg-gray-600 text-white text-xs font-medium rounded-lg hover:bg-gray-700 transition-colors duration-200">
                              <Download className="w-3 h-3" />
                              <span>Download</span>
                            </button>
                          </div>
                        </div>
                      )}

                      {/* Additional Documents Placeholder */}
                      <div className="bg-white p-4 rounded-lg border border-gray-200 hover:border-orange-300 transition-colors duration-200">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                            <FileText className="w-5 h-5 text-orange-600" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-gray-900 truncate">Supporting Documents</p>
                            <p className="text-xs text-gray-500">Multiple Files</p>
                          </div>
                        </div>
                        <div className="mt-3 flex space-x-2">
                          <button className="flex-1 inline-flex items-center justify-center space-x-1 px-3 py-1.5 bg-orange-600 text-white text-xs font-medium rounded-lg hover:bg-orange-700 transition-colors duration-200">
                            <Eye className="w-3 h-3" />
                            <span>View All</span>
                          </button>
                          <button className="flex-1 inline-flex items-center justify-center space-x-1 px-3 py-1.5 bg-gray-600 text-white text-xs font-medium rounded-lg hover:bg-gray-700 transition-colors duration-200">
                            <Download className="w-3 h-3" />
                            <span>Download</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Full Case Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          {/* Backdrop */}
          <div 
            className="fixed inset-0 bg-black bg-opacity-50 transition-opacity duration-300"
            onClick={() => setIsModalOpen(false)}
          />
          
          {/* Modal */}
          <div className="flex min-h-full items-center justify-center p-4">
            <div className="relative bg-white rounded-lg shadow-xl max-w-6xl w-full max-h-[90vh] flex flex-col animate-in fade-in-0 zoom-in-95 duration-300">
              {/* Modal Header */}
              <div className="flex items-center justify-between p-6 border-b border-gray-200">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                    <FileText className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">Full Case Content</h3>
                    <p className="text-sm text-gray-500 break-words leading-tight">
                      {caseData?.title || 'Case Details'}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => setIsModalOpen(false)}
                  className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors duration-200"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              {/* Modal Content */}
              <div className="flex-1 overflow-y-auto p-6">
                <div className="prose prose-lg max-w-none">
                  <div 
                    className="text-gray-900 leading-relaxed"
                    dangerouslySetInnerHTML={{
                      __html: caseData?.summernote_content || caseData?.summernote || caseData?.summarnote || caseData?.metadata?.case_summary || caseData?.case_summary || 'No case content available'
                    }}
                  />
                </div>
              </div>

              {/* Modal Footer */}
              <div className="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
                <div className="flex items-center space-x-2 text-sm text-gray-500">
                  <Clock className="w-4 h-4" />
                  <span>Last updated: {caseData?.updated_at ? formatDate(caseData.updated_at) : 'N/A'}</span>
                </div>
                <div className="flex items-center space-x-3">
                  <button
                    onClick={() => {
                      const content = caseData?.summernote_content || caseData?.summernote || caseData?.summarnote || caseData?.metadata?.case_summary || caseData?.case_summary || '';
                      navigator.clipboard.writeText(content.replace(/<[^>]*>/g, ''));
                    }}
                    className="inline-flex items-center space-x-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200"
                  >
                    <Copy className="w-4 h-4" />
                    <span>Copy Text</span>
                  </button>
                  <button
                    onClick={() => setIsModalOpen(false)}
                    className="inline-flex items-center space-x-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                  >
                    <X className="w-4 h-4" />
                    <span>Close</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CaseDetails;
