import { Box, Container, Typography } from "@mui/material";
import { Link } from "react-router-dom";

export default function NotAuthorized() {
  return (
    <Container>
      <Box paddingBlock={6}>
        <Typography variant="h1" color="red">
          Not Authorized
        </Typography>
        <Typography variant="h5">Please Log In</Typography>
        <Typography variant="subtitle1">
          You will be redirected to the home page shortly...
        </Typography>
        <Typography variant="h5">
          <Link to="/">Home</Link>{" "}
        </Typography>
      </Box>
    </Container>
  );
}
