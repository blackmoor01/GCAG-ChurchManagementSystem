// src/pages/DashboardPage.tsx
import { useNavigate } from "react-router-dom";
import DashboardHero from "../components/dashboard/DashboardHero";
import StatsCard from "../components/dashboard/StatsCard";
import QuickActions from "../components/dashboard/QuickActions";
import UpcomingEvents from "../components/dashboard/UpcomingEvents";
import RecentMembersTable from "../components/dashboard/RecentMemberTable";
import SystemAlert from "../components/dashboard/SystemAlert";

import { stats, quickActions, recentMembers } from "../data/MockData";

export default function DashboardPage() {
  const navigate = useNavigate();

  return (
    <>
      {/* Hero Banner */}
      <DashboardHero
        name="Rev Ebenezer"
        onAddMember={() => navigate("/members/add")}
        onScheduleEvent={() => navigate("/events")}
      />

      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {stats.map((stat, i) => (
          <StatsCard key={i} data={stat} />
        ))}
      </div>

      {/* Quick Actions & System Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        <div className="col-span-1 lg:col-span-2 space-y-4">
          <div className="bg-white rounded-lg shadow p-4">
            <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
            <QuickActions actions={quickActions} />
          </div>
          <SystemAlert />
        </div>

        {/* Upcoming Events */}
        <div>
          <div className="bg-white rounded-lg shadow p-4">
            <h3 className="text-lg font-semibold mb-4">Upcoming Events</h3>
            <UpcomingEvents />
          </div>
        </div>
      </div>

      {/* Recent Members Table */}
      <div className="bg-white rounded-lg shadow p-4 overflow-x-auto">
        <h3 className="text-lg font-semibold mb-4">Recent Members</h3>
        <RecentMembersTable members={recentMembers} />
      </div>
    </>
  );
}
