import { useEffect, useState } from "react";

export default function useCharacters() {
  const [characterData, setCharacterData] = useState<
    Array<Record<string, any>>
  >([]);

  const fetchCharacters = async () => {
    try {
      const response = await fetch("/groups/api/players-flat");

      if (!response.ok) {
        console.error("error occurred fetching characters");
        // throw Error("error fetching data")
      }
      const data = await response.json();
      console.log("fetch data:", data);
      setCharacterData(data);
    } catch (error) {
      console.error("error fetching player data");
    }
  };

  useEffect(() => {
    fetchCharacters();
  }, []);
  return characterData;
}
