import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "bootstrap/dist/css/bootstrap.css";
import App from "./App.tsx";
import { BrowserRouter } from "react-router-dom";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <div className="bg-dark">
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </div>
  </StrictMode>
);