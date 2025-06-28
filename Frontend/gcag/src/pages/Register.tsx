// src/pages/RegisterPage.tsx

import { useNavigate } from "react-router-dom";
import RegisterForm from "../components/auth/RegisterForm";
import aglogo from "../assets/images/aglogo.png";
import logo from "../assets/images/logo.png";

export default function RegisterPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-login-page p-4">
      <div className="flex flex-col md:flex-row w-full max-w-5xl rounded-2xl shadow-2xl overflow-hidden">
        {/* Left Branding Panel */}
        <div
          className="w-full md:w-1/2 text-white flex flex-col"
          style={{ backgroundColor: "#5D0676" }}
        >
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
          <div className="flex-1 flex flex-col items-center justify-center px-8 space-y-4">
            <img src={aglogo} alt="Glory City Chapel" className="w-40 h-40" />
            <h1 className="text-xl font-bold">GLORY CITY CHAPEL</h1>
            <p className="text-sm">MANAGEMENT SYSTEM</p>
          </div>
        </div>

        {/* Right Form Panel */}
        <div className="w-full md:w-1/2 bg-white p-8 md:p-12">
          <div className="mb-6 border-b border-gray-200">
            <div className="flex space-x-6">
              <span
                className="text-purple-700 font-semibold pb-2 cursor-pointer"
                style={{ borderBottom: "2px solid #5D0676" }}
              >
                REGISTER
              </span>
              <span
                className="text-gray-400 pb-2 cursor-pointer"
                onClick={() => navigate("/login")}
              >
                SIGN IN
              </span>
            </div>
          </div>

          <h2 className="text-2xl font-bold mb-1">Create Account</h2>
          <p className="text-sm text-gray-500 mb-6">
            Sign up to your management system
          </p>

          {/* Extracted Register Form */}
          <RegisterForm />
        </div>
      </div>
    </div>
  );
}
