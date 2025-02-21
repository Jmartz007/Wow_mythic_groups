import { Box, Container, Paper, Typography, useTheme } from "@mui/material";
import { Link } from "react-router-dom";

export default function NotFoundPage() {
  const theme = useTheme();
  return (
    <Container>
      {/* <Paper elevation={12}> */}
      <Box paddingBottom={12} minHeight={400} color={theme.palette.error.main}>
        <Typography variant="h1">404 | Page Not Found</Typography>
        <Link to="/">Home</Link>
      </Box>
      {/* </Paper> */}
    </Container>
  );
}
