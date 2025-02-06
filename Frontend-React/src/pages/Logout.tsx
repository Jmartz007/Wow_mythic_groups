import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    const logout = async () => {
      try {
        const response = await fetch("/groups/auth/logout", {
          method: "GET",
        });

        if (!response.ok) {
          throw new Error("Failed to log out");
        }

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
