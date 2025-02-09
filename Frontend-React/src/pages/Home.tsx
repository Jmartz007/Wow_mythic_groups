import { Box } from "@mui/material";
import LoginCard from "../components/LoginCard";

export default function Home() {
  return (
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
  );
}
