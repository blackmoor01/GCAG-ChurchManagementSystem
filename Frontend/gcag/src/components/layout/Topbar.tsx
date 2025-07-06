import { AlignLeft, Bell, User, Search } from "lucide-react";

type Props = {
  onToggleSidebar: () => void;
};

export default function Topbar({ onToggleSidebar }: Props) {
  const loggedInRole = "Admin";
  const unreadCount = 3; // simulate number of notifications

  return (
    <header className="flex items-center justify-between px-6 py-4 shadow-sm bg-white sticky top-0 z-10">
      {/* Left: hamburger + search */}
      <div className="flex items-center gap-4 flex-1">
        <button
          onClick={onToggleSidebar}
          className="text-purple-700 cursor-pointer"
        >
          <AlignLeft className="w-6 h-6" />
        </button>

        {/* Search bar */}
        <div className="relative w-full max-w-md">
          <Search className="absolute left-3 top-2.5 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search members, events or records"
            className="w-full border border-gray-200 rounded-md pl-10 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-300"
          />
        </div>
      </div>

      {/* Right: notifications + profile + role */}
      <div className="flex items-center gap-4">
        {/* Bell with badge */}
        <div className="relative">
          <Bell className="w-6 h-6 text-gray-700" />
          {unreadCount > 0 && (
            <span className="absolute -top-1 -right-1 text-[10px] font-semibold bg-red-500 text-white rounded-full w-4 h-4 flex items-center justify-center">
              {unreadCount}
            </span>
          )}
        </div>

        {/* Profile icon */}
        <div className="bg-purple-100 text-purple-800 rounded-full w-8 h-8 flex items-center justify-center">
          <User className="w-4 h-4" />
        </div>

        {/* Logged‑in role */}
        <span className="text-sm font-medium text-gray-700 whitespace-nowrap">
          {loggedInRole}
        </span>
      </div>
    </header>
  );
}
