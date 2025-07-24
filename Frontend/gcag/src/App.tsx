import { Routes, Route, Navigate } from "react-router-dom";

import LoginPage from "./pages/Login";
import RegisterPage from "./pages/Register";

// Wrap protected routes in Layout:
import Layout from "./components/layout/layout";
import DashboardPage from "./pages/Dasboard";

// Members sub‑pages
import MembersPage from "./pages/members/MembersPage";
import AllMembers from "./pages/members/AllMembers";
import AddMember from "./pages/members/AddMember";
import MemberProfile from "./pages/members/MemberProfile";
import MinistryPage from "./pages/ministries/MinistryPage";

function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Protected area (requires Layout wrapper) */}
      <Route element={<Layout />}>
        <Route path="/dashboard" element={<DashboardPage />} />

        {/* Members parent with tabs */}
        <Route path="/members" element={<MembersPage />}>
          <Route index element={<AllMembers />} />
          <Route path="add" element={<AddMember />} />
          <Route path=":id" element={<MemberProfile />} />
        </Route>
        <Route path="/ministries" element={<MinistryPage />} />

        {/* Redirect unknown protected routes to dashboard */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Route>

      {/*  redirect to login */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default App;
