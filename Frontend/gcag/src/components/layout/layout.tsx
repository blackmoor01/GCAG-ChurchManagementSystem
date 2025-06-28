import { useState } from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function Layout({ children }: { children: React.ReactNode }) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="flex">
      <Sidebar collapsed={collapsed} />
      <div
        className={`flex-1 flex flex-col transition-all duration-300
          ${collapsed ? "ml-20" : "ml-64"}`}
      >
        <Topbar onToggleSidebar={() => setCollapsed((prev) => !prev)} />
        <main className="p-6 bg-gray-50 min-h-screen">{children}</main>
      </div>
    </div>
  );
}
