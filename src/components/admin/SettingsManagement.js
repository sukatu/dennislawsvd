import React, { useState, useEffect } from 'react';
import { 
  Settings as SettingsIcon, 
  Plus, 
  Edit, 
  Trash2, 
  Search, 
  Filter, 
  Eye,
  EyeOff,
  Lock,
  Unlock,
  AlertCircle,
  CheckCircle,
  XCircle
} from 'lucide-react';

const SettingsManagement = () => {
  const [settings, setSettings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({});
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalSettings, setTotalSettings] = useState(0);
  
  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [isPublicFilter, setIsPublicFilter] = useState('');
  const [isEditableFilter, setIsEditableFilter] = useState('');
  
  // Modals
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingSetting, setEditingSetting] = useState(null);

  useEffect(() => {
    loadSettings();
    loadStats();
  }, [currentPage, searchTerm, categoryFilter, isPublicFilter, isEditableFilter]);

  const loadSettings = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams({
        page: currentPage,
        limit: 10,
        ...(searchTerm && { search: searchTerm }),
        ...(categoryFilter && { category: categoryFilter }),
        ...(isPublicFilter !== '' && { is_public: isPublicFilter }),
        ...(isEditableFilter !== '' && { is_editable: isEditableFilter })
      });
      
      const response = await fetch(`/api/admin/settings?${params}`);
      if (!response.ok) throw new Error('Failed to fetch settings');
      
      const data = await response.json();
      setSettings(data.settings || []);
      setTotalPages(data.total_pages || 1);
      setTotalSettings(data.total || 0);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await fetch('/api/admin/settings/stats');
      if (!response.ok) throw new Error('Failed to fetch stats');
      
      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error('Error loading stats:', err);
    }
  };

  const handleCreateSetting = () => {
    setEditingSetting(null);
    setShowCreateModal(true);
  };

  const handleEditSetting = (setting) => {
    setEditingSetting(setting);
    setShowEditModal(true);
  };

  const handleSaveSetting = async (settingData) => {
    try {
      const url = editingSetting 
        ? `/api/admin/settings/${editingSetting.id}`
        : '/api/admin/settings';
      
      const method = editingSetting ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settingData),
      });
      
      if (!response.ok) throw new Error('Failed to save setting');
      
      setShowCreateModal(false);
      setShowEditModal(false);
      setEditingSetting(null);
      loadSettings();
      loadStats();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteSetting = async (settingId) => {
    if (!window.confirm('Are you sure you want to delete this setting?')) return;
    
    try {
      const response = await fetch(`/api/admin/settings/${settingId}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) throw new Error('Failed to delete setting');
      
      loadSettings();
      loadStats();
    } catch (err) {
      setError(err.message);
    }
  };

  const getValueTypeIcon = (type) => {
    switch (type) {
      case 'string':
        return <span className="text-blue-500">📝</span>;
      case 'number':
        return <span className="text-green-500">🔢</span>;
      case 'boolean':
        return <span className="text-purple-500">✅</span>;
      case 'json':
        return <span className="text-orange-500">📋</span>;
      case 'array':
        return <span className="text-pink-500">📊</span>;
      default:
        return <span className="text-gray-500">❓</span>;
    }
  };

  const formatValue = (value, type) => {
    if (!value) return 'Not set';
    
    switch (type) {
      case 'boolean':
        return value === 'true' ? 'Yes' : 'No';
      case 'json':
        try {
          return JSON.stringify(JSON.parse(value), null, 2);
        } catch {
          return value;
        }
      case 'array':
        try {
          const arr = JSON.parse(value);
          return Array.isArray(arr) ? arr.join(', ') : value;
        } catch {
          return value;
        }
      default:
        return value;
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      'general': 'bg-blue-100 text-blue-800',
      'payment': 'bg-green-100 text-green-800',
      'email': 'bg-purple-100 text-purple-800',
      'security': 'bg-red-100 text-red-800',
      'api': 'bg-yellow-100 text-yellow-800',
      'ui': 'bg-pink-100 text-pink-800',
      'database': 'bg-indigo-100 text-indigo-800',
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  if (loading && settings.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-sky-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Settings Management</h2>
          <p className="text-slate-600">Manage system configuration and settings</p>
        </div>
        <button
          onClick={handleCreateSetting}
          className="flex items-center space-x-2 bg-sky-600 text-white px-4 py-2 rounded-lg hover:bg-sky-700 transition-colors"
        >
          <Plus className="h-4 w-4" />
          <span>Create Setting</span>
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <SettingsIcon className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-slate-600">Total Settings</p>
              <p className="text-2xl font-bold text-slate-900">{stats.total_settings || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <Eye className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-slate-600">Public Settings</p>
              <p className="text-2xl font-bold text-slate-900">{stats.public_settings || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <Edit className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-slate-600">Editable</p>
              <p className="text-2xl font-bold text-slate-900">{stats.editable_settings || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-red-100 rounded-lg">
              <AlertCircle className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-slate-600">Required</p>
              <p className="text-2xl font-bold text-slate-900">{stats.required_settings || 0}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow-sm border">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="lg:col-span-2">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
              <input
                type="text"
                placeholder="Search settings..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
              />
            </div>
          </div>
          <div>
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
            >
              <option value="">All Categories</option>
              <option value="general">General</option>
              <option value="payment">Payment</option>
              <option value="email">Email</option>
              <option value="security">Security</option>
              <option value="api">API</option>
              <option value="ui">UI</option>
              <option value="database">Database</option>
            </select>
          </div>
          <div>
            <select
              value={isPublicFilter}
              onChange={(e) => setIsPublicFilter(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
            >
              <option value="">All Visibility</option>
              <option value="true">Public</option>
              <option value="false">Private</option>
            </select>
          </div>
          <div>
            <select
              value={isEditableFilter}
              onChange={(e) => setIsEditableFilter(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
            >
              <option value="">All Editability</option>
              <option value="true">Editable</option>
              <option value="false">Read-only</option>
            </select>
          </div>
        </div>
      </div>

      {/* Settings Table */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Key
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Category
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Value
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Properties
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-200">
              {settings.map((setting) => (
                <tr key={setting.id} className="hover:bg-slate-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-slate-900">{setting.key}</div>
                    {setting.description && (
                      <div className="text-sm text-slate-500">{setting.description}</div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getCategoryColor(setting.category)}`}>
                      {setting.category}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-slate-900 max-w-xs truncate">
                      {formatValue(setting.value, setting.value_type)}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center space-x-1">
                      {getValueTypeIcon(setting.value_type)}
                      <span className="text-sm text-slate-900 capitalize">{setting.value_type}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex space-x-1">
                      {setting.is_public && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          <Eye className="h-3 w-3 mr-1" />
                          Public
                        </span>
                      )}
                      {!setting.is_editable && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                          <Lock className="h-3 w-3 mr-1" />
                          Read-only
                        </span>
                      )}
                      {setting.is_required && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                          <AlertCircle className="h-3 w-3 mr-1" />
                          Required
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEditSetting(setting)}
                        disabled={!setting.is_editable}
                        className="text-sky-600 hover:text-sky-900 disabled:text-gray-400 disabled:cursor-not-allowed"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteSetting(setting.id)}
                        disabled={setting.is_required}
                        className="text-red-600 hover:text-red-900 disabled:text-gray-400 disabled:cursor-not-allowed"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-slate-200 sm:px-6">
          <div className="flex-1 flex justify-between sm:hidden">
            <button
              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
              className="relative inline-flex items-center px-4 py-2 border border-slate-300 text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 disabled:opacity-50"
            >
              Previous
            </button>
            <button
              onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
              disabled={currentPage === totalPages}
              className="ml-3 relative inline-flex items-center px-4 py-2 border border-slate-300 text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 disabled:opacity-50"
            >
              Next
            </button>
          </div>
          <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-slate-700">
                Showing <span className="font-medium">{((currentPage - 1) * 10) + 1}</span> to{' '}
                <span className="font-medium">{Math.min(currentPage * 10, totalSettings)}</span> of{' '}
                <span className="font-medium">{totalSettings}</span> results
              </p>
            </div>
            <div>
              <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-slate-300 bg-white text-sm font-medium text-slate-500 hover:bg-slate-50 disabled:opacity-50"
                >
                  Previous
                </button>
                <button
                  onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                  className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-slate-300 bg-white text-sm font-medium text-slate-500 hover:bg-slate-50 disabled:opacity-50"
                >
                  Next
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>

      {/* Setting Form Modal */}
      {(showCreateModal || showEditModal) && (
        <SettingForm
          setting={editingSetting}
          onSave={handleSaveSetting}
          onCancel={() => {
            setShowCreateModal(false);
            setShowEditModal(false);
            setEditingSetting(null);
          }}
        />
      )}
    </div>
  );
};

// Setting Form Component
const SettingForm = ({ setting, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    key: '',
    category: 'general',
    value: '',
    value_type: 'string',
    description: '',
    is_public: false,
    is_editable: true,
    is_required: false,
    validation_rules: '',
    default_value: ''
  });

  useEffect(() => {
    if (setting) {
      setFormData({
        key: setting.key || '',
        category: setting.category || 'general',
        value: setting.value || '',
        value_type: setting.value_type || 'string',
        description: setting.description || '',
        is_public: setting.is_public || false,
        is_editable: setting.is_editable !== undefined ? setting.is_editable : true,
        is_required: setting.is_required || false,
        validation_rules: setting.validation_rules ? JSON.stringify(setting.validation_rules, null, 2) : '',
        default_value: setting.default_value || ''
      });
    }
  }, [setting]);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const submitData = {
      ...formData,
      validation_rules: formData.validation_rules ? JSON.parse(formData.validation_rules) : null
    };
    
    onSave(submitData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">
          {setting ? 'Edit Setting' : 'Create Setting'}
        </h3>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Key *</label>
              <input
                type="text"
                name="key"
                value={formData.key}
                onChange={handleInputChange}
                required
                disabled={!!setting}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 disabled:bg-slate-100"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Category *</label>
              <select
                name="category"
                value={formData.category}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
              >
                <option value="general">General</option>
                <option value="payment">Payment</option>
                <option value="email">Email</option>
                <option value="security">Security</option>
                <option value="api">API</option>
                <option value="ui">UI</option>
                <option value="database">Database</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Value Type *</label>
              <select
                name="value_type"
                value={formData.value_type}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
              >
                <option value="string">String</option>
                <option value="number">Number</option>
                <option value="boolean">Boolean</option>
                <option value="json">JSON</option>
                <option value="array">Array</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Default Value</label>
              <input
                type="text"
                name="default_value"
                value={formData.default_value}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Value</label>
            <textarea
              name="value"
              value={formData.value}
              onChange={handleInputChange}
              rows={3}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Description</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows={2}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Validation Rules (JSON)</label>
            <textarea
              name="validation_rules"
              value={formData.validation_rules}
              onChange={handleInputChange}
              rows={3}
              placeholder='{"min": 0, "max": 100, "pattern": "^[a-zA-Z]+$"}'
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500"
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <label className="flex items-center">
              <input
                type="checkbox"
                name="is_public"
                checked={formData.is_public}
                onChange={handleInputChange}
                className="h-4 w-4 text-sky-600 focus:ring-sky-500 border-slate-300 rounded"
              />
              <span className="ml-2 text-sm text-slate-700">Public</span>
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                name="is_editable"
                checked={formData.is_editable}
                onChange={handleInputChange}
                className="h-4 w-4 text-sky-600 focus:ring-sky-500 border-slate-300 rounded"
              />
              <span className="ml-2 text-sm text-slate-700">Editable</span>
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                name="is_required"
                checked={formData.is_required}
                onChange={handleInputChange}
                className="h-4 w-4 text-sky-600 focus:ring-sky-500 border-slate-300 rounded"
              />
              <span className="ml-2 text-sm text-slate-700">Required</span>
            </label>
          </div>
          
          <div className="flex justify-end space-x-3 pt-4 border-t">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 text-slate-700 bg-slate-100 rounded-lg hover:bg-slate-200 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 transition-colors"
            >
              {setting ? 'Update Setting' : 'Create Setting'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SettingsManagement;
