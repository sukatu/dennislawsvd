# Dennislaw SVD - React Application

A comprehensive legal database platform built with React for searching people and legal cases in Ghana's court system.

## Features

- **People Search**: Search by name, ID number, phone, or address
- **Advanced Search**: Multi-criteria filtering with comprehensive options
- **Risk Assessment**: Automated risk scoring and categorization
- **Case Management**: Detailed case information and history
- **Responsive Design**: Mobile-optimized interface
- **Export Functionality**: CSV export for search results
- **Interactive UI**: Grid/list view toggle, real-time filtering

## Technology Stack

- **Frontend**: React 18, React Router DOM
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Build Tool**: Create React App

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd case_search_html
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

### Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm eject` - Ejects from Create React App (one-way operation)

## Project Structure

```
src/
├── components/          # Reusable components
│   ├── Header.js       # Navigation header
│   └── Footer.js       # Footer component
├── pages/              # Page components
│   ├── Home.js         # Landing page
│   ├── About.js        # About page
│   ├── Contact.js      # Contact form
│   ├── AdvancedSearch.js # Advanced search form
│   ├── PeopleDatabase.js # People database table
│   ├── PeopleResults.js  # Search results
│   ├── PersonProfile.js  # Individual profile
│   ├── CaseDetail.js     # Case details
│   ├── Results.js        # Case search results
│   ├── Signup.js         # User registration
│   └── Specification.js  # Technical documentation
├── App.js              # Main app component with routing
├── index.js            # App entry point
└── index.css           # Global styles
```

## Key Features Implemented

### 1. **Routing & Navigation**
- React Router DOM for client-side routing
- Responsive navigation with mobile menu
- Breadcrumb navigation

### 2. **State Management**
- React hooks (useState, useEffect) for local state
- URL parameters for search queries
- Form state management

### 3. **Interactive Components**
- Search forms with validation
- Filter systems with checkboxes and dropdowns
- View toggle (grid/list) for results
- Export functionality

### 4. **Responsive Design**
- Mobile-first approach with Tailwind CSS
- Responsive grid layouts
- Touch-friendly interface

### 5. **Data Handling**
- Mock data for demonstration
- Search and filtering logic
- CSV export functionality

## Pages Overview

1. **Home** (`/`) - Landing page with hero section and search
2. **About** (`/about`) - Company information and statistics
3. **Contact** (`/contact`) - Contact form and business info
4. **Advanced Search** (`/advanced-search`) - Comprehensive search form
5. **People Database** (`/people-database`) - Tabular database view
6. **People Results** (`/people-results`) - Search results with filters
7. **Person Profile** (`/person-profile`) - Individual person details
8. **Case Detail** (`/case-detail`) - Individual case information
9. **Results** (`/results`) - Case search results
10. **Signup** (`/signup`) - User registration form
11. **Specification** (`/specification`) - Technical documentation

## Customization

### Styling
- Modify `tailwind.config.js` for theme customization
- Update `src/index.css` for global styles
- Component-specific styles use Tailwind classes

### Data
- Replace mock data in components with API calls
- Update search and filter logic as needed
- Modify export functionality for different formats

### Features
- Add new pages by creating components in `src/pages/`
- Update routing in `src/App.js`
- Add new components in `src/components/`

## Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Static Hosting
The build folder contains static files that can be deployed to:
- Netlify
- Vercel
- GitHub Pages
- AWS S3
- Any static hosting service

### Environment Variables
Create a `.env` file for environment-specific configuration:
```
REACT_APP_API_URL=your_api_url
REACT_APP_ENVIRONMENT=production
```

## Future Enhancements

1. **Backend Integration**
   - Connect to real API endpoints
   - Implement authentication
   - Add data persistence

2. **Advanced Features**
   - Real-time search
   - Advanced filtering
   - Data visualization
   - User accounts and preferences

3. **Performance**
   - Code splitting
   - Lazy loading
   - Caching strategies
   - PWA features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact:
- Email: support@dennislawsvd.com
- Phone: +233 302 123 456

---

**Dennislaw SVD** - Your trusted partner for comprehensive people search and case history discovery.
