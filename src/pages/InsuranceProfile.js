import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { 
  Shield, 
  MapPin, 
  Phone, 
  Mail, 
  Globe, 
  Calendar, 
  Users, 
  TrendingUp, 
  Scale, 
  FileText, 
  ExternalLink,
  ArrowLeft,
  ChevronDown,
  ChevronUp,
  Briefcase,
  Award,
  Clock,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Building2
} from 'lucide-react';

const InsuranceProfile = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const [insuranceData, setInsuranceData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedSections, setExpandedSections] = useState({
    overview: true,
    contact: true,
    management: true,
    cases: true,
    analytics: true
  });

  const searchQuery = new URLSearchParams(location.search).get('q') || '';

  useEffect(() => {
    if (id) {
      loadInsuranceData();
    } else {
      setError('No insurance company ID provided');
      setLoading(false);
    }
  }, [id]);

  const loadInsuranceData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('accessToken');
      
      if (!token) {
        setError('Authentication required');
        setLoading(false);
        return;
      }

      const response = await fetch(`http://localhost:8000/api/insurance/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Insurance data loaded:', data);
        setInsuranceData(data);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to load insurance data');
      }
    } catch (err) {
      setError('Network error. Please try again.');
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
      return 'N/A';
    }
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

  const formatArray = (array) => {
    if (!array) return [];
    if (Array.isArray(array)) return array;
    if (typeof array === 'string') return array.split(',').map(item => item.trim());
    return [];
  };

  const InfoRow = ({ label, value, icon: Icon }) => (
    <div className="flex items-center justify-between py-2">
      <div className="flex items-center space-x-2">
        <Icon className="w-4 h-4 text-gray-500" />
        <span className="text-sm font-medium text-gray-700">{label}</span>
      </div>
      <span className="text-sm text-gray-900">{value || 'N/A'}</span>
    </div>
  );

  const ArrayDisplay = ({ label, items, icon: Icon }) => (
    <div className="py-2">
      <div className="flex items-center space-x-2 mb-2">
        <Icon className="w-4 h-4 text-gray-500" />
        <span className="text-sm font-medium text-gray-700">{label}</span>
      </div>
      <div className="space-y-1">
        {items.map((item, index) => (
          <div key={index} className="text-sm text-gray-900 bg-gray-50 px-3 py-1 rounded">
            {item}
          </div>
        ))}
      </div>
    </div>
  );

  const SectionHeader = ({ title, icon: Icon, isExpanded, onToggle }) => (
    <button
      onClick={onToggle}
      className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 transition-colors"
    >
      <div className="flex items-center space-x-2">
        <Icon className="w-5 h-5 text-gray-600" />
        <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
      </div>
      {isExpanded ? (
        <ChevronUp className="w-5 h-5 text-gray-400" />
      ) : (
        <ChevronDown className="w-5 h-5 text-gray-400" />
      )}
    </button>
  );

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-sky-600 mx-auto"></div>
          <p className="mt-4 text-slate-600">Loading insurance company profile...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 mb-4">
            <AlertTriangle className="h-16 w-16 mx-auto mb-4" />
            <h2 className="text-2xl font-bold">Error Loading Insurance Company</h2>
            <p className="text-gray-600 mt-2">{error}</p>
          </div>
          <button
            onClick={() => navigate('/insurance')}
            className="bg-sky-600 text-white px-6 py-2 rounded-lg hover:bg-sky-700 transition-colors"
          >
            Back to Insurance Companies
          </button>
        </div>
      </div>
    );
  }

  if (!insuranceData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-600 mb-4">
            <Shield className="h-16 w-16 mx-auto mb-4" />
            <h2 className="text-2xl font-bold">Insurance Company Not Found</h2>
            <p className="text-gray-600 mt-2">The requested insurance company could not be found</p>
          </div>
          <button
            onClick={() => navigate('/insurance')}
            className="bg-sky-600 text-white px-6 py-2 rounded-lg hover:bg-sky-700 transition-colors"
          >
            Back to Insurance Companies
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/insurance')}
                className="flex items-center text-gray-600 hover:text-gray-900"
              >
                <ArrowLeft className="h-5 w-5 mr-1" />
                Back to Insurance Companies
              </button>
              <div className="h-8 w-px bg-gray-300"></div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{insuranceData.name}</h1>
                <p className="text-gray-600 mt-1">
                  {insuranceData.insurance_type && `${insuranceData.insurance_type} • `}
                  Insurance Company
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <FileText className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Cases</p>
                <p className="text-2xl font-bold text-gray-900">0</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Resolved Cases</p>
                <p className="text-2xl font-bold text-gray-900">0</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <Clock className="w-6 h-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Cases</p>
                <p className="text-2xl font-bold text-gray-900">0</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Award className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Risk Level</p>
                <p className="text-2xl font-bold text-gray-900">Low</p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* Company Overview */}
            <div className="bg-white rounded-lg shadow-sm border">
              <SectionHeader
                title="Company Overview"
                icon={Shield}
                isExpanded={expandedSections.overview}
                onToggle={() => toggleSection('overview')}
              />
              {expandedSections.overview && (
                <div className="p-6 border-t border-gray-200 space-y-4">
                  <InfoRow label="Company Name" value={insuranceData.name} icon={Shield} />
                  <InfoRow label="Insurance Type" value={insuranceData.insurance_type} icon={Shield} />
                  <InfoRow label="License Number" value={insuranceData.license_number} icon={FileText} />
                  <InfoRow label="Registration Number" value={insuranceData.registration_number} icon={FileText} />
                  <InfoRow label="Established" value={formatDate(insuranceData.established_date)} icon={Calendar} />
                  <InfoRow label="Parent Company" value={insuranceData.parent_company} icon={Building2} />
                  <InfoRow label="CEO/MD" value={insuranceData.ceo_name} icon={Users} />
                  
                  {insuranceData.description && (
                    <div className="pt-4 border-t border-gray-200">
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Description</h4>
                      <p className="text-sm text-gray-900">{insuranceData.description}</p>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Contact Information */}
            <div className="bg-white rounded-lg shadow-sm border">
              <SectionHeader
                title="Contact Information"
                icon={Phone}
                isExpanded={expandedSections.contact}
                onToggle={() => toggleSection('contact')}
              />
              {expandedSections.contact && (
                <div className="p-6 border-t border-gray-200 space-y-4">
                  <InfoRow label="Phone" value={insuranceData.phone} icon={Phone} />
                  <InfoRow label="Email" value={insuranceData.email} icon={Mail} />
                  <InfoRow label="Website" value={insuranceData.website} icon={Globe} />
                  <InfoRow label="Address" value={insuranceData.address} icon={MapPin} />
                  <InfoRow label="City" value={insuranceData.city} icon={MapPin} />
                  <InfoRow label="Region" value={insuranceData.region} icon={MapPin} />
                  <InfoRow label="Postal Code" value={insuranceData.postal_code} icon={MapPin} />
                </div>
              )}
            </div>

            {/* Management & Key Personnel */}
            <div className="bg-white rounded-lg shadow-sm border">
              <SectionHeader
                title="Management & Key Personnel"
                icon={Users}
                isExpanded={expandedSections.management}
                onToggle={() => toggleSection('management')}
              />
              {expandedSections.management && (
                <div className="p-6 border-t border-gray-200 space-y-4">
                  <ArrayDisplay 
                    label="Board of Directors" 
                    items={formatArray(insuranceData.board_directors)} 
                    icon={Users} 
                  />
                  <ArrayDisplay 
                    label="Senior Management" 
                    items={formatArray(insuranceData.senior_management)} 
                    icon={Users} 
                  />
                  <ArrayDisplay 
                    label="Key Personnel" 
                    items={formatArray(insuranceData.key_personnel)} 
                    icon={Users} 
                  />
                  <InfoRow label="Employee Count" value={insuranceData.employee_count} icon={Users} />
                  <InfoRow label="Assets Under Management" value={formatCurrency(insuranceData.assets_under_management)} icon={TrendingUp} />
                  <InfoRow label="Annual Premium Income" value={formatCurrency(insuranceData.annual_premium_income)} icon={TrendingUp} />
                </div>
              )}
            </div>

            {/* Insurance Products */}
            {insuranceData.insurance_products && formatArray(insuranceData.insurance_products).length > 0 && (
              <div className="bg-white rounded-lg shadow-sm border">
                <SectionHeader
                  title="Insurance Products"
                  icon={Shield}
                  isExpanded={expandedSections.products}
                  onToggle={() => toggleSection('products')}
                />
                {expandedSections.products && (
                  <div className="p-6 border-t border-gray-200">
                    <ArrayDisplay 
                      label="Products Offered" 
                      items={formatArray(insuranceData.insurance_products)} 
                      icon={Shield} 
                    />
                  </div>
                )}
              </div>
            )}

            {/* Legal Cases */}
            <div className="bg-white rounded-lg shadow-sm border">
              <SectionHeader
                title="Legal Cases"
                icon={Scale}
                isExpanded={expandedSections.cases}
                onToggle={() => toggleSection('cases')}
              />
              {expandedSections.cases && (
                <div className="p-6 border-t border-gray-200">
                  <div className="text-center py-8">
                    <Scale className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No Cases Found</h3>
                    <p className="text-gray-600">This insurance company has no legal cases in the database</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right Column - Analytics */}
          <div className="space-y-6">
            {/* Analytics */}
            <div className="bg-white rounded-lg shadow-sm border">
              <SectionHeader
                title="Analytics"
                icon={TrendingUp}
                isExpanded={expandedSections.analytics}
                onToggle={() => toggleSection('analytics')}
              />
              {expandedSections.analytics && (
                <div className="p-6 border-t border-gray-200 space-y-4">
                  <div className="text-center py-8">
                    <TrendingUp className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No Analytics Available</h3>
                    <p className="text-gray-600">Analytics will be available once cases are added</p>
                  </div>
                </div>
              )}
            </div>

            {/* Company Status */}
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Company Status</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">License Status</span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    insuranceData.license_status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {insuranceData.license_status || 'Unknown'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Last Updated</span>
                  <span className="text-sm text-gray-900">{formatDate(insuranceData.updated_at)}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Created</span>
                  <span className="text-sm text-gray-900">{formatDate(insuranceData.created_at)}</span>
                </div>
              </div>
            </div>

            {/* Regulatory Information */}
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Regulatory Information</h3>
              <div className="space-y-3">
                <InfoRow label="Regulatory Body" value={insuranceData.regulatory_body} icon={Shield} />
                <InfoRow label="License Expiry" value={formatDate(insuranceData.license_expiry_date)} icon={Calendar} />
                <InfoRow label="Compliance Rating" value={insuranceData.compliance_rating} icon={Award} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InsuranceProfile;
