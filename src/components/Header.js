import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X } from 'lucide-react';

const Header = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'People Search', href: '/people-results' },
    { name: 'Banks', href: '/banks' },
    { name: 'Insurance', href: '/insurance' },
    { name: 'Advanced Search', href: '/advanced-search' },
    { name: 'People Database', href: '/people-database' },
    { name: 'About', href: '/about' },
    { name: 'Contact', href: '/contact' },
    { name: 'Specification', href: '/specification' },
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
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
