import React from 'react';
import { 
  Search, 
  Database, 
  MapPin, 
  Shield, 
  Users, 
  Building2, 
  FileText, 
  Globe,
  CheckCircle,
  ArrowRight
} from 'lucide-react';

const Services = () => {
  const services = [
    {
      icon: <Search className="h-8 w-8 text-blue-600" />,
      title: "People Search",
      description: "Comprehensive search across Ghana's legal database to find individuals involved in legal cases.",
      features: [
        "Advanced search filters",
        "Case history tracking",
        "Risk assessment profiles",
        "Real-time data updates"
      ]
    },
    {
      icon: <Building2 className="h-8 w-8 text-green-600" />,
      title: "Company Database",
      description: "Access detailed information about companies, their legal standing, and case involvement.",
      features: [
        "Company profiles & details",
        "Legal case history",
        "Financial standing analysis",
        "Compliance tracking"
      ]
    },
    {
      icon: <Shield className="h-8 w-8 text-purple-600" />,
      title: "Insurance Records",
      description: "Search and analyze insurance companies and their legal case involvement.",
      features: [
        "Insurance company profiles",
        "Claim history analysis",
        "Policy coverage details",
        "Legal dispute tracking"
      ]
    },
    {
      icon: <Database className="h-8 w-8 text-orange-600" />,
      title: "Bank Records",
      description: "Comprehensive banking sector database with legal case information.",
      features: [
        "Bank profiles & details",
        "Financial case history",
        "Regulatory compliance",
        "Risk assessment"
      ]
    },
    {
      icon: <MapPin className="h-8 w-8 text-red-600" />,
      title: "Court Locator",
      description: "Find and locate courts and legal institutions across Ghana with interactive maps.",
      features: [
        "Interactive court maps",
        "Location-based search",
        "Court type filtering",
        "Contact information"
      ]
    },
    {
      icon: <FileText className="h-8 w-8 text-indigo-600" />,
      title: "Case Management",
      description: "Comprehensive case tracking and management system for legal professionals.",
      features: [
        "Case timeline tracking",
        "Document management",
        "Hearing schedules",
        "Status updates"
      ]
    }
  ];

  const features = [
    {
      icon: <CheckCircle className="h-6 w-6 text-green-500" />,
      title: "Real-time Data",
      description: "Access the most up-to-date legal information with real-time database updates."
    },
    {
      icon: <CheckCircle className="h-6 w-6 text-green-500" />,
      title: "Advanced Search",
      description: "Powerful search capabilities with multiple filters and criteria options."
    },
    {
      icon: <CheckCircle className="h-6 w-6 text-green-500" />,
      title: "Secure Access",
      description: "Enterprise-grade security with role-based access control and data encryption."
    },
    {
      icon: <CheckCircle className="h-6 w-6 text-green-500" />,
      title: "Mobile Responsive",
      description: "Access your data anywhere with our fully responsive mobile interface."
    }
  ];

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-slate-900 dark:text-white mb-4">
            Our Services
          </h1>
          <p className="text-xl text-slate-600 dark:text-slate-300 max-w-3xl mx-auto">
            Comprehensive legal database solutions designed to help legal professionals, 
            researchers, and organizations access critical legal information across Ghana.
          </p>
        </div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {services.map((service, index) => (
            <div
              key={index}
              className="bg-white dark:bg-slate-800 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700 p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center mb-4">
                {service.icon}
                <h3 className="text-xl font-semibold text-slate-900 dark:text-white ml-3">
                  {service.title}
                </h3>
              </div>
              <p className="text-slate-600 dark:text-slate-300 mb-4">
                {service.description}
              </p>
              <ul className="space-y-2">
                {service.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-center text-sm text-slate-500 dark:text-slate-400">
                    <CheckCircle className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Features Section */}
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700 p-8 mb-16">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-8 text-center">
            Why Choose Dennislaw SVD?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div key={index} className="text-center">
                <div className="flex justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-slate-600 dark:text-slate-300 text-sm">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-8 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">
            Ready to Get Started?
          </h2>
          <p className="text-xl mb-6 opacity-90">
            Join thousands of legal professionals who trust Dennislaw SVD for their research needs.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-slate-100 transition-colors flex items-center justify-center">
              Start Free Trial
              <ArrowRight className="h-4 w-4 ml-2" />
            </button>
            <button className="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors">
              Contact Sales
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Services;
