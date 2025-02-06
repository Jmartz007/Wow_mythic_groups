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

function App() {
  return (
    <>
      <div className="bg-dark">
        <Navbar />
        <div className="container p-4">
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
        </div>
      </div>
    </>
  );
}

export default App;
