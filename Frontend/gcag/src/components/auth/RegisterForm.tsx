// src/components/auth/RegisterForm.tsx

import { useState } from "react";
import RoleSelector from "./RoleSelector";

export default function RegisterForm() {
  const [role, setRole] = useState("Admin");
  const [agreed, setAgreed] = useState(false);

  return (
    <form className="space-y-6">
      {/* SECTION: Basic Info */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {/* Full Name */}
        <div className="flex flex-col">
          <label htmlFor="name" className="text-sm font-medium mb-1">
            Full Name
          </label>
          <input
            id="name"
            type="text"
            placeholder="Ebenezer Essibu"
            required
            className="w-full px-4 py-2 border rounded-md text-sm focus:ring-2 focus:ring-purple-500 focus:outline-none"
          />
        </div>

        {/* Email */}
        <div className="flex flex-col">
          <label htmlFor="email" className="text-sm font-medium mb-1">
            Email Address
          </label>
          <input
            id="email"
            type="email"
            placeholder="eben@gmail.com"
            required
            className="w-full px-4 py-2 border rounded-md text-sm focus:ring-2 focus:ring-purple-500 focus:outline-none"
          />
        </div>

        {/* Role */}
        <div className="flex flex-col">
          <label htmlFor="role" className="text-sm font-medium mb-1">
            Role
          </label>
          <RoleSelector value={role} onChange={setRole} />
        </div>

        {/* Password */}
        <div className="flex flex-col">
          <label htmlFor="password" className="text-sm font-medium mb-1">
            Password
          </label>
          <input
            id="password"
            type="password"
            placeholder="**********"
            required
            className="w-full px-4 py-2 border rounded-md text-sm focus:ring-2 focus:ring-purple-500 focus:outline-none"
          />
        </div>
      </div>

      {/* SECTION: Password Tips */}
      <div className="text-sm text-gray-600 mt-1">
        <ul className="list-disc pl-5 space-y-1">
          <li>At least 8 characters</li>
          <li>One uppercase letter</li>
          <li>One number</li>
        </ul>
      </div>

      {/* SECTION: Terms */}
      <div className="flex items-start space-x-3">
        <input
          id="terms"
          type="checkbox"
          checked={agreed}
          onChange={() => setAgreed(!agreed)}
          className="mt-1 accent-purple-700"
        />
        <label htmlFor="terms" className="text-sm text-gray-700 leading-5">
          I agree to the <span className="underline">Terms of Service</span> and{" "}
          <span className="underline">Privacy Policy</span>
        </label>
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={!agreed}
        className={`w-full py-3 text-white rounded-lg font-semibold transition-all ${
          agreed
            ? "bg-gradient-to-r from-purple-700 to-purple-900 hover:opacity-90"
            : "bg-gray-300 cursor-not-allowed"
        }`}
      >
        Create Account
      </button>
    </form>
  );
}
