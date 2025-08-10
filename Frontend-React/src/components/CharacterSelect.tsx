import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Checkbox,
  FormControlLabel,
  Button,
  CircularProgress,
  Alert,
} from "@mui/material";

interface Character {
  id: number;
  name: string;
  realm: { name: string };
  level: number;
  playable_class: { name: string };
  playable_race: { name: string };
  faction: { name: string };
  // Add more fields as needed
}

interface Props {
  accessToken: string;
  onImport: (selected: Character[]) => void;
}

const CharacterSelect: React.FC<Props> = ({ accessToken, onImport }) => {
  const [characters, setCharacters] = useState<Character[]>([]);
  const [selected, setSelected] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/groups/api/profile/import-characters", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then(async (res) => {
        if (!res.ok) {
          throw new Error(await res.text());
        }
        return res.json();
      })
      .then((data) => {
        // Flatten all characters from all wow_accounts
        const allChars: Character[] =
          data.wow_accounts?.flatMap((acct: any) => acct.characters) || [];
        setCharacters(allChars);
        setLoading(false);
      })
      .catch((err) => {
        setError("Failed to load characters: " + err.message);
        setLoading(false);
      });
  }, [accessToken]);

  const handleToggle = (id: number) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const handleImport = () => {
    const selectedChars = characters.filter((c) => selected.has(c.id));
    onImport(selectedChars);
  };

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Select Characters to Import
      </Typography>
      {characters.length === 0 ? (
        <Typography>No characters found.</Typography>
      ) : (
        <Box>
          {characters.map((char) => (
            <FormControlLabel
              key={char.id}
              control={
                <Checkbox
                  checked={selected.has(char.id)}
                  onChange={() => handleToggle(char.id)}
                />
              }
              label={`${char.name} (${char.level} ${char.playable_race?.name} ${char.playable_class?.name}, ${char.realm?.name}, ${char.faction?.name})`}
            />
          ))}
          <Box mt={2}>
            <Button
              variant="contained"
              color="primary"
              disabled={selected.size === 0}
              onClick={handleImport}
            >
              Import Selected Characters
            </Button>
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default CharacterSelect;
