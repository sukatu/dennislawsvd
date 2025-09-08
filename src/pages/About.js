import React from 'react';
import { Link } from 'react-router-dom';
import { ExternalLink } from 'lucide-react';

const About = () => {
  return (
    <div>
      {/* Page Header */}
      <section className="bg-slate-900 text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight">About Dennislaw SVD</h1>
          <p className="mt-4 text-xl text-slate-300 max-w-3xl mx-auto">
            Your comprehensive legal research platform for finding people, cases, and legal information across Ghana's court system.
          </p>
        </div>
      </section>

      {/* Main Content */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <div className="prose prose-slate max-w-none">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">Our Mission</h2>
              <p className="text-slate-600 mb-6">
                Dennislaw SVD is dedicated to providing comprehensive legal research tools that make it easier for legal professionals, researchers, and the public to access and analyze legal information across Ghana's court system.
              </p>
              
              <h2 className="text-2xl font-bold text-slate-900 mb-6">What We Do</h2>
              <p className="text-slate-600 mb-6">
                Our platform offers advanced search capabilities to find people involved in legal cases, track case history, and access detailed information about legal proceedings. We connect data from over 464 courts across 16 regions in Ghana.
              </p>
              
              <h2 className="text-2xl font-bold text-slate-900 mb-6">Key Features</h2>
              <ul className="list-disc list-inside text-slate-600 mb-6 space-y-2">
                <li>Comprehensive people search by case title</li>
                <li>Advanced filtering and search options</li>
                <li>Case history tracking and analysis</li>
                <li>Integration with DennislawGH platform</li>
                <li>Mobile-optimized interface</li>
                <li>Real-time data updates</li>
              </ul>
              
              <h2 className="text-2xl font-bold text-slate-900 mb-6">Our Data</h2>
              <p className="text-slate-600 mb-6">
                We maintain a comprehensive database of over 2.5 million case records spanning more than 25 years of legal history. Our data is updated daily and maintains a 99.9% accuracy rate.
              </p>
            </div>
          </div>
          
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Quick Stats</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">People in Database</span>
                  <span className="font-semibold text-slate-900">500K+</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Case Records</span>
                  <span className="font-semibold text-slate-900">2.5M+</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Courts Connected</span>
                  <span className="font-semibold text-slate-900">464</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Regions Covered</span>
                  <span className="font-semibold text-slate-900">16</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Years of Data</span>
                  <span className="font-semibold text-slate-900">25+</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-600">Accuracy Rate</span>
                  <span className="font-semibold text-slate-900">99.9%</span>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm mt-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Contact Us</h3>
              <p className="text-slate-600 text-sm mb-4">
                Have questions about our platform or need support? We're here to help.
              </p>
              <Link
                to="/contact"
                className="inline-flex items-center gap-2 text-sky-600 hover:text-sky-700 font-medium"
              >
                Get in Touch
                <ExternalLink className="h-4 w-4" />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
