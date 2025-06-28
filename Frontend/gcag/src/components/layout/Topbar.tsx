import { AlignLeft, Bell, User } from "lucide-react";

type Props = {
  onToggleSidebar: () => void;
};

export default function Topbar({ onToggleSidebar }: Props) {
  return (
    <header className="flex items-center justify-between px-6 py-4 shadow-sm bg-white sticky top-0 z-10">
      <div className="flex items-center gap-4">
        <button
          onClick={onToggleSidebar}
          className="text-purple-700 cursor-pointer"
        >
          <AlignLeft className="w-6 h-6" />
        </button>
        <h1 className="text-xl font-bold">Dashboard</h1>
      </div>
      <div className="flex items-center gap-4">
        <Bell className="w-5 h-5 text-gray-700" />
        <div className="bg-purple-100 text-purple-800 rounded-full w-8 h-8 flex items-center justify-center">
          <User className="w-4 h-4" />
        </div>
      </div>
    </header>
  );
}
