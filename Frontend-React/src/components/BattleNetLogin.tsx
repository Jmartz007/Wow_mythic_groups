import { Box, Button } from "@mui/material";
import { useEffect } from "react";

export default function BattleNetLogin() {
  // Function to generate a random state string
  const generateState = () => {
    const array = new Uint32Array(8);
    window.crypto.getRandomValues(array);
    return Array.from(array, (dec) => dec.toString(16).padStart(2, "0")).join("");
  };

  const handleLogin = () => {
    const state = generateState();
    // Store state in sessionStorage to verify when we get it back
    sessionStorage.setItem("oauth_state", state);

    // Construct the authorization URL with required parameters
    const params = new URLSearchParams({
      client_id: process.env.REACT_APP_BLIZZARD_CLIENT_ID || "",
      scope: "openid",
      response_type: "code",
      state: state,
      redirect_uri: process.env.REACT_APP_BLIZZARD_REDIRECT_URI || "",
    });

    // Redirect to Blizzard's authorization page
    window.location.href = `https://oauth.battle.net/authorize?${params.toString()}`;
  };

  return (
    <Box display="flex" justifyContent="center" mt={4}>
      <Button 
        variant="contained" 
        color="primary" 
        onClick={handleLogin}
        size="large"
      >
        Log in with Battle.net
      </Button>
    </Box>
  );
}
