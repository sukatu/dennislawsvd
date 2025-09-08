import React from 'react';
import { ExternalLink, Database, Shield, Zap, Server, Code, Lock, BarChart3 } from 'lucide-react';

const Specification = () => {
  const features = [
    {
      icon: <Database className="h-6 w-6 text-sky-600" />,
      title: "People Search",
      items: [
        "Search by name, ID number, phone, or address",
        "Advanced filtering options",
        "Risk assessment scoring",
        "Detailed profile information",
        "Case history and legal records"
      ]
    },
    {
      icon: <Shield className="h-6 w-6 text-sky-600" />,
      title: "Case Management",
      items: [
        "Comprehensive case database",
        "Case status tracking",
        "Court information and jurisdiction",
        "Judge and lawyer details",
        "Case outcome and resolution"
      ]
    },
    {
      icon: <BarChart3 className="h-6 w-6 text-sky-600" />,
      title: "Risk Assessment",
      items: [
        "Automated risk scoring algorithm",
        "Risk level categorization (Low, Medium, High)",
        "Historical data analysis",
        "Predictive risk modeling",
        "Risk trend analysis"
      ]
    },
    {
      icon: <Zap className="h-6 w-6 text-sky-600" />,
      title: "Reporting & Analytics",
      items: [
        "Custom report generation",
        "Data export capabilities",
        "Statistical analysis",
        "Trend visualization",
        "Performance metrics"
      ]
    }
  ];

  const techStack = [
    {
      category: "Frontend",
      icon: <Code className="h-5 w-5 text-sky-600" />,
      items: ["HTML5 & CSS3", "Tailwind CSS", "JavaScript (ES6+)", "Responsive Design"]
    },
    {
      category: "Backend",
      icon: <Server className="h-5 w-5 text-sky-600" />,
      items: ["Node.js / Python", "Express.js / Django", "RESTful API", "JWT Authentication"]
    },
    {
      category: "Database",
      icon: <Database className="h-5 w-5 text-sky-600" />,
      items: ["PostgreSQL", "Redis (Caching)", "Elasticsearch (Search)", "Data Encryption"]
    },
    {
      category: "Infrastructure",
      icon: <Shield className="h-5 w-5 text-sky-600" />,
      items: ["Cloud Hosting (AWS/Azure)", "CDN (Content Delivery)", "SSL/TLS Security", "Load Balancing"]
    }
  ];

  const apiEndpoints = [
    { method: "GET", endpoint: "/api/people/search", description: "Search for people by various criteria" },
    { method: "POST", endpoint: "/api/people", description: "Create a new person record" },
    { method: "GET", endpoint: "/api/cases/search", description: "Search for cases by various criteria" },
    { method: "GET", endpoint: "/api/risk-assessment/{person_id}", description: "Get risk assessment for a specific person" }
  ];

  const securityFeatures = [
    {
      title: "Authentication & Authorization",
      icon: <Lock className="h-5 w-5 text-sky-600" />,
      items: [
        "JWT-based authentication",
        "Role-based access control",
        "Multi-factor authentication",
        "Session management",
        "Password policies"
      ]
    },
    {
      title: "Data Protection",
      icon: <Shield className="h-5 w-5 text-sky-600" />,
      items: [
        "End-to-end encryption",
        "Data anonymization",
        "Secure data transmission",
        "Regular security audits",
        "GDPR compliance"
      ]
    }
  ];

  return (
    <div>
      {/* Hero Section */}
      <section className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-10 text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-slate-900">System Specification</h1>
        <p className="mt-2 text-slate-600">Comprehensive technical documentation for the Dennislaw SVD platform architecture, features, and implementation details.</p>
      </section>

      {/* Main Content */}
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 pb-20">
        <div className="prose prose-slate max-w-none">
          {/* Table of Contents */}
          <div className="bg-slate-50 border border-slate-200 rounded-lg p-6 mb-8">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">Table of Contents</h2>
            <ul className="space-y-2 text-sm">
              <li><a href="#overview" className="text-sky-600 hover:text-sky-700">1. System Overview</a></li>
              <li><a href="#architecture" className="text-sky-600 hover:text-sky-700">2. System Architecture</a></li>
              <li><a href="#features" className="text-sky-600 hover:text-sky-700">3. Core Features</a></li>
              <li><a href="#database" className="text-sky-600 hover:text-sky-700">4. Database Schema</a></li>
              <li><a href="#api" className="text-sky-600 hover:text-sky-700">5. API Documentation</a></li>
              <li><a href="#security" className="text-sky-600 hover:text-sky-700">6. Security Features</a></li>
              <li><a href="#performance" className="text-sky-600 hover:text-sky-700">7. Performance Requirements</a></li>
              <li><a href="#deployment" className="text-sky-600 hover:text-sky-700">8. Deployment Guide</a></li>
            </ul>
          </div>

          {/* System Overview */}
          <section id="overview" className="mb-12">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">System Overview</h2>
            <p className="text-slate-600 mb-4">The Dennislaw SVD is a comprehensive legal database platform designed to provide instant access to legal case information, people search capabilities, and risk assessment tools for legal professionals, researchers, and the general public.</p>
            
            <div className="bg-sky-50 border border-sky-200 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-3">Key Objectives</h3>
              <ul className="space-y-2 text-slate-700">
                <li>• Provide comprehensive legal case database access</li>
                <li>• Enable efficient people search and verification</li>
                <li>• Offer risk assessment and scoring capabilities</li>
                <li>• Ensure data security and privacy compliance</li>
                <li>• Support multiple user roles and permissions</li>
              </ul>
            </div>

            <h3 className="text-xl font-semibold text-slate-900 mb-4">Target Users</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div className="bg-white border border-slate-200 rounded-lg p-4">
                <h4 className="font-semibold text-slate-900 mb-2">Legal Professionals</h4>
                <p className="text-sm text-slate-600">Lawyers, judges, and legal researchers who need quick access to case information and people verification.</p>
              </div>
              <div className="bg-white border border-slate-200 rounded-lg p-4">
                <h4 className="font-semibold text-slate-900 mb-2">Government Agencies</h4>
                <p className="text-sm text-slate-600">Government departments requiring background checks and legal history verification.</p>
              </div>
              <div className="bg-white border border-slate-200 rounded-lg p-4">
                <h4 className="font-semibold text-slate-900 mb-2">Private Sector</h4>
                <p className="text-sm text-slate-600">Companies conducting due diligence and background verification for employment or partnerships.</p>
              </div>
              <div className="bg-white border border-slate-200 rounded-lg p-4">
                <h4 className="font-semibold text-slate-900 mb-2">General Public</h4>
                <p className="text-sm text-slate-600">Individuals seeking information about legal cases or people for personal or business purposes.</p>
              </div>
            </div>
          </section>

          {/* System Architecture */}
          <section id="architecture" className="mb-12">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">System Architecture</h2>
            
            <div className="bg-white border border-slate-200 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Technology Stack</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {techStack.map((stack, index) => (
                  <div key={index}>
                    <div className="flex items-center gap-2 mb-2">
                      {stack.icon}
                      <h4 className="font-medium text-slate-900">{stack.category}</h4>
                    </div>
                    <ul className="space-y-1 text-sm text-slate-600">
                      {stack.items.map((item, itemIndex) => (
                        <li key={itemIndex}>• {item}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-slate-50 border border-slate-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">System Components</h3>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <div className="h-8 w-8 rounded-full bg-sky-100 flex items-center justify-center flex-shrink-0">
                    <span className="text-sm font-semibold text-sky-600">1</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-slate-900">Web Interface</h4>
                    <p className="text-sm text-slate-600">Responsive web application providing user-friendly access to all system features.</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="h-8 w-8 rounded-full bg-sky-100 flex items-center justify-center flex-shrink-0">
                    <span className="text-sm font-semibold text-sky-600">2</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-slate-900">API Gateway</h4>
                    <p className="text-sm text-slate-600">Centralized entry point for all API requests with authentication and rate limiting.</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="h-8 w-8 rounded-full bg-sky-100 flex items-center justify-center flex-shrink-0">
                    <span className="text-sm font-semibold text-sky-600">3</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-slate-900">Search Engine</h4>
                    <p className="text-sm text-slate-600">Advanced search capabilities with full-text search and filtering options.</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="h-8 w-8 rounded-full bg-sky-100 flex items-center justify-center flex-shrink-0">
                    <span className="text-sm font-semibold text-sky-600">4</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-slate-900">Data Processing</h4>
                    <p className="text-sm text-slate-600">Automated data ingestion, validation, and processing from various court systems.</p>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Core Features */}
          <section id="features" className="mb-12">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">Core Features</h2>
            
            <div className="space-y-6">
              {features.map((feature, index) => (
                <div key={index} className="bg-white border border-slate-200 rounded-lg p-6">
                  <div className="flex items-center gap-3 mb-3">
                    {feature.icon}
                    <h3 className="text-lg font-semibold text-slate-900">{feature.title}</h3>
                  </div>
                  <ul className="space-y-2 text-slate-600">
                    {feature.items.map((item, itemIndex) => (
                      <li key={itemIndex}>• {item}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </section>

          {/* Database Schema */}
          <section id="database" className="mb-12">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">Database Schema</h2>
            
            <div className="bg-white border border-slate-200 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Core Tables</h3>
              <div className="space-y-4">
                <div className="border-l-4 border-sky-500 pl-4">
                  <h4 className="font-medium text-slate-900">People</h4>
                  <p className="text-sm text-slate-600">Stores personal information, contact details, and identification data.</p>
                  <div className="mt-2 text-xs text-slate-500">
                    Fields: id, first_name, last_name, date_of_birth, id_number, phone, email, address, created_at, updated_at
                  </div>
                </div>
                <div className="border-l-4 border-sky-500 pl-4">
                  <h4 className="font-medium text-slate-900">Cases</h4>
                  <p className="text-sm text-slate-600">Contains case information, court details, and legal proceedings.</p>
                  <div className="mt-2 text-xs text-slate-500">
                    Fields: id, case_number, title, description, court_id, judge_id, status, outcome, date_filed, date_resolved
                  </div>
                </div>
                <div className="border-l-4 border-sky-500 pl-4">
                  <h4 className="font-medium text-slate-900">People_Cases</h4>
                  <p className="text-sm text-slate-600">Junction table linking people to their associated cases.</p>
                  <div className="mt-2 text-xs text-slate-500">
                    Fields: person_id, case_id, role, involvement_type, created_at
                  </div>
                </div>
                <div className="border-l-4 border-sky-500 pl-4">
                  <h4 className="font-medium text-slate-900">Courts</h4>
                  <p className="text-sm text-slate-600">Court information including jurisdiction and contact details.</p>
                  <div className="mt-2 text-xs text-slate-500">
                    Fields: id, name, type, region, address, phone, email, created_at
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* API Documentation */}
          <section id="api" className="mb-12">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">API Documentation</h2>
            
            <div className="bg-white border border-slate-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Endpoints</h3>
              <div className="space-y-4">
                {apiEndpoints.map((endpoint, index) => (
                  <div key={index} className="bg-slate-50 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <span className={`px-2 py-1 text-xs font-semibold text-white rounded ${
                        endpoint.method === 'GET' ? 'bg-green-600' : 'bg-blue-600'
                      }`}>
                        {endpoint.method}
                      </span>
                      <code className="text-sm font-mono">{endpoint.endpoint}</code>
                    </div>
                    <p className="text-sm text-slate-600">{endpoint.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* Security Features */}
          <section id="security" className="mb-12">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">Security Features</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {securityFeatures.map((feature, index) => (
                <div key={index} className="bg-white border border-slate-200 rounded-lg p-6">
                  <div className="flex items-center gap-2 mb-3">
                    {feature.icon}
                    <h3 className="text-lg font-semibold text-slate-900">{feature.title}</h3>
                  </div>
                  <ul className="space-y-2 text-slate-600">
                    {feature.items.map((item, itemIndex) => (
                      <li key={itemIndex}>• {item}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </section>

          {/* Performance Requirements */}
          <section id="performance" className="mb-12">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">Performance Requirements</h2>
            
            <div className="bg-white border border-slate-200 rounded-lg p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-semibold text-slate-900 mb-3">Response Times</h3>
                  <ul className="space-y-2 text-slate-600">
                    <li>• Search queries: &lt; 2 seconds</li>
                    <li>• Page load: &lt; 3 seconds</li>
                    <li>• API responses: &lt; 1 second</li>
                    <li>• Database queries: &lt; 500ms</li>
                  </ul>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-slate-900 mb-3">Scalability</h3>
                  <ul className="space-y-2 text-slate-600">
                    <li>• Support 10,000+ concurrent users</li>
                    <li>• Handle 1M+ records</li>
                    <li>• 99.9% uptime</li>
                    <li>• Auto-scaling capabilities</li>
                  </ul>
                </div>
              </div>
            </div>
          </section>

          {/* Deployment Guide */}
          <section id="deployment" className="mb-12">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">Deployment Guide</h2>
            
            <div className="bg-white border border-slate-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Prerequisites</h3>
              <ul className="space-y-2 text-slate-600 mb-6">
                <li>• Node.js 18+ or Python 3.9+</li>
                <li>• PostgreSQL 13+</li>
                <li>• Redis 6+</li>
                <li>• Elasticsearch 7+</li>
                <li>• SSL certificate</li>
              </ul>
              
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Installation Steps</h3>
              <div className="bg-slate-900 text-slate-100 rounded-lg p-4 font-mono text-sm">
                <div className="space-y-2">
                  <div># Clone repository</div>
                  <div>git clone https://github.com/dennislaw/svd.git</div>
                  <div>cd svd</div>
                  <div></div>
                  <div># Install dependencies</div>
                  <div>npm install</div>
                  <div></div>
                  <div># Configure environment</div>
                  <div>cp .env.example .env</div>
                  <div></div>
                  <div># Run database migrations</div>
                  <div>npm run migrate</div>
                  <div></div>
                  <div># Start application</div>
                  <div>npm start</div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default Specification;
