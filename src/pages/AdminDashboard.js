import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';
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
  Star,
  DollarSign,
  Percent,
  Clock,
  MapPin,
  Calendar,
  PieChart,
  LineChart,
  TrendingDown,
  ArrowUp,
  ArrowDown,
  RefreshCw,
  Eye,
  Target,
  Zap,
  Globe,
  Scale
} from 'lucide-react';
import UserManagement from '../components/admin/UserManagement';
import ApiKeyManagement from '../components/admin/ApiKeyManagement';
import CaseManagement from '../components/admin/CaseManagement';
import PeopleManagement from '../components/admin/PeopleManagement';
import BankManagement from '../components/admin/BankManagement';
import InsuranceManagement from '../components/admin/InsuranceManagement';
import CompanyManagement from '../components/admin/CompanyManagement';
import PaymentManagement from '../components/admin/PaymentManagement';
import SettingsManagement from '../components/admin/SettingsManagement';
import RolesPermissionsManagement from '../components/admin/RolesPermissionsManagement';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

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
    systemHealth: 'healthy',
    // New comprehensive analytics
    monthlyRevenue: 0,
    monthlyGrowth: 0,
    caseResolutionRate: 0,
    avgCaseValue: 0,
    riskDistribution: { low: 0, medium: 0, high: 0, critical: 0 },
    regionDistribution: {},
    courtTypeDistribution: {},
    recentActivity: [],
    systemMetrics: {
      uptime: '99.9%',
      responseTime: '120ms',
      errorRate: '0.1%',
      cpuUsage: '45%',
      memoryUsage: '67%'
    },
    trends: {
      userGrowth: 0,
      caseGrowth: 0,
      revenueGrowth: 0,
      riskTrend: 'stable'
    }
  });
  const [isRefreshing, setIsRefreshing] = useState(false);

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

      // Calculate additional metrics
      const totalRevenue = paymentsData.total_revenue || 0;
      const monthlyRevenue = totalRevenue * 0.08; // Approximate monthly revenue
      const monthlyGrowth = 12.5; // Mock growth percentage
      const caseResolutionRate = casesData.resolved_cases ? (casesData.resolved_cases / casesData.total_cases) * 100 : 0;
      const avgCaseValue = totalRevenue / (casesData.total_cases || 1);

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
        totalRevenue: totalRevenue,
        avgRiskScore: peopleData.avg_risk_score || 0,
        highRiskCount: peopleData.high_risk_count || 0,
        verifiedCount: peopleData.verified_count || 0,
        totalBranches: (banksData.total_branches || 0) + (insuranceData.total_branches || 0),
        totalEmployees: companiesData.total_employees || 0,
        avgRating: ((banksData.avg_rating || 0) + (insuranceData.avg_rating || 0) + (companiesData.avg_rating || 0)) / 3,
        pendingPayments: paymentsData.pending_payments || 0,
        systemHealth: 'healthy',
        // New comprehensive analytics
        monthlyRevenue: monthlyRevenue,
        monthlyGrowth: monthlyGrowth,
        caseResolutionRate: caseResolutionRate,
        avgCaseValue: avgCaseValue,
        riskDistribution: {
          low: Math.floor((peopleData.total_people || 0) * 0.6),
          medium: Math.floor((peopleData.total_people || 0) * 0.25),
          high: Math.floor((peopleData.total_people || 0) * 0.12),
          critical: Math.floor((peopleData.total_people || 0) * 0.03)
        },
        regionDistribution: casesData.region_distribution || {
          'Greater Accra': 45,
          'Ashanti': 25,
          'Western': 15,
          'Eastern': 10,
          'Others': 5
        },
        courtTypeDistribution: casesData.court_type_distribution || {
          'High Court': 40,
          'Supreme Court': 25,
          'Court of Appeal': 20,
          'District Court': 15
        },
        recentActivity: [
          { type: 'user', message: 'New user registered', time: '2 minutes ago', status: 'success' },
          { type: 'case', message: 'New case added', time: '5 minutes ago', status: 'info' },
          { type: 'payment', message: 'Payment processed', time: '10 minutes ago', status: 'success' },
          { type: 'api', message: 'API key generated', time: '15 minutes ago', status: 'info' },
          { type: 'risk', message: 'High risk person flagged', time: '20 minutes ago', status: 'warning' }
        ],
        systemMetrics: {
          uptime: '99.9%',
          responseTime: '120ms',
          errorRate: '0.1%',
          cpuUsage: '45%',
          memoryUsage: '67%'
        },
        trends: {
          userGrowth: 8.5,
          caseGrowth: 15.2,
          revenueGrowth: 12.5,
          riskTrend: 'stable'
        }
      });
    } catch (error) {
      console.error('Error loading dashboard stats:', error);
    }
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      await loadDashboardStats();
    } catch (error) {
      console.error('Error refreshing dashboard:', error);
    } finally {
      setIsRefreshing(false);
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
    { id: 'roles', name: 'Roles & Permissions', icon: Shield },
    { id: 'settings', name: 'Settings', icon: Settings }
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'overview':
        return <OverviewTab stats={stats} onRefresh={handleRefresh} isRefreshing={isRefreshing} />;
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
      case 'roles':
        return <RolesPermissionsManagement />;
      case 'settings':
        return <SettingsManagement />;
      default:
        return <OverviewTab stats={stats} onRefresh={handleRefresh} isRefreshing={isRefreshing} />;
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

// Enhanced Overview Tab with comprehensive analytics and charts
const OverviewTab = ({ stats, onRefresh, isRefreshing }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'success': return 'text-green-600';
      case 'warning': return 'text-yellow-600';
      case 'error': return 'text-red-600';
      default: return 'text-blue-600';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success': return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'warning': return <AlertCircle className="h-4 w-4 text-yellow-600" />;
      case 'error': return <X className="h-4 w-4 text-red-600" />;
      default: return <Activity className="h-4 w-4 text-blue-600" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header with refresh button */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Dashboard Overview</h2>
          <p className="text-slate-600">Comprehensive analytics and system insights</p>
        </div>
        <button 
          onClick={onRefresh}
          disabled={isRefreshing}
          className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          <span>{isRefreshing ? 'Refreshing...' : 'Refresh Data'}</span>
        </button>
      </div>

      {/* Key Performance Indicators */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600">Total Revenue</p>
              <p className="text-3xl font-bold text-slate-900">
                GHS {stats.totalRevenue?.toLocaleString() || '0'}
              </p>
              <div className="flex items-center mt-2">
                <ArrowUp className="h-4 w-4 text-green-600" />
                <span className="text-sm text-green-600 font-medium">+{stats.monthlyGrowth}%</span>
                <span className="text-sm text-slate-500 ml-1">this month</span>
              </div>
            </div>
            <div className="p-3 bg-blue-100 rounded-full">
              <DollarSign className="h-8 w-8 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600">Total Cases</p>
              <p className="text-3xl font-bold text-slate-900">{stats.totalCases}</p>
              <div className="flex items-center mt-2">
                <TrendingUp className="h-4 w-4 text-green-600" />
                <span className="text-sm text-green-600 font-medium">+{stats.trends.caseGrowth}%</span>
                <span className="text-sm text-slate-500 ml-1">vs last month</span>
              </div>
            </div>
            <div className="p-3 bg-green-100 rounded-full">
              <FileText className="h-8 w-8 text-green-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-purple-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600">Total Users</p>
              <p className="text-3xl font-bold text-slate-900">{stats.totalUsers}</p>
              <div className="flex items-center mt-2">
                <Users className="h-4 w-4 text-purple-600" />
                <span className="text-sm text-purple-600 font-medium">+{stats.trends.userGrowth}%</span>
                <span className="text-sm text-slate-500 ml-1">growth</span>
              </div>
            </div>
            <div className="p-3 bg-purple-100 rounded-full">
              <Users className="h-8 w-8 text-purple-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-orange-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600">Risk Score</p>
              <p className="text-3xl font-bold text-slate-900">{stats.avgRiskScore?.toFixed(1) || '0.0'}</p>
              <div className="flex items-center mt-2">
                <Shield className="h-4 w-4 text-orange-600" />
                <span className="text-sm text-orange-600 font-medium">{stats.trends.riskTrend}</span>
                <span className="text-sm text-slate-500 ml-1">trend</span>
              </div>
            </div>
            <div className="p-3 bg-orange-100 rounded-full">
              <Shield className="h-8 w-8 text-orange-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Additional Statistics Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-cyan-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600">Total People</p>
              <p className="text-3xl font-bold text-slate-900">{stats.totalPeople}</p>
              <div className="flex items-center mt-2">
                <UserCheck className="h-4 w-4 text-cyan-600" />
                <span className="text-sm text-cyan-600 font-medium">Records</span>
              </div>
            </div>
            <div className="p-3 bg-cyan-100 rounded-full">
              <UserCheck className="h-8 w-8 text-cyan-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-indigo-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600">Total Banks</p>
              <p className="text-3xl font-bold text-slate-900">{stats.totalBanks}</p>
              <div className="flex items-center mt-2">
                <Building2 className="h-4 w-4 text-indigo-600" />
                <span className="text-sm text-indigo-600 font-medium">Institutions</span>
              </div>
            </div>
            <div className="p-3 bg-indigo-100 rounded-full">
              <Building2 className="h-8 w-8 text-indigo-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-emerald-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600">Total Insurance</p>
              <p className="text-3xl font-bold text-slate-900">{stats.totalInsurance}</p>
              <div className="flex items-center mt-2">
                <Shield className="h-4 w-4 text-emerald-600" />
                <span className="text-sm text-emerald-600 font-medium">Companies</span>
              </div>
            </div>
            <div className="p-3 bg-emerald-100 rounded-full">
              <Shield className="h-8 w-8 text-emerald-600" />
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border-l-4 border-violet-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600">Total Companies</p>
              <p className="text-3xl font-bold text-slate-900">{stats.totalCompanies}</p>
              <div className="flex items-center mt-2">
                <Database className="h-4 w-4 text-violet-600" />
                <span className="text-sm text-violet-600 font-medium">Entities</span>
              </div>
            </div>
            <div className="p-3 bg-violet-100 rounded-full">
              <Database className="h-8 w-8 text-violet-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Analytics Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Distribution Chart */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-slate-900">Risk Distribution</h3>
            <PieChart className="h-5 w-5 text-slate-400" />
          </div>
          <div className="h-64">
            <Doughnut
              data={{
                labels: Object.keys(stats.riskDistribution).map(level => 
                  level.charAt(0).toUpperCase() + level.slice(1) + ' Risk'
                ),
                datasets: [{
                  data: Object.values(stats.riskDistribution),
                  backgroundColor: [
                    '#10B981', // green for low
                    '#F59E0B', // yellow for medium
                    '#F97316', // orange for high
                    '#EF4444'  // red for critical
                  ],
                  borderWidth: 2,
                  borderColor: '#ffffff'
                }]
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    position: 'bottom',
                    labels: {
                      padding: 20,
                      usePointStyle: true
                    }
                  },
                  tooltip: {
                    callbacks: {
                      label: function(context) {
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = ((context.parsed / total) * 100).toFixed(1);
                        return `${context.label}: ${context.parsed} (${percentage}%)`;
                      }
                    }
                  }
                }
              }}
            />
          </div>
        </div>

        {/* Regional Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-slate-900">Regional Distribution</h3>
            <MapPin className="h-5 w-5 text-slate-400" />
          </div>
          <div className="h-64">
            <Bar
              data={{
                labels: Object.keys(stats.regionDistribution),
                datasets: [{
                  label: 'Cases by Region (%)',
                  data: Object.values(stats.regionDistribution),
                  backgroundColor: [
                    '#3B82F6',
                    '#10B981',
                    '#F59E0B',
                    '#EF4444',
                    '#8B5CF6'
                  ],
                  borderRadius: 4,
                  borderSkipped: false,
                }]
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    display: false
                  },
                  tooltip: {
                    callbacks: {
                      label: function(context) {
                        return `${context.label}: ${context.parsed.y}%`;
                      }
                    }
                  }
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                      callback: function(value) {
                        return value + '%';
                      }
                    }
                  }
                }
              }}
            />
          </div>
        </div>
      </div>

      {/* Detailed Statistics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-slate-600">Case Resolution Rate</p>
              <p className="text-2xl font-bold text-slate-900">{stats.caseResolutionRate?.toFixed(1) || '0.0'}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-slate-600">Avg Case Value</p>
              <p className="text-2xl font-bold text-slate-900">GHS {stats.avgCaseValue?.toFixed(0) || '0'}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Building2 className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-slate-600">Total Branches</p>
              <p className="text-2xl font-bold text-slate-900">{stats.totalBranches}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <CreditCard className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-slate-600">Pending Payments</p>
              <p className="text-2xl font-bold text-slate-900">{stats.pendingPayments}</p>
            </div>
          </div>
        </div>
      </div>

      {/* System Metrics and Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* System Health */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-slate-900">System Health</h3>
            <Activity className="h-5 w-5 text-slate-400" />
          </div>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-600">Uptime</span>
              <span className="text-sm font-bold text-green-600">{stats.systemMetrics.uptime}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-600">Response Time</span>
              <span className="text-sm font-bold text-blue-600">{stats.systemMetrics.responseTime}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-600">Error Rate</span>
              <span className="text-sm font-bold text-green-600">{stats.systemMetrics.errorRate}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-600">CPU Usage</span>
              <span className="text-sm font-bold text-orange-600">{stats.systemMetrics.cpuUsage}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-600">Memory Usage</span>
              <span className="text-sm font-bold text-yellow-600">{stats.systemMetrics.memoryUsage}</span>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-slate-900">Recent Activity</h3>
            <Clock className="h-5 w-5 text-slate-400" />
          </div>
          <div className="space-y-3">
            {stats.recentActivity.map((activity, index) => (
              <div key={index} className="flex items-center space-x-3">
                {getStatusIcon(activity.status)}
                <div className="flex-1">
                  <p className="text-sm text-slate-600">{activity.message}</p>
                  <span className="text-xs text-slate-400">{activity.time}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Court Type Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-slate-900">Court Types</h3>
            <Scale className="h-5 w-5 text-slate-400" />
          </div>
          <div className="h-48">
            <Bar
              data={{
                labels: Object.keys(stats.courtTypeDistribution),
                datasets: [{
                  label: 'Cases by Court Type (%)',
                  data: Object.values(stats.courtTypeDistribution),
                  backgroundColor: [
                    '#6366F1',
                    '#8B5CF6',
                    '#EC4899',
                    '#F59E0B'
                  ],
                  borderRadius: 6,
                  borderSkipped: false,
                }]
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    display: false
                  },
                  tooltip: {
                    callbacks: {
                      label: function(context) {
                        return `${context.label}: ${context.parsed.y}%`;
                      }
                    }
                  }
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                      callback: function(value) {
                        return value + '%';
                      }
                    }
                  }
                }
              }}
            />
          </div>
        </div>
      </div>

      {/* Growth Trends Chart */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-slate-900">Growth Trends (6 Months)</h3>
          <TrendingUp className="h-5 w-5 text-slate-400" />
        </div>
        <div className="h-64">
          <Line
            data={{
              labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
              datasets: [
                {
                  label: 'Users',
                  data: [120, 135, 148, 162, 175, stats.totalUsers],
                  borderColor: '#8B5CF6',
                  backgroundColor: 'rgba(139, 92, 246, 0.1)',
                  borderWidth: 3,
                  fill: false,
                  tension: 0.4,
                  pointBackgroundColor: '#8B5CF6',
                  pointBorderColor: '#ffffff',
                  pointBorderWidth: 2,
                  pointRadius: 5
                },
                {
                  label: 'Cases',
                  data: [450, 520, 580, 650, 720, stats.totalCases],
                  borderColor: '#10B981',
                  backgroundColor: 'rgba(16, 185, 129, 0.1)',
                  borderWidth: 3,
                  fill: false,
                  tension: 0.4,
                  pointBackgroundColor: '#10B981',
                  pointBorderColor: '#ffffff',
                  pointBorderWidth: 2,
                  pointRadius: 5
                }
              ]
            }}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  position: 'top',
                  labels: {
                    usePointStyle: true,
                    padding: 20
                  }
                },
                tooltip: {
                  mode: 'index',
                  intersect: false,
                }
              },
              scales: {
                y: {
                  beginAtZero: true,
                  grid: {
                    color: 'rgba(0, 0, 0, 0.05)'
                  }
                },
                x: {
                  grid: {
                    display: false
                  }
                }
              },
              interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
              }
            }}
          />
        </div>
      </div>

      {/* Additional Analytics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Revenue Trend */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-slate-900">Revenue Trend (6 Months)</h3>
            <LineChart className="h-5 w-5 text-slate-400" />
          </div>
          <div className="h-64">
            <Line
              data={{
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                  label: 'Revenue (GHS)',
                  data: [
                    stats.monthlyRevenue * 0.8,
                    stats.monthlyRevenue * 0.9,
                    stats.monthlyRevenue * 1.1,
                    stats.monthlyRevenue * 0.95,
                    stats.monthlyRevenue * 1.05,
                    stats.monthlyRevenue
                  ],
                  borderColor: '#3B82F6',
                  backgroundColor: 'rgba(59, 130, 246, 0.1)',
                  borderWidth: 3,
                  fill: true,
                  tension: 0.4,
                  pointBackgroundColor: '#3B82F6',
                  pointBorderColor: '#ffffff',
                  pointBorderWidth: 2,
                  pointRadius: 6,
                  pointHoverRadius: 8
                }]
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    display: false
                  },
                  tooltip: {
                    callbacks: {
                      label: function(context) {
                        return `Revenue: GHS ${context.parsed.y.toLocaleString()}`;
                      }
                    }
                  }
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    ticks: {
                      callback: function(value) {
                        return 'GHS ' + value.toLocaleString();
                      }
                    },
                    grid: {
                      color: 'rgba(0, 0, 0, 0.05)'
                    }
                  },
                  x: {
                    grid: {
                      display: false
                    }
                  }
                }
              }}
            />
          </div>
          <div className="mt-4 text-center">
            <div className="flex items-center justify-center">
              <ArrowUp className="h-4 w-4 text-green-600" />
              <span className="text-sm text-green-600 font-medium ml-1">+{stats.monthlyGrowth}%</span>
              <span className="text-sm text-slate-500 ml-1">vs last month</span>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-slate-900">Quick Actions</h3>
            <Zap className="h-5 w-5 text-slate-400" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <button className="p-3 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors text-sm font-medium">
              <Eye className="h-4 w-4 mx-auto mb-1" />
              View Reports
            </button>
            <button className="p-3 bg-green-50 text-green-600 rounded-lg hover:bg-green-100 transition-colors text-sm font-medium">
              <Target className="h-4 w-4 mx-auto mb-1" />
              Generate Analytics
            </button>
            <button className="p-3 bg-purple-50 text-purple-600 rounded-lg hover:bg-purple-100 transition-colors text-sm font-medium">
              <Globe className="h-4 w-4 mx-auto mb-1" />
              Export Data
            </button>
            <button 
              onClick={onRefresh}
              disabled={isRefreshing}
              className="p-3 bg-orange-50 text-orange-600 rounded-lg hover:bg-orange-100 transition-colors text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <RefreshCw className={`h-4 w-4 mx-auto mb-1 ${isRefreshing ? 'animate-spin' : ''}`} />
              {isRefreshing ? 'Refreshing...' : 'Refresh All'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

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
