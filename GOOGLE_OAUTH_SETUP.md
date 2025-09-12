# Google OAuth Setup Guide

This app now supports Google authentication for both login and registration. Follow these steps to set up Google OAuth:

## 1. Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API (or Google Identity API)
4. Go to "Credentials" in the left sidebar
5. Click "Create Credentials" → "OAuth 2.0 Client IDs"
6. Choose "Web application" as the application type
7. Add your domain to "Authorized JavaScript origins":
   - For development: `http://localhost:3000`
   - For production: `https://yourdomain.com`
8. Copy the generated Client ID

## 2. Configure Environment Variables

Create a `.env` file in the root directory and add:

```env
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

Replace `your-google-client-id.apps.googleusercontent.com` with your actual Google Client ID.

## 3. Features

### Login Page (`/login`)
- Traditional email/password login
- Google Sign-In button
- Demo credentials: `demo@dennislaw.com` / `demo123`

### Registration Page (`/signup`)
- Traditional registration form
- Google Sign-In button
- Cross-linking to login page

### Header Component
- Shows Login/Register buttons when not authenticated
- Shows user email and Logout button when authenticated
- Handles both traditional and Google authentication

## 4. User Experience

- **Seamless Integration**: Google Sign-In works alongside traditional authentication
- **Persistent Sessions**: Login state persists across browser sessions
- **Mobile Responsive**: Works on all device sizes
- **Error Handling**: Graceful error handling for failed authentications

## 5. Security Notes

- Google OAuth tokens are handled securely by Google's services
- User data is stored locally in localStorage (consider using secure storage for production)
- All authentication flows include proper error handling

## 6. Testing

1. Start the development server: `npm start`
2. Navigate to `/login` or `/signup`
3. Try both traditional login and Google Sign-In
4. Test logout functionality
5. Verify session persistence across page refreshes

## Troubleshooting

- **Google Sign-In not loading**: Check if the Google Client ID is correctly set
- **Authentication errors**: Verify the domain is added to authorized origins
- **Console errors**: Check browser console for detailed error messages
