import { Route, Routes } from "react-router-dom";
import Navbar from "./components/NavHeader";
import Home from "./pages/Home";
import EditDungeons from "./pages/EditDungeons";
import NotFoundPage from "./pages/NotFoundPage";
import PlayerEntry from "./pages/PlayerEntry";

function App() {
  return (
    <>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} errorElement={<NotFoundPage />} />
          <Route path="/Dungeons" element={<EditDungeons />} />
          <Route path="/new-entry" element={<PlayerEntry />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
