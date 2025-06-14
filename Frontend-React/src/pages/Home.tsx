import { Box, Container, Typography } from "@mui/material";
import BattleNetLogin from "../components/BattleNetLogin";

export default function Home() {
  return (
    <Container>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          width: "100%",
          alignItems: "center",
          marginTop: 8,
        }}
      >
        <Typography variant="h2" component="h1" gutterBottom>
          Mythic Groups Maker
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          Log in with your Battle.net account to get started
        </Typography>
        <BattleNetLogin />
      </Box>
    </Container>
  );
}
