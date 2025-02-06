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
            <Route path="/list" element={<PlayersList />} />
            <Route path="/dungeons" element={<EditDungeons />} />
            <Route path="/new-entry" element={<PlayerEntry />} />
            <Route path="/players/:playername" element={<PlayerDetails />} />
            <Route
              path="/players/:playername/characters/:charactername"
              element={<CharacterDetails />}
            />
            <Route path="/create-groups" element={<GroupListPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </div>
      </div>
    </>
  );
}

export default App;
