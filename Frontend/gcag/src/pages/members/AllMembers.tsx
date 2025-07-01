// src/pages/members/AllMembers.tsx
import RecentMemberTable from "../../components/dashboard/RecentMemberTable";
import { recentMembers } from "../../data/MockData";

export default function AllMembers() {
  return (
    <div className="bg-white rounded-lg shadow p-4 overflow-x-auto">
      <h3 className="text-lg font-semibold mb-4">Church Members</h3>
      {/* Pass the mock data into your RecentMemberTable */}
      <RecentMemberTable members={recentMembers} />
    </div>
  );
}
