import { useEffect, useState } from "react";
import { Player } from "../types/Player";

export default function useCharacters() {
  const [characterData, setCharacterData] = useState<Player[]>([]);
  const [loading, setLoading] = useState(true);
  // const { isAuthenticated } = useAuth();

  const fetchCharacters = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch("/groups/api/players-flat", {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Token is invalid or expired
          localStorage.removeItem('token');
          console.error("Authentication failed");
        } else {
          console.error("error occurred fetching characters");
        }
        throw new Error("Failed to fetch data");
      }
      const data = await response.json();
      // console.log("useCharacter data:", data);
      setCharacterData(data);
      setLoading(false);
    } catch (error) {
      console.error("error fetching player data");
    }
  };

  useEffect(() => {
    console.log("fetching characters");
    fetchCharacters();
  }, []);

  return { characterData, loading };
}
