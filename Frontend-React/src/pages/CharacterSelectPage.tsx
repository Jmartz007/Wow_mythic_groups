import React from "react";
import { Container, Box, Typography } from "@mui/material";
import CharacterSelect from "../components/CharacterSelect";

const CharacterSelectPage: React.FC = () => {
  const accessToken = localStorage.getItem("token") || "";

  const handleImport = (selectedCharacters: any[]) => {
    // Implement your import logic here (e.g., send to backend, update state, etc.)
    console.log("Selected characters to import:", selectedCharacters);
    // You could redirect or show a success message here
  };

  return (
    <Container>
      <Box paddingBottom={12}>
        <Box paddingBlock={4} marginInline={4}>
          <Typography variant="h3">Import Your WoW Characters</Typography>
        </Box>
        <CharacterSelect accessToken={accessToken} onImport={handleImport} />
      </Box>
    </Container>
  );
};

export default CharacterSelectPage;