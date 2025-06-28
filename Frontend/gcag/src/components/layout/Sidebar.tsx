// src/components/layout/Sidebar.tsx
import { Link, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  Users,
  Church,
  Calendar,
  Heart,
  Settings,
  LogOut,
  CreditCard,
} from "lucide-react";

type SidebarProps = {
  collapsed: boolean;
};

const menuItems = [
  { label: "Dashboard", icon: <LayoutDashboard />, to: "/dashboard" },
  { label: "Members", icon: <Users />, to: "/members" },
  { label: "Ministries", icon: <Church />, to: "/ministries" },
  { label: "Events", icon: <Calendar />, to: "/events" },
  { label: "Welfare", icon: <Heart />, to: "/welfare" },
  { label: "Finance", icon: <CreditCard />, to: "/finance" },
  { label: "Settings", icon: <Settings />, to: "/settings" },
];

export default function Sidebar({ collapsed }: SidebarProps) {
  const location = useLocation();

  return (
    <aside
      className={`fixed top-0 left-0 h-screen bg-[#5D0676] text-white z-20
        flex flex-col justify-between transition-all duration-300
        ${collapsed ? "w-20" : "w-64"}`}
    >
      <div>
        {/* Header */}
        <div className="py-6 text-center">
          {!collapsed && (
            <h2 className="text-lg font-bold tracking-wide">
              GLORY CITY CHAPEL
            </h2>
          )}
        </div>

        {/* Menu */}
        <nav className="flex-1">
          <ul className="space-y-2">
            {menuItems.map((item) => {
              const isActive = location.pathname === item.to;
              return (
                <li key={item.label}>
                  <Link
                    to={item.to}
                    className={[
                      "flex items-center rounded transition-colors duration-200",
                      isActive ? "bg-purple-800" : "hover:bg-purple-700",
                      collapsed
                        ? "justify-center py-3"
                        : "justify-start px-4 py-3",
                    ].join(" ")}
                  >
                    {/* Icon */}
                    <span className="flex-shrink-0 text-xl">{item.icon}</span>

                    {/* Label */}
                    {!collapsed && (
                      <span className="ml-3 text-sm font-medium">
                        {item.label}
                      </span>
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      </div>

      {/* Logout */}
      <div className="pb-6">
        <Link
          to="/logout"
          className={[
            "flex items-center rounded transition-colors duration-200",
            collapsed ? "justify-center py-3" : "justify-start px-4 py-3",
            "hover:bg-purple-700",
          ].join(" ")}
        >
          <span className="flex-shrink-0 text-xl">
            <LogOut />
          </span>
          {!collapsed && (
            <span className="ml-3 text-sm font-medium">Logout</span>
          )}
        </Link>
      </div>
    </aside>
  );
}
