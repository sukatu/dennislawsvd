import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, Building2, MapPin, Phone, Mail, Globe, Users, 
  TrendingUp, Award, Star, Clock, Eye, EyeOff, AlertCircle, 
  ExternalLink, Download, FileText, Briefcase, DollarSign, 
  User, Calendar, Hash, CreditCard, Share2, Building, 
  UserCheck, FileCheck, PieChart, Link, ChevronDown, ChevronUp
} from 'lucide-react';

const CompanyProfile = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [companyData, setCompanyData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedSections, setExpandedSections] = useState({
    basicInfo: true,
    directors: true,
    secretary: true,
    auditor: true,
    capitalDetails: true,
    shareholders: true,
    linkedCompanies: true
  });

  // Load company data
  useEffect(() => {
    const loadCompanyData = async () => {
      if (!id) {
        setError('Company ID not provided');
        setIsLoading(false);
        return;
      }

      try {
        const token = localStorage.getItem('accessToken') || 'test-token-123';
        const response = await fetch(`http://localhost:8000/api/companies/${id}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          setCompanyData(data);
        } else {
          const errorData = await response.json();
          setError(errorData.detail || 'Failed to load company data');
        }
      } catch (err) {
        setError('Network error. Please try again.');
        console.error('Error loading company data:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadCompanyData();
  }, [id]);

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleDateString('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
    } catch {
      return 'N/A';
    }
  };

  const formatCurrency = (amount) => {
    if (!amount) return 'N/A';
    return new Intl.NumberFormat('en-GH', {
      style: 'currency',
      currency: 'GHS'
    }).format(amount);
  };

  const formatNumber = (number) => {
    if (!number) return 'N/A';
    return new Intl.NumberFormat('en-GH').format(number);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading company profile...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Company</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => navigate('/companies')}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Back to Companies
          </button>
        </div>
      </div>
    );
  }

  if (!companyData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Building2 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Company Not Found</h2>
          <p className="text-gray-600 mb-4">The requested company could not be found.</p>
          <button
            onClick={() => navigate('/companies')}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Back to Companies
          </button>
        </div>
      </div>
    );
  }

  const SectionHeader = ({ title, icon: Icon, isExpanded, onToggle, count }) => (
    <button
      onClick={onToggle}
      className="w-full flex items-center justify-between p-4 bg-white border-b border-gray-200 hover:bg-gray-50 transition-colors"
    >
      <div className="flex items-center space-x-3">
        <Icon className="h-5 w-5 text-blue-600" />
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        {count !== undefined && (
          <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded-full">
            {count}
          </span>
        )}
      </div>
      {isExpanded ? (
        <ChevronUp className="h-5 w-5 text-gray-400" />
      ) : (
        <ChevronDown className="h-5 w-5 text-gray-400" />
      )}
    </button>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-4">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/companies')}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ArrowLeft className="h-5 w-5 text-gray-600" />
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{companyData.name}</h1>
                <p className="text-gray-600">{companyData.type_of_company || 'Company'}</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2">
                <Download className="h-4 w-4" />
                <span>Export Profile</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Basic Information */}
            <div className="bg-white rounded-lg shadow-sm border">
              <SectionHeader
                title="Basic Information"
                icon={Building2}
                isExpanded={expandedSections.basicInfo}
                onToggle={() => toggleSection('basicInfo')}
              />
              {expandedSections.basicInfo && (
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Company Name</label>
                      <p className="text-gray-900 font-medium">{companyData.name}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Type of Company</label>
                      <p className="text-gray-900">{companyData.type_of_company || 'N/A'}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                      <p className="text-gray-900">{companyData.address || 'N/A'}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">District</label>
                      <p className="text-gray-900">{companyData.district || 'N/A'}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Region</label>
                      <p className="text-gray-900">{companyData.region || 'N/A'}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Date of Incorporation</label>
                      <p className="text-gray-900">{formatDate(companyData.date_of_incorporation)}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Date of Commencement</label>
                      <p className="text-gray-900">{formatDate(companyData.date_of_commencement)}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Nature of Business</label>
                      <p className="text-gray-900">{companyData.nature_of_business || 'N/A'}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Registration Number</label>
                      <p className="text-gray-900 font-mono">{companyData.registration_number || 'N/A'}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Tax Identification Number</label>
                      <p className="text-gray-900 font-mono">{companyData.tax_identification_number || 'N/A'}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                      <p className="text-gray-900">{companyData.phone_number || 'N/A'}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                      <p className="text-gray-900">{companyData.email || 'N/A'}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Directors */}
            <div className="bg-white rounded-lg shadow-sm border">
              <SectionHeader
                title="Directors"
                icon={Users}
                isExpanded={expandedSections.directors}
                onToggle={() => toggleSection('directors')}
                count={companyData.directors?.length || 0}
              />
              {expandedSections.directors && (
                <div className="p-6">
                  {companyData.directors && companyData.directors.length > 0 ? (
                    <div className="space-y-4">
                      {companyData.directors.map((director, index) => (
                        <div key={index} className="border border-gray-200 rounded-lg p-4">
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                              <p className="text-gray-900 font-medium">{director.name}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Nationality</label>
                              <p className="text-gray-900">{director.nationality}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                              <p className="text-gray-900">{director.address}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Occupation</label>
                              <p className="text-gray-900">{director.occupation}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                              <p className="text-gray-900">{director.email}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Contact</label>
                              <p className="text-gray-900">{director.contact}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Tax ID</label>
                              <p className="text-gray-900 font-mono">{director.tax_identification_number}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Other Directorship</label>
                              <p className="text-gray-900">
                                {director.other_directorship && director.other_directorship.length > 0 
                                  ? director.other_directorship.join(', ') 
                                  : 'None'}
                              </p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500 text-center py-4">No directors information available</p>
                  )}
                </div>
              )}
            </div>

            {/* Secretary */}
            <div className="bg-white rounded-lg shadow-sm border">
              <SectionHeader
                title="Secretary"
                icon={FileCheck}
                isExpanded={expandedSections.secretary}
                onToggle={() => toggleSection('secretary')}
              />
              {expandedSections.secretary && (
                <div className="p-6">
                  {companyData.secretary ? (
                    <div className="border border-gray-200 rounded-lg p-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                          <p className="text-gray-900 font-medium">{companyData.secretary.name}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Nationality</label>
                          <p className="text-gray-900">{companyData.secretary.nationality}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                          <p className="text-gray-900">{companyData.secretary.address}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Occupation</label>
                          <p className="text-gray-900">{companyData.secretary.occupation}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                          <p className="text-gray-900">{companyData.secretary.email}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Contact</label>
                          <p className="text-gray-900">{companyData.secretary.contact}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Tax ID</label>
                          <p className="text-gray-900 font-mono">{companyData.secretary.tax_identification_number}</p>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <p className="text-gray-500 text-center py-4">No secretary information available</p>
                  )}
                </div>
              )}
            </div>

            {/* Auditor */}
            <div className="bg-white rounded-lg shadow-sm border">
              <SectionHeader
                title="Auditor"
                icon={Award}
                isExpanded={expandedSections.auditor}
                onToggle={() => toggleSection('auditor')}
              />
              {expandedSections.auditor && (
                <div className="p-6">
                  {companyData.auditor ? (
                    <div className="border border-gray-200 rounded-lg p-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                          <p className="text-gray-900 font-medium">{companyData.auditor.name}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Nationality</label>
                          <p className="text-gray-900">{companyData.auditor.nationality}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                          <p className="text-gray-900">{companyData.auditor.address}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Occupation</label>
                          <p className="text-gray-900">{companyData.auditor.occupation}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                          <p className="text-gray-900">{companyData.auditor.email}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Contact</label>
                          <p className="text-gray-900">{companyData.auditor.contact}</p>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Tax ID</label>
                          <p className="text-gray-900 font-mono">{companyData.auditor.tax_identification_number}</p>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <p className="text-gray-500 text-center py-4">No auditor information available</p>
                  )}
                </div>
              )}
            </div>

            {/* Capital Details */}
            <div className="bg-white rounded-lg shadow-sm border">
              <SectionHeader
                title="Capital Details"
                icon={DollarSign}
                isExpanded={expandedSections.capitalDetails}
                onToggle={() => toggleSection('capitalDetails')}
              />
              {expandedSections.capitalDetails && (
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Authorized Shares</label>
                      <p className="text-gray-900 font-mono text-lg">{formatNumber(companyData.authorized_shares)}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Stated Capital</label>
                      <p className="text-gray-900 font-mono text-lg">{formatCurrency(companyData.stated_capital)}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Shareholders */}
            <div className="bg-white rounded-lg shadow-sm border">
              <SectionHeader
                title="Shareholders"
                icon={PieChart}
                isExpanded={expandedSections.shareholders}
                onToggle={() => toggleSection('shareholders')}
                count={companyData.shareholders?.length || 0}
              />
              {expandedSections.shareholders && (
                <div className="p-6">
                  {companyData.shareholders && companyData.shareholders.length > 0 ? (
                    <div className="space-y-4">
                      {companyData.shareholders.map((shareholder, index) => (
                        <div key={index} className="border border-gray-200 rounded-lg p-4">
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                              <p className="text-gray-900 font-medium">{shareholder.name}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Nationality</label>
                              <p className="text-gray-900">{shareholder.nationality}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                              <p className="text-gray-900">{shareholder.address}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Occupation</label>
                              <p className="text-gray-900">{shareholder.occupation || 'N/A'}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                              <p className="text-gray-900">{shareholder.email}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Contact</label>
                              <p className="text-gray-900">{shareholder.contact}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Tax ID</label>
                              <p className="text-gray-900 font-mono">{shareholder.tax_identification_number}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Shares Alloted</label>
                              <p className="text-gray-900 font-mono">{formatNumber(shareholder.shares_alloted)}</p>
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Consideration Payable</label>
                              <p className="text-gray-900">{shareholder.consideration_payable}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500 text-center py-4">No shareholders information available</p>
                  )}
                </div>
              )}
            </div>

            {/* Other Linked Companies */}
            <div className="bg-white rounded-lg shadow-sm border">
              <SectionHeader
                title="Other Linked Companies"
                icon={Link}
                isExpanded={expandedSections.linkedCompanies}
                onToggle={() => toggleSection('linkedCompanies')}
                count={companyData.other_linked_companies?.length || 0}
              />
              {expandedSections.linkedCompanies && (
                <div className="p-6">
                  {companyData.other_linked_companies && companyData.other_linked_companies.length > 0 ? (
                    <div className="space-y-2">
                      {companyData.other_linked_companies.map((company, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                          <span className="text-gray-900 font-medium">{company}</span>
                          <button className="text-blue-600 hover:text-blue-800">
                            <ExternalLink className="h-4 w-4" />
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500 text-center py-4">No linked companies information available</p>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center justify-center space-x-2">
                  <Download className="h-4 w-4" />
                  <span>Export Profile</span>
                </button>
                <button className="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center justify-center space-x-2">
                  <FileText className="h-4 w-4" />
                  <span>Generate Report</span>
                </button>
                <button className="w-full bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 flex items-center justify-center space-x-2">
                  <Share2 className="h-4 w-4" />
                  <span>Share Profile</span>
                </button>
              </div>
            </div>

            {/* Company Status */}
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Company Status</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Status</span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    companyData.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {companyData.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Verified</span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    companyData.is_verified ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {companyData.is_verified ? 'Verified' : 'Unverified'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Search Count</span>
                  <span className="text-gray-900 font-medium">{companyData.search_count || 0}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CompanyProfile;
