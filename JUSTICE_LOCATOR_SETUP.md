# Justice Locator Setup Guide

## Google Maps API Configuration

To enable the map functionality in the Justice Locator, you need to configure a Google Maps API key.

### Step 1: Get a Google Maps API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Maps JavaScript API**
   - **Places API** (for search functionality)
   - **Geocoding API** (for address conversion)

### Step 2: Configure the API Key

1. Create a `.env` file in the project root directory
2. Add the following line:
   ```
   REACT_APP_GOOGLE_MAPS_API_KEY=your_actual_api_key_here
   ```
3. Replace `your_actual_api_key_here` with your actual Google Maps API key

### Step 3: Restart the Development Server

After adding the API key, restart your development server:
```bash
npm start
```

### Step 4: Verify Setup

1. Navigate to the Justice Locator page
2. You should see the map view working properly
3. If the API key is not configured, you'll see a helpful message with setup instructions

## Features Available

### With Google Maps API Key:
- Interactive map view with court markers
- Click on markers to view court details
- Get directions to courts
- Proximity search functionality
- Map bounds automatically adjust to show all courts

### Without Google Maps API Key:
- List view of all courts
- Search and filter functionality
- Court details sidebar
- All court information is still accessible

## Troubleshooting

### Common Issues:

1. **"InvalidKeyMapError"**: The API key is not valid or not properly configured
2. **"Map view unavailable"**: The API key is missing or the required APIs are not enabled
3. **Map not loading**: Check browser console for specific error messages

### Security Notes:

- Never commit your `.env` file to version control
- Restrict your API key to specific domains in production
- Monitor your API usage in the Google Cloud Console

## Court Data

The Justice Locator comes with sample court data including:
- Supreme Court of Ghana
- High Court locations
- Circuit Courts
- District Courts
- Commercial Courts

Admins can add, edit, and manage court data through the admin dashboard.
