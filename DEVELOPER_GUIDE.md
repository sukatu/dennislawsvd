# Juridence Legal Database System - Developer Guide

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [API Documentation](#api-documentation)
4. [Authentication](#authentication)
5. [SDK Examples](#sdk-examples)
6. [Error Handling](#error-handling)
7. [Rate Limits](#rate-limits)
8. [Best Practices](#best-practices)
9. [Testing](#testing)
10. [Deployment](#deployment)

## Overview

The Juridence Legal Database System is a comprehensive legal database providing access to:
- **11,911+ Legal Cases** with detailed information
- **6,331+ People** with case statistics and risk analysis
- **34 Banks** with financial data and services
- **49 Insurance Companies** with coverage information
- **4,829+ Companies** with corporate data and directors

### Key Features
- 🔍 **Unified Search** across all legal entities
- 🤖 **AI-Powered Analysis** using GPT-4
- 📊 **Real-time Analytics** and reporting
- 🔐 **Secure API** with role-based access
- 🌐 **RESTful API** for easy integration
- 📱 **Multi-platform Support**

## Getting Started

### Prerequisites
- API Key (contact admin for access)
- HTTP client library (axios, requests, curl, etc.)
- Basic understanding of REST APIs

### Quick Start

1. **Get your API Key**
   ```bash
   # Contact admin to generate API key
   # Or use admin dashboard: Admin → API Keys → Generate New Key
   ```

2. **Test your connection**
   ```bash
   curl -X GET "https://api.juridence.com/api/search/quick?query=test" \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```

3. **Start building**
   ```javascript
   const response = await fetch('https://api.juridence.com/api/search/unified?query=mahama', {
     headers: {
       'Authorization': 'Bearer YOUR_API_KEY',
       'Content-Type': 'application/json'
     }
   });
   const data = await response.json();
   ```

## API Documentation

### Base URL
```
https://api.juridence.com
```

### Authentication
All API requests require authentication using a Bearer token:

```http
Authorization: Bearer your-api-key-here
```

### Core Endpoints

#### Search Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/search/unified` | Search across all entities |
| `GET` | `/api/search/quick` | Quick search for autocomplete |
| `GET` | `/api/case-search/search` | Search legal cases |
| `GET` | `/api/people/search` | Search people |
| `GET` | `/api/banks/search` | Search banks |
| `GET` | `/api/companies/search` | Search companies |
| `GET` | `/api/insurance/search` | Search insurance companies |

#### Entity Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/cases/{id}` | Get case details |
| `GET` | `/api/people/{id}` | Get person details |
| `GET` | `/api/banks/{id}` | Get bank details |
| `POST` | `/api/banks` | Create bank |
| `PUT` | `/api/banks/{id}` | Update bank |
| `DELETE` | `/api/banks/{id}` | Delete bank |

#### AI Integration
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ai-chat/message` | Send message to AI |
| `POST` | `/api/ai-chat/case-summary` | Generate case summary |
| `GET` | `/api/ai-chat/analytics` | Get AI usage analytics |

### Example Requests

#### Search for Cases
```bash
curl -X GET "https://api.juridence.com/api/search/unified?query=mahama&limit=10" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Get Case Details
```bash
curl -X GET "https://api.juridence.com/api/cases/6490" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### Create New Bank
```bash
curl -X POST "https://api.juridence.com/api/banks" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Bank Ltd",
    "bank_code": "NEW001",
    "license_number": "BOG999",
    "country": "Ghana"
  }'
```

## Authentication

### API Key Generation

1. **Admin Dashboard Method**
   - Login to admin dashboard
   - Navigate to "API Keys" section
   - Click "Generate New Key"
   - Provide key name and permissions
   - Copy and store securely

2. **Programmatic Method** (Admin only)
   ```python
   from backend.services.api_key_service import ApiKeyService
   
   service = ApiKeyService(db)
   api_key = service.generate_api_key(
       name="My App",
       permissions=["read", "write"],
       user_id=1
   )
   ```

### Key Management

- **View Keys**: List all active API keys
- **Regenerate**: Create new key to replace old one
- **Revoke**: Immediately disable compromised key
- **Monitor**: Track usage and rate limits

## SDK Examples

### JavaScript/Node.js

```javascript
class JuridenceAPI {
  constructor(apiKey, baseURL = 'https://api.juridence.com') {
    this.apiKey = apiKey;
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    };

    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Search methods
  async searchUnified(query, limit = 20, page = 1) {
    return this.request(`/api/search/unified?query=${encodeURIComponent(query)}&limit=${limit}&page=${page}`);
  }

  async searchCases(query, limit = 20) {
    return this.request(`/api/case-search/search?query=${encodeURIComponent(query)}&limit=${limit}`);
  }

  async searchPeople(query, limit = 20) {
    return this.request(`/api/people/search?query=${encodeURIComponent(query)}&limit=${limit}`);
  }

  // Entity methods
  async getCase(id) {
    return this.request(`/api/cases/${id}`);
  }

  async getPerson(id) {
    return this.request(`/api/people/${id}`);
  }

  async getBank(id) {
    return this.request(`/api/banks/${id}`);
  }

  // AI methods
  async sendAIMessage(message, caseId, sessionId = null) {
    return this.request('/api/ai-chat/message', {
      method: 'POST',
      body: JSON.stringify({
        message,
        case_id: caseId,
        session_id: sessionId
      })
    });
  }

  async generateCaseSummary(caseId, userId = 1) {
    return this.request('/api/ai-chat/case-summary', {
      method: 'POST',
      body: JSON.stringify({
        case_id: caseId,
        user_id: userId
      })
    });
  }
}

// Usage
const api = new JuridenceAPI('your-api-key-here');

// Search for cases
const cases = await api.searchCases('mahama', 10);
console.log(cases);

// Get case details
const caseDetails = await api.getCase(6490);
console.log(caseDetails);

// AI analysis
const aiResponse = await api.sendAIMessage('Analyze this case', 6490);
console.log(aiResponse);
```

### Python

```python
import requests
from typing import Dict, List, Optional

class JuridenceAPI:
    def __init__(self, api_key: str, base_url: str = 'https://api.juridence.com'):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def search_unified(self, query: str, limit: int = 20, page: int = 1) -> Dict:
        """Search across all entities"""
        params = {'query': query, 'limit': limit, 'page': page}
        return self._request('GET', '/api/search/unified', params=params)

    def search_cases(self, query: str, limit: int = 20) -> Dict:
        """Search legal cases"""
        params = {'query': query, 'limit': limit}
        return self._request('GET', '/api/case-search/search', params=params)

    def search_people(self, query: str, limit: int = 20) -> Dict:
        """Search people"""
        params = {'query': query, 'limit': limit}
        return self._request('GET', '/api/people/search', params=params)

    def get_case(self, case_id: int) -> Dict:
        """Get case details"""
        return self._request('GET', f'/api/cases/{case_id}')

    def get_person(self, person_id: int) -> Dict:
        """Get person details"""
        return self._request('GET', f'/api/people/{person_id}')

    def get_bank(self, bank_id: int) -> Dict:
        """Get bank details"""
        return self._request('GET', f'/api/banks/{bank_id}')

    def create_bank(self, bank_data: Dict) -> Dict:
        """Create new bank"""
        return self._request('POST', '/api/banks', json=bank_data)

    def update_bank(self, bank_id: int, bank_data: Dict) -> Dict:
        """Update bank"""
        return self._request('PUT', f'/api/banks/{bank_id}', json=bank_data)

    def delete_bank(self, bank_id: int) -> Dict:
        """Delete bank"""
        return self._request('DELETE', f'/api/banks/{bank_id}')

    def send_ai_message(self, message: str, case_id: int, session_id: Optional[str] = None) -> Dict:
        """Send message to AI chat"""
        data = {
            'message': message,
            'case_id': case_id,
            'session_id': session_id
        }
        return self._request('POST', '/api/ai-chat/message', json=data)

    def generate_case_summary(self, case_id: int, user_id: int = 1) -> Dict:
        """Generate AI case summary"""
        data = {'case_id': case_id, 'user_id': user_id}
        return self._request('POST', '/api/ai-chat/case-summary', json=data)

# Usage
api = JuridenceAPI('your-api-key-here')

# Search for cases
cases = api.search_cases('mahama', 10)
print(cases)

# Get case details
case_details = api.get_case(6490)
print(case_details)

# AI analysis
ai_response = api.send_ai_message('Analyze this case', 6490)
print(ai_response)
```

### PHP

```php
<?php
class JuridenceAPI {
    private $apiKey;
    private $baseUrl;
    private $httpClient;

    public function __construct($apiKey, $baseUrl = 'https://api.juridence.com') {
        $this->apiKey = $apiKey;
        $this->baseUrl = $baseUrl;
        $this->httpClient = curl_init();
    }

    private function request($method, $endpoint, $data = null) {
        $url = $this->baseUrl . $endpoint;
        
        curl_setopt_array($this->httpClient, [
            CURLOPT_URL => $url,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_HTTPHEADER => [
                'Authorization: Bearer ' . $this->apiKey,
                'Content-Type: application/json'
            ]
        ]);

        if ($data) {
            curl_setopt($this->httpClient, CURLOPT_POSTFIELDS, json_encode($data));
        }

        $response = curl_exec($this->httpClient);
        $httpCode = curl_getinfo($this->httpClient, CURLINFO_HTTP_CODE);

        if ($httpCode >= 400) {
            throw new Exception('API Error: ' . $httpCode . ' ' . $response);
        }

        return json_decode($response, true);
    }

    public function searchUnified($query, $limit = 20, $page = 1) {
        $params = http_build_query(['query' => $query, 'limit' => $limit, 'page' => $page]);
        return $this->request('GET', '/api/search/unified?' . $params);
    }

    public function searchCases($query, $limit = 20) {
        $params = http_build_query(['query' => $query, 'limit' => $limit]);
        return $this->request('GET', '/api/case-search/search?' . $params);
    }

    public function searchPeople($query, $limit = 20) {
        $params = http_build_query(['query' => $query, 'limit' => $limit]);
        return $this->request('GET', '/api/people/search?' . $params);
    }

    public function getCase($caseId) {
        return $this->request('GET', '/api/cases/' . $caseId);
    }

    public function getPerson($personId) {
        return $this->request('GET', '/api/people/' . $personId);
    }

    public function getBank($bankId) {
        return $this->request('GET', '/api/banks/' . $bankId);
    }

    public function createBank($bankData) {
        return $this->request('POST', '/api/banks', $bankData);
    }

    public function updateBank($bankId, $bankData) {
        return $this->request('PUT', '/api/banks/' . $bankId, $bankData);
    }

    public function deleteBank($bankId) {
        return $this->request('DELETE', '/api/banks/' . $bankId);
    }

    public function sendAIMessage($message, $caseId, $sessionId = null) {
        $data = [
            'message' => $message,
            'case_id' => $caseId,
            'session_id' => $sessionId
        ];
        return $this->request('POST', '/api/ai-chat/message', $data);
    }

    public function generateCaseSummary($caseId, $userId = 1) {
        $data = ['case_id' => $caseId, 'user_id' => $userId];
        return $this->request('POST', '/api/ai-chat/case-summary', $data);
    }

    public function __destruct() {
        curl_close($this->httpClient);
    }
}

// Usage
$api = new JuridenceAPI('your-api-key-here');

// Search for cases
$cases = $api->searchCases('mahama', 10);
print_r($cases);

// Get case details
$caseDetails = $api->getCase(6490);
print_r($caseDetails);

// AI analysis
$aiResponse = $api->sendAIMessage('Analyze this case', 6490);
print_r($aiResponse);
?>
```

## Error Handling

### HTTP Status Codes

| Code | Description | Action |
|------|-------------|--------|
| 200 | Success | Continue processing |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Check request parameters |
| 401 | Unauthorized | Check API key |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Contact support |

### Error Response Format

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-09-28T15:30:00Z",
  "request_id": "req_123456789"
}
```

### Common Errors

#### Invalid API Key
```json
{
  "detail": "Invalid API key provided",
  "error_code": "INVALID_API_KEY"
}
```

#### Rate Limit Exceeded
```json
{
  "detail": "Rate limit exceeded. Try again in 3600 seconds",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 3600
}
```

#### Validation Error
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "name"],
      "msg": "Field required"
    }
  ],
  "error_code": "VALIDATION_ERROR"
}
```

### Error Handling Examples

#### JavaScript
```javascript
try {
  const response = await api.searchCases('mahama');
  console.log(response);
} catch (error) {
  if (error.message.includes('401')) {
    console.error('Invalid API key');
  } else if (error.message.includes('429')) {
    console.error('Rate limit exceeded');
  } else {
    console.error('API Error:', error.message);
  }
}
```

#### Python
```python
try:
    cases = api.search_cases('mahama')
    print(cases)
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print('Invalid API key')
    elif e.response.status_code == 429:
        print('Rate limit exceeded')
    else:
        print(f'API Error: {e}')
```

## Rate Limits

### Limits by Plan

| Plan | Requests/Hour | Requests/Day | Burst Limit |
|------|---------------|--------------|-------------|
| Free | 100 | 1,000 | 10 |
| Professional | 1,000 | 10,000 | 100 |
| Enterprise | 10,000 | 100,000 | 1,000 |

### Rate Limit Headers

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

### Handling Rate Limits

```javascript
async function makeRequestWithRetry(apiCall, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await apiCall();
    } catch (error) {
      if (error.status === 429 && i < maxRetries - 1) {
        const retryAfter = error.headers['retry-after'] || 60;
        await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
        continue;
      }
      throw error;
    }
  }
}
```

## Best Practices

### 1. API Key Security
- Store API keys securely (environment variables, secret management)
- Never expose keys in client-side code
- Rotate keys regularly
- Use different keys for different environments

### 2. Request Optimization
- Use pagination for large datasets
- Implement caching where appropriate
- Batch requests when possible
- Use appropriate limits

### 3. Error Handling
- Implement comprehensive error handling
- Log errors for debugging
- Implement retry logic for transient errors
- Provide user-friendly error messages

### 4. Performance
- Use connection pooling
- Implement request timeouts
- Monitor API usage
- Optimize query parameters

### 5. Data Handling
- Validate data before sending
- Handle null/empty responses
- Implement data transformation
- Use appropriate data types

## Testing

### Unit Tests

```javascript
// Jest example
describe('JuridenceAPI', () => {
  let api;

  beforeEach(() => {
    api = new JuridenceAPI('test-api-key');
  });

  test('should search cases', async () => {
    const mockResponse = { results: [] };
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResponse)
    });

    const result = await api.searchCases('mahama');
    expect(result).toEqual(mockResponse);
  });
});
```

### Integration Tests

```python
# pytest example
import pytest
from juridence_api import JuridenceAPI

@pytest.fixture
def api():
    return JuridenceAPI('test-api-key')

def test_search_cases(api):
    result = api.search_cases('mahama')
    assert 'results' in result
    assert isinstance(result['results'], list)
```

### Load Testing

```bash
# Using Apache Bench
ab -n 1000 -c 10 -H "Authorization: Bearer YOUR_API_KEY" \
  "https://api.juridence.com/api/search/unified?query=test"
```

## Deployment

### Environment Variables

```bash
# Required
JURIDENCE_API_KEY=your-api-key-here
JURIDENCE_BASE_URL=https://api.juridence.com

# Optional
JURIDENCE_TIMEOUT=30000
JURIDENCE_RETRY_ATTEMPTS=3
JURIDENCE_CACHE_TTL=3600
```

### Docker Example

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .

ENV JURIDENCE_API_KEY=your-api-key-here
ENV JURIDENCE_BASE_URL=https://api.juridence.com

EXPOSE 3000
CMD ["npm", "start"]
```

### Kubernetes Config

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: juridence-config
data:
  API_KEY: "your-api-key-here"
  BASE_URL: "https://api.juridence.com"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: juridence-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: juridence-app
  template:
    metadata:
      labels:
        app: juridence-app
    spec:
      containers:
      - name: app
        image: your-app:latest
        envFrom:
        - configMapRef:
            name: juridence-config
```

## Support

### Getting Help
- **Documentation**: Check this guide and API docs
- **Admin Dashboard**: Use the built-in documentation
- **Support Email**: support@juridence.com
- **GitHub Issues**: For bug reports and feature requests

### Reporting Issues
When reporting issues, please include:
- API endpoint and method
- Request parameters
- Response status and body
- Steps to reproduce
- Expected vs actual behavior

### Feature Requests
- Use the admin dashboard feedback form
- Email: features@juridence.com
- Include use case and business justification

---

**Last Updated**: September 28, 2025  
**Version**: 1.0.0  
**API Version**: v1
