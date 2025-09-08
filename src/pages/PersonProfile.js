import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Download, Star, User, Calendar, MapPin, Mail } from 'lucide-react';

const PersonProfile = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [personData, setPersonData] = useState(null);

  // Mock data - in real app, this would come from API
  const mockPersonData = {
    id: 1,
    name: 'Albert Kweku Obeng',
    dob: '7 March 1962',
    dod: '9 March 2004',
    idNumber: 'KL1K-DXP',
    gender: 'Male',
    nationality: 'Ghanaian',
    riskLevel: 'Low',
    riskScore: 25,
    totalCases: 5,
    resolvedCases: 4,
    pendingCases: 1,
    favorableOutcomes: 3,
    cases: [
      {
        id: 1,
        title: 'Property Dispute Case',
        caseNumber: 'GJ/123/2003',
        status: 'Resolved',
        date: '2003-2004',
        type: 'Property Dispute',
        outcome: 'Favorable',
        court: 'High Court, Accra',
        judge: 'Justice Sarah Mensah'
      },
      {
        id: 2,
        title: 'Family Law Matter',
        caseNumber: 'GJ/456/2002',
        status: 'Resolved',
        date: '2002-2003',
        type: 'Family Law',
        outcome: 'Favorable',
        court: 'Family Court, Kumasi',
        judge: 'Justice Kwame Nkrumah'
      },
      {
        id: 3,
        title: 'Contract Dispute with ABC Bank',
        caseNumber: 'GJ/789/2001',
        status: 'Resolved',
        date: '2001-2002',
        type: 'Commercial Law',
        outcome: 'Unfavorable',
        court: 'Commercial Court, Accra',
        judge: 'Justice Ama Serwaa'
      },
      {
        id: 4,
        title: 'Insurance Claim Dispute',
        caseNumber: 'GJ/101/2000',
        status: 'Resolved',
        date: '2000-2001',
        type: 'Insurance Law',
        outcome: 'Favorable',
        court: 'High Court, Accra',
        judge: 'Justice Kofi Annan'
      },
      {
        id: 5,
        title: 'Employment Dispute',
        caseNumber: 'GJ/202/2004',
        status: 'Pending',
        date: '2004-Present',
        type: 'Labor Law',
        outcome: 'Pending',
        court: 'Labor Court, Accra',
        judge: 'Justice Nana Addo'
      }
    ],
    caseDetails: [
      {
        title: 'Property Dispute vs. Estate of John Doe',
        description: 'This case involved a property dispute between Albert Kweku Obeng and the estate of John Doe. The dispute centered around the ownership of a residential property in Accra. The case was resolved in favor of Mr. Obeng, with the court ruling that he had legitimate claim to the property based on inheritance documents.',
        judge: 'Justice Sarah Mensah',
        court: 'High Court, Accra',
        lawyer: 'Kwame Asante',
        outcome: 'Favorable'
      },
      {
        title: 'Contract Dispute with ABC Bank',
        description: 'A commercial dispute involving loan repayment terms and interest calculations. The bank claimed default on a business loan, while Mr. Obeng argued that the interest rates were unfairly applied. The court ruled in favor of the bank.',
        judge: 'Justice Ama Serwaa',
        court: 'Commercial Court, Accra',
        lawyer: 'Ama Serwaa',
        outcome: 'Unfavorable'
      }
    ],
    relatedPeople: [
      { name: 'John Doe', role: 'Estate Representative' },
      { name: 'Kwame Asante', role: 'Legal Counsel' },
      { name: 'ABC Bank Ltd', role: 'Opposing Party' },
      { name: 'XYZ Insurance Co.', role: 'Insurance Provider' }
    ]
  };

  useEffect(() => {
    const personId = searchParams.get('id');
    if (personId) {
      // In real app, fetch person data by ID
      setPersonData(mockPersonData);
    }
  }, [searchParams]);

  if (!personData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-sky-600 mx-auto"></div>
          <p className="mt-4 text-slate-600">Loading profile...</p>
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
    <div>
      {/* Breadcrumb */}
      <div className="bg-white border-b border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-3">
          <nav className="flex items-center space-x-2 text-sm text-slate-600">
            <button
              onClick={() => navigate('/')}
              className="hover:text-slate-900 transition-colors"
            >
              Home
            </button>
            <span>/</span>
            <button
              onClick={() => navigate('/people-results')}
              className="hover:text-slate-900 transition-colors"
            >
              People Search
            </button>
            <span>/</span>
            <span className="text-slate-900">{personData.name}</span>
          </nav>
        </div>
      </div>

      {/* Profile Header */}
      <div className="bg-white border-b border-slate-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center gap-6">
            <div className="h-20 w-20 rounded-full bg-sky-100 flex items-center justify-center">
              <User className="h-10 w-10 text-sky-600" />
            </div>
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-slate-900">{personData.name}</h1>
              <p className="text-lg text-slate-600">
                {personData.dob} {personData.dod && `– ${personData.dod}`} • {personData.idNumber}
              </p>
              <div className="mt-2 flex items-center gap-4">
                <span className={`inline-flex items-center gap-1 rounded-full px-3 py-1 text-sm font-semibold ring-1 ${getRiskColor(personData.riskLevel)}`}>
                  <span className={`inline-block h-2 w-2 rounded-full ${getRiskColor(personData.riskLevel).split(' ')[1].replace('text-', 'bg-')}`}></span>
                  {personData.riskLevel} Risk
                </span>
                <span className="text-sm text-slate-500">Risk Score: {personData.riskScore}</span>
              </div>
            </div>
            <div className="flex gap-2">
              <button className="inline-flex items-center gap-2 rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors">
                <Download className="h-4 w-4" />
                Export
              </button>
              <button className="inline-flex items-center gap-2 rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700 transition-colors">
                <Star className="h-4 w-4" />
                Add to Watchlist
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* Personal Information */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Personal Information</h2>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <div>
                  <label className="text-sm font-medium text-slate-600">Full Name</label>
                  <p className="text-slate-900">{personData.name}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-600">Date of Birth</label>
                  <p className="text-slate-900">{personData.dob}</p>
                </div>
                {personData.dod && (
                  <div>
                    <label className="text-sm font-medium text-slate-600">Date of Death</label>
                    <p className="text-slate-900">{personData.dod}</p>
                  </div>
                )}
                <div>
                  <label className="text-sm font-medium text-slate-600">ID Number</label>
                  <p className="text-slate-900">{personData.idNumber}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-600">Gender</label>
                  <p className="text-slate-900">{personData.gender}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-600">Nationality</label>
                  <p className="text-slate-900">{personData.nationality}</p>
                </div>
              </div>
            </section>

            {/* Legal History */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Legal History ({personData.totalCases} Cases)</h2>
              <div className="space-y-4">
                {personData.cases.map((caseItem, index) => (
                  <div key={caseItem.id} className="border-l-4 border-sky-500 pl-4 py-3 hover:bg-slate-50 rounded-r-lg transition-colors">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h3 className="font-medium text-slate-900 mb-1">{caseItem.title}</h3>
                        <div className="grid grid-cols-2 gap-2 text-sm text-slate-600">
                          <p><span className="font-medium">Case No:</span> {caseItem.caseNumber}</p>
                          <p><span className="font-medium">Type:</span> {caseItem.type}</p>
                          <p><span className="font-medium">Status:</span> 
                            <span className={`ml-1 px-2 py-1 rounded-full text-xs font-medium ${
                              caseItem.status === 'Resolved' ? 'bg-emerald-100 text-emerald-700' : 
                              caseItem.status === 'Pending' ? 'bg-amber-100 text-amber-700' : 
                              'bg-slate-100 text-slate-700'
                            }`}>
                              {caseItem.status}
                            </span>
                          </p>
                          <p><span className="font-medium">Outcome:</span> 
                            <span className={`ml-1 px-2 py-1 rounded-full text-xs font-medium ${
                              caseItem.outcome === 'Favorable' ? 'bg-emerald-100 text-emerald-700' : 
                              caseItem.outcome === 'Unfavorable' ? 'bg-red-100 text-red-700' : 
                              'bg-slate-100 text-slate-700'
                            }`}>
                              {caseItem.outcome}
                            </span>
                          </p>
                          <p><span className="font-medium">Court:</span> {caseItem.court}</p>
                          <p><span className="font-medium">Judge:</span> {caseItem.judge}</p>
                        </div>
                        <p className="text-sm text-slate-500 mt-2"><span className="font-medium">Date:</span> {caseItem.date}</p>
                      </div>
                      <button 
                        onClick={() => navigate(`/case-detail?caseId=${caseItem.id}&source=search`)}
                        className="ml-4 text-sky-600 hover:text-sky-700 text-sm font-medium"
                      >
                        View Details →
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* Case Details */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Case Details</h2>
              <div className="space-y-6">
                {personData.caseDetails.map((detail, index) => (
                  <div key={index}>
                    <h3 className="font-medium text-slate-900 mb-2">{detail.title}</h3>
                    <div className="bg-slate-50 rounded-lg p-4">
                      <p className="text-sm text-slate-700 leading-relaxed">{detail.description}</p>
                    </div>
                    <div className="mt-3 grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="font-medium text-slate-600">Judge:</span>
                        <span className="text-slate-900 ml-1">{detail.judge}</span>
                      </div>
                      <div>
                        <span className="font-medium text-slate-600">Court:</span>
                        <span className="text-slate-900 ml-1">{detail.court}</span>
                      </div>
                      <div>
                        <span className="font-medium text-slate-600">Lawyer:</span>
                        <span className="text-slate-900 ml-1">{detail.lawyer}</span>
                      </div>
                      <div>
                        <span className="font-medium text-slate-600">Outcome:</span>
                        <span className="text-slate-900 ml-1">{detail.outcome}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Risk Assessment */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Risk Assessment</h2>
              <div className="text-center">
                <div className={`text-3xl font-bold mb-2 ${getRiskScoreColor(personData.riskScore)}`}>
                  {personData.riskScore}
                </div>
                <div className="text-sm text-slate-600 mb-4">{personData.riskLevel} Risk Score</div>
                <div className="w-full bg-slate-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${getProgressBarColor(personData.riskScore)}`}
                    style={{ width: `${personData.riskScore}%` }}
                  ></div>
                </div>
                <p className="text-xs text-slate-500 mt-2">Based on legal history and case outcomes</p>
              </div>
            </section>

            {/* Quick Stats */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Quick Stats</h2>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Total Cases</span>
                  <span className="text-sm font-medium text-slate-900">{personData.totalCases}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Resolved Cases</span>
                  <span className="text-sm font-medium text-slate-900">{personData.resolvedCases}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Pending Cases</span>
                  <span className="text-sm font-medium text-slate-900">{personData.pendingCases}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-600">Favorable Outcomes</span>
                  <span className="text-sm font-medium text-slate-900">{personData.favorableOutcomes}</span>
                </div>
              </div>
            </section>

            {/* Related People */}
            <section className="rounded-xl border border-slate-200 bg-white p-6">
              <h2 className="text-lg font-semibold text-slate-900 mb-4">Related People</h2>
              <div className="space-y-3">
                {personData.relatedPeople.map((person, index) => (
                  <div key={index} className="flex items-center gap-3">
                    <div className="h-8 w-8 rounded-full bg-slate-100 flex items-center justify-center">
                      <User className="h-4 w-4 text-slate-500" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-slate-900">{person.name}</p>
                      <p className="text-xs text-slate-500">{person.role}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PersonProfile;
