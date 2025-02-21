import { Typography } from "@mui/material";
import { Link } from "react-router-dom";

export default function NotAuthorized() {
  return (
    <div className="rounded border border-1 shadow bg-primary-subtle p-4">
      <h1>Not Authorized</h1>
      <h3>Please Log In</h3>
      <p>You will be redirected to the home page shortly...</p>
      <Typography variant="h1">
        <Link to="/">Home</Link>{" "}
      </Typography>
    </div>
  );
}
