// src/components/layout/Layout.tsx
import { useState } from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function Layout() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="flex">
      {/* Fixed, collapsible sidebar */}
      <Sidebar collapsed={collapsed} />

      {/* Main content: shifts based on sidebar width */}
      <div
        className={`flex-1 flex flex-col transition-all duration-300 ${
          collapsed ? "ml-20" : "ml-64"
        }`}
      >
        {/* Topbar with hamburger toggle */}
        <Topbar onToggleSidebar={() => setCollapsed((prev) => !prev)} />

        {/* Outlet renders the matched child route (dashboard, members, etc.) */}
        <main className="p-6 bg-gray-50 min-h-screen">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
