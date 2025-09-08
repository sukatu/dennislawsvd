import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserPlus, Lock, Check } from 'lucide-react';

const Signup = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    plan: ''
  });
  const [showSuccess, setShowSuccess] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    
    // Show success message
    setShowSuccess(true);
    
    // Redirect after delay
    setTimeout(() => {
      navigate('/people-results?paid=1');
    }, 1500);
  };

  return (
    <div>
      {/* Header */}
      <header className="bg-slate-900 text-white">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="h-8 w-8 rounded-full bg-sky-400 flex items-center justify-center">
                <Lock className="h-4 w-4 text-white" />
              </div>
              <h1 className="text-xl font-bold">Dennislaw SVD</h1>
            </div>
            <nav className="hidden md:flex space-x-6">
              <button
                onClick={() => navigate('/')}
                className="hover:text-sky-400 transition-colors"
              >
                Home
              </button>
              <button
                onClick={() => navigate('/people-database')}
                className="hover:text-sky-400 transition-colors"
              >
                People Database
              </button>
              <button
                onClick={() => navigate('/advanced-search')}
                className="hover:text-sky-400 transition-colors"
              >
                Advanced Search
              </button>
              <button
                onClick={() => navigate('/about')}
                className="hover:text-sky-400 transition-colors"
              >
                About
              </button>
              <button
                onClick={() => navigate('/contact')}
                className="hover:text-sky-400 transition-colors"
              >
                Contact
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="min-h-screen bg-slate-50 py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-md mx-auto">
            <div className="bg-white rounded-xl shadow-lg p-8">
              <div className="text-center mb-8">
                <UserPlus className="h-12 w-12 text-sky-500 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-slate-900 mb-2">Sign up to Download Reports</h2>
                <p className="text-slate-600">Create an account and complete payment to download generated reports.</p>
              </div>
              
              {!showSuccess ? (
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Full Name</label>
                    <input
                      type="text"
                      name="fullName"
                      value={formData.fullName}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-colors"
                      placeholder="Enter your full name"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Email</label>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-colors"
                      placeholder="Enter your email address"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Password</label>
                    <input
                      type="password"
                      name="password"
                      value={formData.password}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-colors"
                      placeholder="Enter your password"
                      minLength="6"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">Plan</label>
                    <select
                      name="plan"
                      value={formData.plan}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-colors"
                      required
                    >
                      <option value="">Choose a plan</option>
                      <option value="basic">Basic (per-report)</option>
                      <option value="premium">Premium (monthly)</option>
                    </select>
                  </div>
                  
                  <button
                    type="submit"
                    className="w-full bg-sky-500 hover:bg-sky-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center space-x-2"
                  >
                    <Lock className="h-4 w-4" />
                    <span>Continue to Payment</span>
                  </button>
                </form>
              ) : (
                <div className="text-center">
                  <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                    <Check className="h-8 w-8 text-green-600 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-green-800 mb-2">Account Created Successfully!</h3>
                    <p className="text-green-700">Redirecting to payment...</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Signup;
