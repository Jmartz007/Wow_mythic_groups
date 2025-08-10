import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Logout() {
  const navigate = useNavigate();
  const { logout } = useAuth();

  useEffect(() => {
    const handleLogout = async () => {
      try {
        await logout();
        navigate("/");
      } catch (error) {
        console.error("Logout error:", error);
        alert("There was an error logging out");
        navigate("/");
      }
    };

    handleLogout();
  }, [navigate, logout]);

  return <div>Logging Out...</div>;
}
