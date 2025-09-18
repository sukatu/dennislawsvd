module.exports = {
  apps: [
    {
      name: 'case-search-backend',
      cwd: '/var/www/case-search/backend',
      script: 'venv/bin/uvicorn',
      args: 'main:app --host 0.0.0.0 --port 8000',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        DATABASE_URL: 'mysql+pymysql://root:your_password@localhost:3306/case_search_db',
        SECRET_KEY: 'your-secret-key-change-this-in-production',
        ALGORITHM: 'HS256',
        ACCESS_TOKEN_EXPIRE_MINUTES: '30',
        CORS_ORIGINS: 'https://your-domain.com,http://localhost:3000',
        REACT_APP_GOOGLE_MAPS_API_KEY: 'your_google_maps_api_key',
        DEBUG: 'False'
      },
      error_file: '/var/log/pm2/case-search-backend-error.log',
      out_file: '/var/log/pm2/case-search-backend-out.log',
      log_file: '/var/log/pm2/case-search-backend.log'
    },
    {
      name: 'case-search-frontend',
      cwd: '/var/www/case-search',
      script: 'npx',
      args: 'serve -s build -l 3000',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'production',
        REACT_APP_API_URL: 'https://your-domain.com',
        REACT_APP_GOOGLE_MAPS_API_KEY: 'your_google_maps_api_key'
      },
      error_file: '/var/log/pm2/case-search-frontend-error.log',
      out_file: '/var/log/pm2/case-search-frontend-out.log',
      log_file: '/var/log/pm2/case-search-frontend.log'
    }
  ]
};
