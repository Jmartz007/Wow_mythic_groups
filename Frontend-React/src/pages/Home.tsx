import { Box, Container } from "@mui/material";
import LoginCard from "../components/LoginCard";

export default function Home() {
  return (
    <Container>
    <Box
      sx={{
        display: "flex",
        width: "100%",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <LoginCard />
    </Box>
    </Container>
  );
}
