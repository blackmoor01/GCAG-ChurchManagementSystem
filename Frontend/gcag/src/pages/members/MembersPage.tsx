import { NavLink, Outlet } from "react-router-dom";
import { useState } from "react";

const tabs = [
  { label: "All Members", to: "" }, // index route
  { label: "Add Member", to: "add" },
  { label: "Member Profile", to: "1" }, // placeholder; real IDs come from table
];

export default function MembersPage() {
  const [searchTerm, setSearchTerm] = useState("");

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold">Members</h2>
        <p className="text-sm text-gray-600">
          Manage church members and their information
        </p>
      </div>

      {/* Search Bar */}
      <div className="w-full max-w-md">
        <input
          type="text"
          placeholder="Search members..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full border rounded-md px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#5D0676]"
        />
      </div>

      {/* Tabs */}
      <nav className="border-b border-gray-200">
        <ul className="flex -mb-px">
          {tabs.map((tab) => (
            <li key={tab.to} className="mr-6">
              <NavLink
                to={tab.to}
                end={tab.to === ""}
                className={({ isActive }) =>
                  "inline-block pb-2 text-sm font-medium " +
                  (isActive
                    ? "text-[#5D0676] border-b-2 border-[#5D0676]"
                    : "text-gray-500 hover:text-gray-700")
                }
              >
                {tab.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* Sub‑page content, passing searchTerm down */}
      <div className="pt-4">
        <Outlet context={{ searchTerm }} />
      </div>
    </div>
  );
}
