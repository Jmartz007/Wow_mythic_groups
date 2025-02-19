import { Box, Container, Typography } from "@mui/material";
import EntryForm from "../components/EntryForm";

function PlayerEntry() {
  return (
    <Container>
      <Box paddingBottom={12}>
        <Box paddingBlock={4} marginInline={4}>
          <Typography variant="h3">Player Entry Form</Typography>
        </Box>
        <Box gap={4}>
          <EntryForm />
        </Box>
      </Box>
    </Container>
  );
}

export default PlayerEntry;
