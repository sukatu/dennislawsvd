import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Menu, X, LogIn, UserPlus, LogOut, User, Settings } from 'lucide-react';

const Header = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const [userName, setUserName] = useState('');
  const location = useLocation();
  const navigate = useNavigate();

  // Check authentication status on component mount and listen for changes
  useEffect(() => {
    const checkAuthStatus = () => {
      const authStatus = localStorage.getItem('isAuthenticated');
      const adminStatus = localStorage.getItem('isAdmin');
      const email = localStorage.getItem('userEmail');
      const name = localStorage.getItem('userName');
      const authProvider = localStorage.getItem('authProvider');
      setIsAuthenticated(authStatus === 'true');
      setIsAdmin(adminStatus === 'true');
      setUserEmail(email || '');
      setUserName(name || '');
      
      // Log authentication provider for debugging
      if (authProvider) {
        console.log('User authenticated via:', authProvider);
      }
    };

    // Check initial auth status
    checkAuthStatus();

    // Listen for authentication changes
    const handleAuthChange = () => {
      checkAuthStatus();
    };

    // Add event listener for custom auth events
    window.addEventListener('authStateChanged', handleAuthChange);
    
    // Also listen for storage changes (in case localStorage is modified from another tab)
    window.addEventListener('storage', handleAuthChange);

    // Cleanup event listeners
    return () => {
      window.removeEventListener('authStateChanged', handleAuthChange);
      window.removeEventListener('storage', handleAuthChange);
    };
  }, []);

  // Function to get user initials
  const getUserInitials = () => {
    if (userName) {
      return userName
        .split(' ')
        .map(name => name.charAt(0))
        .join('')
        .toUpperCase()
        .slice(0, 2);
    }
    if (userEmail) {
      const emailName = userEmail.split('@')[0];
      return emailName
        .split('.')
        .map(part => part.charAt(0))
        .join('')
        .toUpperCase()
        .slice(0, 2);
    }
    return 'U';
  };

  const handleLogout = () => {
    // Clear all authentication data
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userName');
    localStorage.removeItem('userPicture');
    localStorage.removeItem('authProvider');
    localStorage.removeItem('accessToken');
    localStorage.removeItem('userData');
    
    // If user was authenticated via Google, also sign out from Google
    if (window.google?.accounts?.id) {
      window.google.accounts.id.disableAutoSelect();
    }
    
    // Dispatch custom event to notify other components
    window.dispatchEvent(new CustomEvent('authStateChanged'));
    
    setIsAuthenticated(false);
    setUserEmail('');
    setUserName('');
    navigate('/');
  };

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'People', href: '/people' },
    { name: 'Banks', href: '/banks' },
    { name: 'Insurance', href: '/insurance' },
    { name: 'Companies', href: '/companies' },
    ...(isAdmin ? [{ name: 'Admin Dashboard', href: '/admin' }] : []),
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
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-sky-500 rounded-full flex items-center justify-center text-white text-sm font-medium">
                  {getUserInitials()}
                </div>
                <span className="hidden lg:inline text-sm text-slate-200">
                  {userName || userEmail.split('@')[0]}
                </span>
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
                    <div className="w-6 h-6 bg-sky-500 rounded-full flex items-center justify-center text-white text-xs font-medium">
                      {getUserInitials()}
                    </div>
                    {userName || userEmail.split('@')[0]}
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
