import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Users, 
  Key, 
  FileText, 
  UserCheck, 
  Building2, 
  Shield, 
  CreditCard, 
  BarChart3, 
  Settings, 
  LogOut,
  Menu,
  X,
  Home,
  Activity,
  TrendingUp,
  Database,
  AlertCircle,
  CheckCircle,
  Star
} from 'lucide-react';
import UserManagement from '../components/admin/UserManagement';
import ApiKeyManagement from '../components/admin/ApiKeyManagement';
import CaseManagement from '../components/admin/CaseManagement';
import PeopleManagement from '../components/admin/PeopleManagement';
import BankManagement from '../components/admin/BankManagement';
import InsuranceManagement from '../components/admin/InsuranceManagement';
import CompanyManagement from '../components/admin/CompanyManagement';
import PaymentManagement from '../components/admin/PaymentManagement';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [userInfo, setUserInfo] = useState(null);
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalCases: 0,
    totalPeople: 0,
    totalBanks: 0,
    totalInsurance: 0,
    totalCompanies: 0,
    totalPayments: 0,
    activeSubscriptions: 0,
    // Enhanced stats
    totalRevenue: 0,
    avgRiskScore: 0,
    highRiskCount: 0,
    verifiedCount: 0,
    totalBranches: 0,
    totalEmployees: 0,
    avgRating: 0,
    pendingPayments: 0,
    systemHealth: 'healthy'
  });

  // Check authentication and admin status
  useEffect(() => {
    const checkAuthStatus = () => {
      const authStatus = localStorage.getItem('isAuthenticated');
      const userData = localStorage.getItem('userData');
      const isAuth = authStatus === 'true';
      
      setIsAuthenticated(isAuth);
      
      if (isAuth && userData) {
        try {
          const user = JSON.parse(userData);
          setUserInfo(user);
          // Check if user is admin (you can modify this logic based on your user model)
          setIsAdmin(user.role === 'admin' || user.is_admin === true);
        } catch (error) {
          console.error('Error parsing user data:', error);
        }
      }
    };

    checkAuthStatus();

    // Listen for authentication changes
    const handleAuthChange = () => {
      checkAuthStatus();
    };

    window.addEventListener('authStateChanged', handleAuthChange);
    window.addEventListener('storage', handleAuthChange);

    return () => {
      window.removeEventListener('authStateChanged', handleAuthChange);
      window.removeEventListener('storage', handleAuthChange);
    };
  }, []);

  // Load dashboard statistics
  useEffect(() => {
    if (isAdmin) {
      loadDashboardStats();
    }
  }, [isAdmin]);

  const loadDashboardStats = async () => {
    try {
      // Load statistics from various endpoints
      const [adminRes, usersRes, casesRes, peopleRes, banksRes, insuranceRes, companiesRes, paymentsRes] = await Promise.all([
        fetch('http://localhost:8000/api/admin/stats'),
        fetch('http://localhost:8000/api/admin/users/stats'),
        fetch('http://localhost:8000/api/admin/cases/stats'),
        fetch('http://localhost:8000/api/admin/people/stats'),
        fetch('http://localhost:8000/api/admin/banks/stats'),
        fetch('http://localhost:8000/api/admin/insurance/stats'),
        fetch('http://localhost:8000/api/admin/companies/stats'),
        fetch('http://localhost:8000/api/admin/payments/stats')
      ]);

      const [adminData, usersData, casesData, peopleData, banksData, insuranceData, companiesData, paymentsData] = await Promise.all([
        adminRes.json(),
        usersRes.json(),
        casesRes.json(),
        peopleRes.json(),
        banksRes.json(),
        insuranceRes.json(),
        companiesRes.json(),
        paymentsRes.json()
      ]);

      setStats({
        totalUsers: adminData.total_users || 0,
        totalCases: adminData.total_cases || 0,
        totalPeople: adminData.total_people || 0,
        totalBanks: adminData.total_banks || 0,
        totalInsurance: adminData.total_insurance || 0,
        totalCompanies: adminData.total_companies || 0,
        totalPayments: adminData.total_payments || 0,
        activeSubscriptions: adminData.active_subscriptions || 0,
        // Enhanced stats
        totalRevenue: paymentsData.total_revenue || 0,
        avgRiskScore: peopleData.avg_risk_score || 0,
        highRiskCount: peopleData.high_risk_count || 0,
        verifiedCount: peopleData.verified_count || 0,
        totalBranches: (banksData.total_branches || 0) + (insuranceData.total_branches || 0),
        totalEmployees: companiesData.total_employees || 0,
        avgRating: ((banksData.avg_rating || 0) + (insuranceData.avg_rating || 0) + (companiesData.avg_rating || 0)) / 3,
        pendingPayments: paymentsData.pending_payments || 0,
        systemHealth: 'healthy'
      });
    } catch (error) {
      console.error('Error loading dashboard stats:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userName');
    localStorage.removeItem('userPicture');
    localStorage.removeItem('authProvider');
    localStorage.removeItem('accessToken');
    localStorage.removeItem('userData');
    
    window.dispatchEvent(new CustomEvent('authStateChanged'));
    navigate('/');
  };

  // Redirect if not authenticated or not admin
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-slate-900 mb-2">Authentication Required</h2>
          <p className="text-slate-600 mb-4">Please log in to access the admin dashboard.</p>
          <button
            onClick={() => navigate('/login')}
            className="bg-sky-600 text-white px-4 py-2 rounded-lg hover:bg-sky-700 transition-colors"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  if (!isAdmin) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <Shield className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-slate-900 mb-2">Access Denied</h2>
          <p className="text-slate-600 mb-4">You don't have admin privileges to access this dashboard.</p>
          <button
            onClick={() => navigate('/')}
            className="bg-sky-600 text-white px-4 py-2 rounded-lg hover:bg-sky-700 transition-colors"
          >
            Go to Home
          </button>
        </div>
      </div>
    );
  }

  const navigationItems = [
    { id: 'overview', name: 'Overview', icon: BarChart3 },
    { id: 'users', name: 'Users', icon: Users },
    { id: 'api-keys', name: 'API Keys', icon: Key },
    { id: 'cases', name: 'Cases', icon: FileText },
    { id: 'people', name: 'People', icon: UserCheck },
    { id: 'banks', name: 'Banks', icon: Building2 },
    { id: 'insurance', name: 'Insurance', icon: Shield },
    { id: 'companies', name: 'Companies', icon: Database },
    { id: 'payments', name: 'Payments', icon: CreditCard },
    { id: 'settings', name: 'Settings', icon: Settings }
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'overview':
        return <OverviewTab stats={stats} />;
      case 'users':
        return <UserManagement />;
      case 'api-keys':
        return <ApiKeyManagement />;
      case 'cases':
        return <CaseManagement />;
      case 'people':
        return <PeopleManagement />;
      case 'banks':
        return <BankManagement />;
      case 'insurance':
        return <InsuranceManagement />;
      case 'companies':
        return <CompanyManagement />;
      case 'payments':
        return <PaymentManagement />;
      case 'settings':
        return <SettingsTab />;
      default:
        return <OverviewTab stats={stats} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Mobile sidebar backdrop */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 ${
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="flex items-center justify-between h-16 px-4 border-b border-slate-200">
          <div className="flex items-center space-x-2">
            <div className="h-8 w-8 rounded-full bg-sky-500 flex items-center justify-center">
              <Settings className="h-4 w-4 text-white" />
            </div>
            <span className="font-semibold text-slate-900">Admin Panel</span>
          </div>
          <button
            onClick={() => setIsSidebarOpen(false)}
            className="lg:hidden p-2 rounded-md hover:bg-slate-100"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <nav className="mt-4 px-2">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => {
                  setActiveTab(item.id);
                  setIsSidebarOpen(false);
                }}
                className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg mb-1 transition-colors ${
                  activeTab === item.id
                    ? 'bg-sky-100 text-sky-700'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                <Icon className="h-5 w-5 mr-3" />
                {item.name}
              </button>
            );
          })}
        </nav>

        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-slate-200">
          <div className="flex items-center space-x-3 mb-3">
            <div className="h-8 w-8 rounded-full bg-slate-200 flex items-center justify-center">
              <span className="text-sm font-medium text-slate-600">
                {userInfo?.name?.charAt(0) || userInfo?.email?.charAt(0) || 'A'}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-slate-900 truncate">
                {userInfo?.name || userInfo?.email || 'Admin User'}
              </p>
              <p className="text-xs text-slate-500">Administrator</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="w-full flex items-center px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <LogOut className="h-4 w-4 mr-3" />
            Logout
          </button>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:ml-64">
        {/* Top bar */}
        <div className="bg-white shadow-sm border-b border-slate-200">
          <div className="flex items-center justify-between h-16 px-4">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setIsSidebarOpen(true)}
                className="lg:hidden p-2 rounded-md hover:bg-slate-100"
              >
                <Menu className="h-5 w-5" />
              </button>
              <h1 className="text-xl font-semibold text-slate-900">
                {navigationItems.find(item => item.id === activeTab)?.name || 'Admin Dashboard'}
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/')}
                className="flex items-center space-x-2 text-slate-600 hover:text-slate-900 transition-colors"
              >
                <Home className="h-4 w-4" />
                <span className="text-sm">Back to Site</span>
              </button>
            </div>
          </div>
        </div>

        {/* Page content */}
        <div className="p-6">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

// Placeholder components for each tab
const OverviewTab = ({ stats }) => (
  <div className="space-y-6">
    {/* Main Statistics */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Users className="h-6 w-6 text-blue-600" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-slate-600">Total Users</p>
            <p className="text-2xl font-bold text-slate-900">{stats.totalUsers}</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-2 bg-green-100 rounded-lg">
            <FileText className="h-6 w-6 text-green-600" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-slate-600">Total Cases</p>
            <p className="text-2xl font-bold text-slate-900">{stats.totalCases}</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-2 bg-purple-100 rounded-lg">
            <UserCheck className="h-6 w-6 text-purple-600" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-slate-600">Total People</p>
            <p className="text-2xl font-bold text-slate-900">{stats.totalPeople}</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-2 bg-orange-100 rounded-lg">
            <Building2 className="h-6 w-6 text-orange-600" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-slate-600">Total Banks</p>
            <p className="text-2xl font-bold text-slate-900">{stats.totalBanks}</p>
          </div>
        </div>
      </div>
    </div>

    {/* Secondary Statistics */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-2 bg-red-100 rounded-lg">
            <Shield className="h-6 w-6 text-red-600" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-slate-600">Insurance Companies</p>
            <p className="text-2xl font-bold text-slate-900">{stats.totalInsurance}</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-2 bg-indigo-100 rounded-lg">
            <Database className="h-6 w-6 text-indigo-600" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-slate-600">Companies</p>
            <p className="text-2xl font-bold text-slate-900">{stats.totalCompanies}</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-2 bg-yellow-100 rounded-lg">
            <CreditCard className="h-6 w-6 text-yellow-600" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-slate-600">Total Revenue</p>
            <p className="text-2xl font-bold text-slate-900">
              {stats.totalRevenue ? `GHS ${stats.totalRevenue.toLocaleString()}` : 'N/A'}
            </p>
          </div>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-2 bg-teal-100 rounded-lg">
            <Activity className="h-6 w-6 text-teal-600" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-slate-600">Active Subscriptions</p>
            <p className="text-2xl font-bold text-slate-900">{stats.activeSubscriptions}</p>
          </div>
        </div>
      </div>
    </div>

    {/* Risk and Analytics */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-2 bg-red-100 rounded-lg">
            <AlertCircle className="h-6 w-6 text-red-600" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-slate-600">High Risk People</p>
            <p className="text-2xl font-bold text-slate-900">{stats.highRiskCount}</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-2 bg-green-100 rounded-lg">
            <CheckCircle className="h-6 w-6 text-green-600" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-slate-600">Verified People</p>
            <p className="text-2xl font-bold text-slate-900">{stats.verifiedCount}</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-2 bg-blue-100 rounded-lg">
            <BarChart3 className="h-6 w-6 text-blue-600" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-slate-600">Avg Risk Score</p>
            <p className="text-2xl font-bold text-slate-900">{stats.avgRiskScore?.toFixed(1) || '0.0'}</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-2 bg-purple-100 rounded-lg">
            <Star className="h-6 w-6 text-purple-600" />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-slate-600">Avg Rating</p>
            <p className="text-2xl font-bold text-slate-900">{stats.avgRating?.toFixed(1) || '0.0'}</p>
          </div>
        </div>
      </div>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Recent Activity</h3>
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <p className="text-sm text-slate-600">New user registered</p>
            <span className="text-xs text-slate-400">2 minutes ago</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <p className="text-sm text-slate-600">New case added</p>
            <span className="text-xs text-slate-400">5 minutes ago</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
            <p className="text-sm text-slate-600">API key generated</p>
            <span className="text-xs text-slate-400">10 minutes ago</span>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">System Status</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-slate-600">Database</span>
            <span className="text-sm text-green-600 font-medium">Online</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-slate-600">API Server</span>
            <span className="text-sm text-green-600 font-medium">Online</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-slate-600">Frontend</span>
            <span className="text-sm text-green-600 font-medium">Online</span>
          </div>
        </div>
      </div>
    </div>
  </div>
);

const UsersTab = () => (
  <div className="bg-white rounded-lg shadow">
    <div className="p-6 border-b border-slate-200">
      <h3 className="text-lg font-semibold text-slate-900">User Management</h3>
      <p className="text-sm text-slate-600">Manage users, roles, and permissions</p>
    </div>
    <div className="p-6">
      <p className="text-slate-500">User management interface will be implemented here.</p>
    </div>
  </div>
);

const ApiKeysTab = () => (
  <div className="bg-white rounded-lg shadow">
    <div className="p-6 border-b border-slate-200">
      <h3 className="text-lg font-semibold text-slate-900">API Key Management</h3>
      <p className="text-sm text-slate-600">Generate and manage API keys for users</p>
    </div>
    <div className="p-6">
      <p className="text-slate-500">API key management interface will be implemented here.</p>
    </div>
  </div>
);

const CasesTab = () => (
  <div className="bg-white rounded-lg shadow">
    <div className="p-6 border-b border-slate-200">
      <h3 className="text-lg font-semibold text-slate-900">Case Management</h3>
      <p className="text-sm text-slate-600">Manage cases, metadata, analytics and statistics</p>
    </div>
    <div className="p-6">
      <p className="text-slate-500">Case management interface will be implemented here.</p>
    </div>
  </div>
);

const PeopleTab = () => (
  <div className="bg-white rounded-lg shadow">
    <div className="p-6 border-b border-slate-200">
      <h3 className="text-lg font-semibold text-slate-900">People Management</h3>
      <p className="text-sm text-slate-600">Manage people records and analytics</p>
    </div>
    <div className="p-6">
      <p className="text-slate-500">People management interface will be implemented here.</p>
    </div>
  </div>
);

const BanksTab = () => (
  <div className="bg-white rounded-lg shadow">
    <div className="p-6 border-b border-slate-200">
      <h3 className="text-lg font-semibold text-slate-900">Bank Management</h3>
      <p className="text-sm text-slate-600">Manage bank records and analytics</p>
    </div>
    <div className="p-6">
      <p className="text-slate-500">Bank management interface will be implemented here.</p>
    </div>
  </div>
);

const InsuranceTab = () => (
  <div className="bg-white rounded-lg shadow">
    <div className="p-6 border-b border-slate-200">
      <h3 className="text-lg font-semibold text-slate-900">Insurance Management</h3>
      <p className="text-sm text-slate-600">Manage insurance records and analytics</p>
    </div>
    <div className="p-6">
      <p className="text-slate-500">Insurance management interface will be implemented here.</p>
    </div>
  </div>
);

const CompaniesTab = () => (
  <div className="bg-white rounded-lg shadow">
    <div className="p-6 border-b border-slate-200">
      <h3 className="text-lg font-semibold text-slate-900">Company Management</h3>
      <p className="text-sm text-slate-600">Manage company records and analytics</p>
    </div>
    <div className="p-6">
      <p className="text-slate-500">Company management interface will be implemented here.</p>
    </div>
  </div>
);

const PaymentsTab = () => (
  <div className="bg-white rounded-lg shadow">
    <div className="p-6 border-b border-slate-200">
      <h3 className="text-lg font-semibold text-slate-900">Payment Management</h3>
      <p className="text-sm text-slate-600">Manage payments and subscriptions</p>
    </div>
    <div className="p-6">
      <p className="text-slate-500">Payment management interface will be implemented here.</p>
    </div>
  </div>
);

const SettingsTab = () => (
  <div className="bg-white rounded-lg shadow">
    <div className="p-6 border-b border-slate-200">
      <h3 className="text-lg font-semibold text-slate-900">System Settings</h3>
      <p className="text-sm text-slate-600">Configure system settings and preferences</p>
    </div>
    <div className="p-6">
      <p className="text-slate-500">System settings interface will be implemented here.</p>
    </div>
  </div>
);

export default AdminDashboard;
