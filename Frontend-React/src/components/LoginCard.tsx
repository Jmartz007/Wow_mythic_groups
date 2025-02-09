import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  FormControl,
  InputLabel,
  OutlinedInput,
  Typography,
  useTheme,
} from "@mui/material";
import { FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginCard() {
  const navigate = useNavigate();
  const { isAuthenticated, checkAuthStatus } = useAuth();
  const theme = useTheme();

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
      sx={{
        width: "100vw",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "400px",
        borderColor: "blue",
        borderWidth: 2,
        borderStyle: "solid",
      }}
    >
      <Card
        component="form"
        onSubmit={handleSubmit}
        variant="outlined"
        sx={{
          minWidth: "200px",
          maxWidth: "400px",
          width: "75%",
          flexGrow: 1,
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          borderColor: "green",
          borderWidth: 4,
          borderStyle: "dotted",
        }}
      >
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
          <>
            <CardContent
              sx={{
                display: "flex",
                flexDirection: "column",
                gap: 3,
                borderColor: "orange",
                borderWidth: 4,
                borderStyle: "double",
                alignItems: "stretch",
                alignContent: "stretch",
              }}
            >
              <Typography
                variant="h3"
                sx={{
                  m: 1,
                  borderColor: "purple",
                  borderStyle: "solid",
                  textAlign: "center",
                }}
              >
                Log In
              </Typography>

              <FormControl fullWidth>
                <InputLabel htmlFor="username" className="form-label">
                  User Name
                </InputLabel>
                <OutlinedInput
                  label="User Name"
                  type="text"
                  id="username"
                  name="username"
                />
              </FormControl>

              <FormControl fullWidth>
                <InputLabel htmlFor="outlined-password-input">
                  Password
                </InputLabel>
                <OutlinedInput
                  id="outlined-password-input"
                  label="Password"
                  type="password"
                  name="password"
                />
              </FormControl>
            </CardContent>

            <CardActions
              sx={{
                justifyContent: "center",
                paddingBottom: 2,
                borderColor: "orange",
                borderWidth: 4,
                borderStyle: "double",
              }}
            >
              <Button type="submit" variant="contained" color="primary">
                Log In
              </Button>
            </CardActions>
          </>
        )}
      </Card>
    </Box>
  );
}
