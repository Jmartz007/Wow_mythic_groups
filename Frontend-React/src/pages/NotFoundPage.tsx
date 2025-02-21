import { Box, Container, Typography, useTheme } from "@mui/material";
import { Link } from "react-router-dom";

export default function NotFoundPage() {
  const theme = useTheme();
  return (
    <Container>
      <Box paddingBlock={6} color={theme.palette.error.main}>
        <Typography variant="h1">404 | Page Not Found</Typography>
        <Link to="/">Home</Link>
      </Box>
    </Container>
  );
}
