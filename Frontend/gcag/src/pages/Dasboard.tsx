import Layout from "../components/layout/layout";
import StatsCard from "../components/dashboard/StatsCard";
import QuickActions from "../components/dashboard/QuickActions";
import UpcomingEvents from "../components/dashboard/UpcomingEvents";
import RecentMembersTable from "../components/dashboard/RecentMemberTable";

import { stats, quickActions, recentMembers } from "../data/MockData";

export default function DashboardPage() {
  return (
    <Layout>
      <h2 className="text-xl font-bold mb-4">Welcome, Rev Ebenezer</h2>
      <p>Here is what`s happening at your church</p>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {stats.map((stat, i) => (
          <StatsCard key={i} data={stat} />
        ))}
      </div>

      {/* Quick Actions & Upcoming Events */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        <div className="lg:col-span-2">
          <QuickActions actions={quickActions} />
        </div>
        <UpcomingEvents />
      </div>

      {/* Recent Members */}
      <RecentMembersTable members={recentMembers} />
    </Layout>
  );
}
