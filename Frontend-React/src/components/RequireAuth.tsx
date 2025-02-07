import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import NotAuthorized from "../pages/NotAuthorized";
import { useAuth } from "../context/AuthContext";

const RequireAuth = ({ children }: { children: JSX.Element }) => {
  const { isAuthenticated, checkAuthStatus } = useAuth();
  const [showNotAuthorized, setShowNotAuthorized] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated === false) {
      console.log("Not authorized, showing NotAuthorized page");
      setShowNotAuthorized(true);
      setTimeout(() => {
        setShowNotAuthorized(false);
        navigate("/");
      }, 3000); // Show the "Not Authorized" page for 3 seconds
    }
  }, [isAuthenticated, navigate]);

  useEffect(() => {
    checkAuthStatus();
  }, [checkAuthStatus]);

  if (showNotAuthorized) {
    return <NotAuthorized />;
  }

  return isAuthenticated ? children : null;
};

export default RequireAuth;
