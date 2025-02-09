import { Route, Routes } from "react-router-dom";
import Navbar from "./components/NavHeader";
import Home from "./pages/Home";
import EditDungeons from "./pages/EditDungeons";
import NotFoundPage from "./pages/NotFoundPage";
import PlayerEntry from "./pages/PlayerEntry";
import PlayerDetails from "./pages/PlayerDetails";
import CharacterDetails from "./pages/CharacterDetails";
import PlayersList from "./pages/PlayersList";
import GroupListPage from "./pages/GroupListPage";
import Logout from "./pages/Logout";
import RequireAuth from "./components/RequireAuth";
import { AuthProvider } from "./context/AuthContext";
import {
  Box,
  Container,
  CssBaseline,
  ThemeProvider,
  useMediaQuery,
} from "@mui/material";
import { darkTheme, lightTheme } from "./theme";
import { useMemo, useState } from "react";

function App() {
  const prefersDarkMode = useMediaQuery("(prefers-color-scheme: dark)");
  const [isDarkMode, setIsDarkMode] = useState(prefersDarkMode);

  const theme = useMemo(
    () => (isDarkMode ? darkTheme : lightTheme),
    [isDarkMode]
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Navbar />
        <Box
          sx={{
            height: "100vh",
          }}
        >
          <Routes>
            <Route
              path="/"
              element={<Home />}
              errorElement={<NotFoundPage />}
            ></Route>
            <Route
              path="/list"
              element={
                <RequireAuth>
                  <PlayersList />
                </RequireAuth>
              }
            />
            <Route
              path="/dungeons"
              element={
                <RequireAuth>
                  <EditDungeons />
                </RequireAuth>
              }
            />
            <Route
              path="/new-entry"
              element={
                <RequireAuth>
                  <PlayerEntry />
                </RequireAuth>
              }
            />
            <Route
              path="/players/:playername"
              element={
                <RequireAuth>
                  <PlayerDetails />
                </RequireAuth>
              }
            />
            <Route
              path="/players/:playername/characters/:charactername"
              element={
                <RequireAuth>
                  <CharacterDetails />
                </RequireAuth>
              }
            />
            <Route
              path="/create-groups"
              element={
                <RequireAuth>
                  <GroupListPage />
                </RequireAuth>
              }
            />
            <Route path="/logout" element={<Logout />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </Box>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
