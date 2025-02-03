import { useEffect, useState } from "react";

interface Player {
  Character: string;
  Class: string;
  Dungeon: string;
  "Is Active": number;
  "Key Level": number;
  Player: string;
  Range: string;
  "Role Skill": number[];
  "Role Type": string[];
  "Skill Level": number;
}

export default function useCharacters() {
  const [characterData, setCharacterData] = useState<Player[]>([]);

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
