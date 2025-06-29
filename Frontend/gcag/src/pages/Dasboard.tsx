// src/pages/DashboardPage.tsx
import Layout from "../components/layout/layout";
import StatsCard from "../components/dashboard/StatsCard";
import QuickActions from "../components/dashboard/QuickActions";
import UpcomingEvents from "../components/dashboard/UpcomingEvents";
import RecentMembersTable from "../components/dashboard/RecentMemberTable";

import { stats, quickActions, recentMembers } from "../data/MockData";

export default function DashboardPage() {
  return (
    <Layout>
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-1">Welcome, Rev Ebenezer</h2>
        <p className="text-sm text-gray-600">
          Here’s what’s happening at your church
        </p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {stats.map((stat, i) => (
          <StatsCard key={i} data={stat} />
        ))}
      </div>

      {/* Quick Actions & Upcoming Events */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        {/* Quick Actions: full‑width on mobile, 2/3 on desktop */}
        <div className="col-span-1 lg:col-span-2">
          <div className="bg-white rounded-lg shadow p-4 mb-4 lg:mb-0">
            <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
            <QuickActions actions={quickActions} />
          </div>
        </div>

        {/* Upcoming Events: full‑width on mobile, 1/3 on desktop */}
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
    </Layout>
  );
}
