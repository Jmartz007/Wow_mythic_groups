import { Box } from "@mui/material";
import LoginCard from "../components/LoginCard";

export default function Home() {
  return (
    <Box sx={{borderWidth: 1, borderStyle: "solid", borderColor: "red" }}>
      <LoginCard />
      <h1>Hello</h1>
    </Box>
  );
}
