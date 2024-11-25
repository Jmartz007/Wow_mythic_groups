import { Route, Routes } from "react-router-dom";
import Navbar from "./components/NavHeader";
import Home from "./pages/Home";
import EditDungeons from "./pages/EditDungeons";
import NotFoundPage from "./pages/NotFoundPage";
import PlayerEntry from "./pages/PlayerEntry";

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
            <Route path="/Dungeons" element={<EditDungeons />} />
            <Route path="/new-entry" element={<PlayerEntry />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </div>
      </div>
    </>
  );
}

export default App;
