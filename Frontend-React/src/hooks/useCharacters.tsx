import { useEffect, useState } from "react";
import { Player } from "../types/Player";
import { useAuth } from "../context/AuthContext";

export default function useCharacters() {
  const [characterData, setCharacterData] = useState<Player[]>([]);
  const { isAuthenticated } = useAuth();

  const fetchCharacters = async () => {
    try {
      const response = await fetch("/groups/api/players-flat");

      if (!response.ok) {
        console.error("error occurred fetching characters");
        // throw Error("error fetching data")
      }
      const data = await response.json();
      console.log("Player data:", data);
      setCharacterData(data);
    } catch (error) {
      console.error("error fetching player data");
    }
  };

  useEffect(() => {
    console.log("isAuthenticated changed: ", isAuthenticated);
    if (isAuthenticated) {
      fetchCharacters();
    }
  }, [isAuthenticated]);

  return characterData;
}
