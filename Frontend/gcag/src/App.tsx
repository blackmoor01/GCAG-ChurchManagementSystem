// src/App.tsx
import { Routes, Route } from "react-router-dom";
import LoginPage from "./pages/Login";
import RegisterPage from "./pages/Register";
import DashboardPage from "./pages/Dasboard";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      {/* default route */}
      <Route path="*" element={<LoginPage />} />
    </Routes>
  );
}

export default App;
