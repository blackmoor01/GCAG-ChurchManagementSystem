import { useState } from "react";
import { useNavigate } from "react-router-dom"; // Needed for navigation
import RoleSelector from "../components/auth/RoleSelector";
import LoginForm from "../components/auth/LoginForm";

import aglogo from "../assets/images/aglogo.png";
import logo from "../assets/images/logo.png";

export default function LoginPage() {
  const [role, setRole] = useState("Head Pastor");
  const navigate = useNavigate(); // for navigating to /register

  return (
    <div className="min-h-screen flex items-center justify-center bg-login-page p-4">
      {/* Responsive wrapper that mimics a card */}
      <div className="flex flex-col md:flex-row w-full max-w-5xl rounded-2xl shadow-2xl overflow-hidden">
        {/* LEFT PANEL - Purple background with logos and selector */}
        <div
          className="w-full md:w-1/2 text-white flex flex-col"
          style={{ backgroundColor: "#5D0676" }}
        >
          {/* Top: Assemblies of God Ghana logo and name */}
          <div className="flex items-center px-8 py-4">
            <img
              src={logo}
              alt="Assemblies of God Ghana"
              className="h-10 w-10"
            />
            <span className="ml-4 font-semibold uppercase">
              Assemblies of God Ghana
            </span>
          </div>

          {/* Center: Chapel logo and title */}
          <div className="flex-1 flex flex-col items-center justify-center px-8 space-y-4">
            <img src={aglogo} alt="Glory City Chapel" className="w-40 h-40" />
            <h1 className="text-xl font-bold">GLORY CITY CHAPEL</h1>
            <p className="text-sm">MANAGEMENT SYSTEM</p>
          </div>

          {/* Bottom: Role selector */}
          <div className="px-8 py-6">
            <RoleSelector value={role} onChange={setRole} />
          </div>
        </div>

        {/* RIGHT PANEL - Sign In Form */}
        <div className="w-full md:w-1/2 bg-white p-8 md:p-12">
          {/* Tab headers */}
          <div className="mb-6 border-b border-gray-200">
            <div className="flex space-x-6">
              {/* SIGN IN (active) */}
              <span
                className="font-semibold pb-2 cursor-pointer "
                style={{
                  color: "#5D0676",
                  borderBottom: "2px solid #5D0676",
                }}
              >
                SIGN IN
              </span>

              {/* REGISTER (clickable link to register page) */}
              <span
                className="text-gray-400 pb-2 cursor-pointer"
                onClick={() => navigate("/register")}
              >
                REGISTER
              </span>
            </div>
          </div>

          {/* Header & description */}
          <h2 className="text-2xl font-bold mb-1">Welcome Back</h2>
          <p className="text-sm text-gray-500 mb-6">
            Sign in to your management system
          </p>

          {/* The login form component */}
          <LoginForm />
        </div>
      </div>
    </div>
  );
}
