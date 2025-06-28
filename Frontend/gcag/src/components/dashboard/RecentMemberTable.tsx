import type { Member } from "../../types";

type Props = {
  members: Member[];
};

export default function RecentMembersTable({ members }: Props) {
  return (
    <div className="bg-white shadow rounded-lg p-6 mt-6 overflow-auto">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">Recent Members</h3>
        <a href="#" className="text-sm text-purple-700 hover:underline">
          View all
        </a>
      </div>
      <table className="min-w-full text-sm text-left table-auto">
        <thead className="bg-gray-100">
          <tr className="text-gray-600">
            <th className="p-3">Name</th>
            <th className="p-3">Join Date</th>
            <th className="p-3">Status</th>
            <th className="p-3">Groups</th>
            <th className="p-3">Action</th>
          </tr>
        </thead>
        <tbody>
          {members.map((m: Member, i: number) => (
            <tr key={i} className="border-t hover:bg-gray-50">
              <td className="p-3">{m.name}</td>
              <td className="p-3">{m.joinDate}</td>
              <td className="p-3">
                <span
                  className={`px-2 py-1 rounded text-xs font-medium ${
                    m.status === "ACTIVE"
                      ? "bg-green-100 text-green-700"
                      : "bg-gray-200 text-gray-600"
                  }`}
                >
                  {m.status}
                </span>
              </td>
              <td className="p-3 text-gray-700">{m.groups.join(", ")}</td>
              <td className="p-3">
                <a href="#" className="text-purple-600 hover:underline">
                  View
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
