import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { FormEvent } from "react";
import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  FormControl,
  FormLabel,
  TextField,
  Typography,
} from "@mui/material";

export default function LoginCard() {
  const navigate = useNavigate();
  const { isAuthenticated, checkAuthStatus } = useAuth();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const formData = new FormData(e.currentTarget);
      const jsonData = Object.fromEntries(formData.entries());

      const response = await fetch("/groups/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(jsonData),
      });
      console.log(JSON.stringify(jsonData));

      if (!response.ok) {
        const errorResponse = await response.json();
        console.log(errorResponse);
        const errorMessage = errorResponse.error.message;
        throw new Error(errorMessage);
      }

      const data = await response.json();
      console.log(data);
      await checkAuthStatus();

      navigate("/list");
    } catch (error) {
      console.error("error submitting form: ", error);
      if (error instanceof Error) {
        alert(`Log in error: ${error.message}`);
      } else {
        alert("there was an error submitting form");
      }
    }
  };
  return (
    <Box
      sx={{ display: "flex", flexDirection: "column", width: "100%", gap: 2, bordercolor: "blue", borderwidth: 5, borderStyle: "solid" }}
    >
      <Card variant="outlined">
        {isAuthenticated ? (
          <CardContent>
            <div>
              <h2>Welcome back!</h2>
              <p>
                We're glad to see you again. You can navigate to the Player List
                page to see your players.
              </p>
            </div>
          </CardContent>
        ) : (
          <Box component="form" onSubmit={handleSubmit} sx={{width: "100%", gap: 2, bordercolor: "orange", borderwidth: 2, borderStyle: "dashed"}}>
            <CardContent sx={{ justifyContent: "center" }}>
              <Typography variant="h3">Log In</Typography>
              <div className="mb-3">
                <FormControl>
                  <FormLabel htmlFor="username" className="form-label">
                    User Name
                  </FormLabel>
                  <TextField
                    type="text"
                    id="username"
                    name="username"
                    placeholder="User Name"
                  />
                </FormControl>
              </div>
              <div className="mb-3">
                <FormControl>
                  <FormLabel htmlFor="password">Password</FormLabel>
                  <TextField
                    type="password"
                    id="password"
                    name="password"
                    placeholder="Password"
                  />
                </FormControl>
              </div>
            </CardContent>

            <CardActions sx={{ justifyContent: "center", paddingBottom: 2 }}>
              <Button type="submit" variant="contained">
                Log In
              </Button>
            </CardActions>
          </Box>
        )}
      </Card>
    </Box>
  );
}
