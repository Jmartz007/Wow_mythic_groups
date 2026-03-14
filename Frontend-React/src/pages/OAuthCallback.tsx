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

      try {        // Exchange the code for tokens
        const response = await fetch('/groups/auth/oauth/blizzard/callback?code=' + code);
         if (!response.ok) {
          if (response.status === 400) {
            console.log('Bad request, possibly invalid code or state');
            const msg = await response.json()
            console.log('Error message: ', msg);
            return;
                }
          throw new Error(`HTTP error! status: ${response.status}`);
              }

        const data = await response.json();
        console.log('Received data:', data);
        if (data.token) {
          // Store the JWT token
          localStorage.setItem('token', data.token);
          // Store the Blizzard access token for fetching character data
          if (data.blizzard_access_token) {
            localStorage.setItem('blizzard_access_token', data.blizzard_access_token);
          }
          // Store user info including characters
          if (data.user) {
            localStorage.setItem('user', JSON.stringify({
              id: data.user.id,
              battletag: data.user.battletag,
            }));
            // Store characters if available
            if (data.characters) {
              localStorage.setItem('characters', JSON.stringify(data.characters));
              console.log('Stored characters:', data.characters.length);
            }
          }
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
