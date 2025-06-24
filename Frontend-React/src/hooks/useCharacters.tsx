import { useEffect, useState } from "react";
import { Player } from "../types/Player";

export default function useCharacters() {
  const [characterData, setCharacterData] = useState<Player[]>([]);
  const [loading, setLoading] = useState(true);
  // const { isAuthenticated } = useAuth();

  const fetchCharacters = async () => {
    try {
      setLoading(true);

      const response = await fetch("/groups/api/players-flat");

      if (!response.ok) {
        console.error("error occurred fetching characters");
        // throw Error("error fetching data")
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
