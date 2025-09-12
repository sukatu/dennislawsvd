import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Menu, X, LogIn, UserPlus, LogOut, User, Settings } from 'lucide-react';

const Header = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const location = useLocation();
  const navigate = useNavigate();

  // Check authentication status on component mount
  useEffect(() => {
    const authStatus = localStorage.getItem('isAuthenticated');
    const email = localStorage.getItem('userEmail');
    const authProvider = localStorage.getItem('authProvider');
    setIsAuthenticated(authStatus === 'true');
    setUserEmail(email || '');
    
    // Log authentication provider for debugging
    if (authProvider) {
      console.log('User authenticated via:', authProvider);
    }
  }, []);

  const handleLogout = () => {
    // Clear all authentication data
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userName');
    localStorage.removeItem('userPicture');
    localStorage.removeItem('authProvider');
    
    // If user was authenticated via Google, also sign out from Google
    if (window.google?.accounts?.id) {
      window.google.accounts.id.disableAutoSelect();
    }
    
    setIsAuthenticated(false);
    setUserEmail('');
    navigate('/');
  };

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'People', href: '/people' },
    { name: 'Banks', href: '/banks' },
    { name: 'Insurance', href: '/insurance' },
    { name: 'Companies', href: '/companies' },
    { name: 'About', href: '/about' },
    { name: 'Contact', href: '/contact' },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <header className="w-full bg-slate-900 text-white">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2">
          <span className="h-2.5 w-2.5 rounded-full bg-sky-400 ring-4 ring-white/10"></span>
          <span className="font-semibold">Dennislaw SVD</span>
        </Link>
        
        <nav className="hidden md:flex items-center gap-6 text-sm/6 text-slate-200">
          {navigation.map((item) => (
            <Link
              key={item.name}
              to={item.href}
              className={`hover:text-white transition-colors ${
                isActive(item.href) ? 'text-white' : 'text-slate-200'
              }`}
            >
              {item.name}
            </Link>
          ))}
        </nav>

        {/* Authentication Buttons */}
        <div className="hidden md:flex items-center gap-3">
          {isAuthenticated ? (
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2 text-sm text-slate-200">
                <User className="h-4 w-4" />
                <span className="hidden lg:inline">{userEmail}</span>
              </div>
              <Link
                to="/settings"
                className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-200 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
              >
                <Settings className="h-4 w-4" />
                Settings
              </Link>
              <button
                onClick={handleLogout}
                className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-200 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
              >
                <LogOut className="h-4 w-4" />
                Logout
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link
                to="/login"
                className="inline-flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-200 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
              >
                <LogIn className="h-4 w-4" />
                Login
              </Link>
              <Link
                to="/signup"
                className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-sky-600 hover:bg-sky-700 rounded-lg transition-colors"
              >
                <UserPlus className="h-4 w-4" />
                Register
              </Link>
            </div>
          )}
        </div>
        
        <button
          className="md:hidden inline-flex items-center justify-center rounded-lg p-2 hover:bg-white/10"
          aria-label="Open menu"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        >
          {isMobileMenuOpen ? (
            <X className="h-5 w-5" />
          ) : (
            <Menu className="h-5 w-5" />
          )}
        </button>
      </div>
      
      {/* Mobile menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-slate-800 border-t border-slate-700">
          <div className="px-4 py-2 space-y-1">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`block px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive(item.href)
                    ? 'text-white bg-slate-700'
                    : 'text-slate-200 hover:text-white hover:bg-slate-700'
                }`}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                {item.name}
              </Link>
            ))}
            
            {/* Mobile Authentication Buttons */}
            <div className="border-t border-slate-700 pt-2 mt-2">
              {isAuthenticated ? (
                <div className="space-y-1">
                  <div className="px-3 py-2 text-sm text-slate-300 flex items-center gap-2">
                    <User className="h-4 w-4" />
                    {userEmail}
                  </div>
                  <Link
                    to="/settings"
                    className="block px-3 py-2 rounded-md text-sm font-medium text-slate-200 hover:text-white hover:bg-slate-700 transition-colors flex items-center gap-2"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <Settings className="h-4 w-4" />
                    Settings
                  </Link>
                  <button
                    onClick={() => {
                      handleLogout();
                      setIsMobileMenuOpen(false);
                    }}
                    className="w-full text-left px-3 py-2 rounded-md text-sm font-medium text-slate-200 hover:text-white hover:bg-slate-700 transition-colors flex items-center gap-2"
                  >
                    <LogOut className="h-4 w-4" />
                    Logout
                  </button>
                </div>
              ) : (
                <div className="space-y-1">
                  <Link
                    to="/login"
                    className="block px-3 py-2 rounded-md text-sm font-medium text-slate-200 hover:text-white hover:bg-slate-700 transition-colors flex items-center gap-2"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <LogIn className="h-4 w-4" />
                    Login
                  </Link>
                  <Link
                    to="/signup"
                    className="block px-3 py-2 rounded-md text-sm font-medium text-white bg-sky-600 hover:bg-sky-700 transition-colors flex items-center gap-2"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <UserPlus className="h-4 w-4" />
                    Register
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
