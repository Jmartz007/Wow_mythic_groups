import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

const RequireAuth = ({ children }: { children: JSX.Element }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const response = await fetch("/groups/auth/status", {
          method: "GET",
          credentials: "include",
        });
        const data = await response.json();
        setIsAuthenticated(data.authenticated);
      } catch (error) {
        console.error("Error checking authentication status:", error);
        setIsAuthenticated(false);
      }
    };

    checkAuthStatus();
  }, []);

  if (isAuthenticated === null) {
    // Optionally, you can return a loading indicator while checking the auth status
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/" />;
  }

  return children;
};

export default RequireAuth;
