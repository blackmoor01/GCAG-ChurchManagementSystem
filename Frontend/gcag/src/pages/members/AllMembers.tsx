import { useOutletContext } from "react-router-dom";
import RecentMembersTable from "../../components/dashboard/RecentMemberTable";
import { recentMembers } from "../../data/MockData";

type ContextType = { searchTerm: string };

export default function AllMembers() {
  const { searchTerm } = useOutletContext<ContextType>();

  // Filter by member name (case‑insensitive)
  const filteredMembers = recentMembers.filter((m) =>
    m.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <RecentMembersTable members={filteredMembers} />
    </div>
  );
}
