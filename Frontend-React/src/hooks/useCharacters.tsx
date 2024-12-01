import { useEffect, useState } from "react";

export default function useCharacters() {
    const [characterData, setCharacterData] = useState<Array<Record<string,any>>>([]);

    const fetchCharacters = async () => {
        const response = await fetch("http://localhost:5000/groups/api/current-players");

        if (!response.ok) {
            console.error("error occurred fetching characters")
            throw Error("error fetching data")
        };
        const data = await response.json();
        setCharacterData(data);
    };

    useEffect(() => {
        fetchCharacters();
    }, []);

    return characterData 
};