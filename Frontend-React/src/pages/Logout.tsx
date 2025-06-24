import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Logout() {
  const navigate = useNavigate();
  const { checkAuthStatus } = useAuth();

  useEffect(() => {
    const logout = async () => {
      try {
        const response = await fetch("/groups/auth/logout", {
          method: "GET",
        });

        if (!response.ok) {
          throw new Error("Failed to log out");
        }

        await checkAuthStatus();

        navigate("/");
      } catch (error) {
        console.error("Logout error: ", error);
        alert("There was an error logging out");
      }
    };

    logout();
  }, [navigate]);

  return <div>Logging Out...</div>;
}
