import { Input } from "../ui/input.tsx";
import { Button } from "../ui/button";
import { Mail, Lock } from "lucide-react";
import { useState } from "react";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <form className="space-y-4">
      <div>
        <label className="block text-sm mb-1">Email Address</label>
        <div className="relative">
          <Mail className="absolute left-3 top-2.5 text-gray-500" size={18} />
          <Input
            type="email"
            placeholder="eben@gmail.com"
            className="pl-10"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
      </div>

      <div>
        <label className="block text-sm mb-1">Password</label>
        <div className="relative">
          <Lock className="absolute left-3 top-2.5 text-gray-500" size={18} />
          <Input
            type="password"
            placeholder="******************"
            className="pl-10"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <input type="checkbox" id="2fa" />
        <label htmlFor="2fa" className="text-sm">
          Set up Two-Factor Authentication
        </label>
      </div>

      <div className="flex items-center space-x-2">
        <input type="checkbox" id="remember" />
        <label htmlFor="remember" className="text-sm">
          Remember me
        </label>
      </div>

      <div className="flex justify-between items-center">
        <div />
        <a
          href="/forgot-password"
          className="text-sm text-purple-600 hover:underline"
        >
          Forgot Password?
        </a>
      </div>

      <Button
        type="submit"
        className="w-full bg-gradient-to-r from-purple-400 to-purple-700 cursor-pointer hover:bg-purple-800 text-white"
      >
        Continue →
      </Button>
    </form>
  );
}
