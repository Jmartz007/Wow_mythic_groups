import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function OAuthCallback() {
  const navigate = useNavigate();
  const { checkAuthStatus } = useAuth();

  useEffect(() => {
    const handleCallback = async () => {
      // Get the authorization code and state from the URL
      const params = new URLSearchParams(window.location.search);
      const code = params.get('code');
      const state = params.get('state');
      
      // Verify state matches what we stored
      const storedState = sessionStorage.getItem('oauth_state');
      if (!state || state !== storedState) {
        console.error('State mismatch. Possible CSRF attack.');
        navigate('/');
        return;
      }

      if (!code) {
        console.error('No authorization code received');
        navigate('/');
        return;
      }

      try {
        // Exchange the code for tokens
        const response = await fetch('/api/oauth/blizzard/callback?code=' + code);
        if (!response.ok) {
          throw new Error('Failed to exchange code for token');
        }

        const data = await response.json();
        if (data.token) {
          // Store the JWT token
          localStorage.setItem('token', data.token);
          await checkAuthStatus();
          navigate('/list');
        } else {
          throw new Error('No token received');
        }
      } catch (error) {
        console.error('Auth error:', error);
        navigate('/');
      }
    };

    handleCallback();
  }, [navigate, checkAuthStatus]);

  return (
    <div>
      Processing login...
    </div>
  );
}
