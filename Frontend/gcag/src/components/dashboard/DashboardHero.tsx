import { Plus, Calendar as CalendarIcon } from "lucide-react";
import heroBg from "../../assets/images/heroBg.jpg";

interface DashboardHeroProps {
  name: string;
  onAddMember: () => void;
  onScheduleEvent: () => void;
}

export default function DashboardHero({
  name,
  onAddMember,
  onScheduleEvent,
}: DashboardHeroProps) {
  return (
    <div
      className="relative rounded-2xl overflow-hidden mb-6"
      style={{
        backgroundImage: `url(${heroBg})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      {/* Overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-800/80 to-blue-800/60" />

      {/* Content */}
      <div className="relative p-8 md:p-12 text-white">
        <h1 className="text-3xl md:text-4xl font-bold mb-2">
          Welcome back, {name}!
        </h1>
        <p className="text-sm md:text-base mb-6">
          Your church community is growing beautifully. Here’s what’s happening
          this week.
        </p>

        <div className="flex flex-col sm:flex-row gap-4">
          <button
            onClick={onAddMember}
            className="inline-flex items-center justify-center gap-2 bg-purple-500 hover:bg-purple-600 text-white rounded-full px-5 py-2 text-sm font-medium shadow-lg transition"
          >
            <Plus className="w-4 h-4" /> Add New Member
          </button>
          <button
            onClick={onScheduleEvent}
            className="inline-flex items-center justify-center gap-2 border border-white hover:bg-white/10 rounded-full px-5 py-2 text-sm font-medium transition"
          >
            <CalendarIcon className="w-4 h-4" /> Schedule Event
          </button>
        </div>
      </div>
    </div>
  );
}
