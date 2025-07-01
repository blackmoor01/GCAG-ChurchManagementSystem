// src/components/dashboard/RecentMembersTable.tsx
import type { Member } from "../../types";
import { User } from "lucide-react";

type Props = {
  members: Member[];
};

export default function RecentMembersTable({ members }: Props) {
  return (
    <div className="bg-white shadow rounded-lg p-6 mt-6 overflow-auto">
      <h3 className="text-lg font-semibold mb-4">Church Members</h3>
      <table className="min-w-full text-sm text-left table-auto border-separate border-spacing-y-3">
        <thead>
          <tr className="text-gray-600">
            <th className="p-3">Member</th>
            <th className="p-3">Contact</th>
            <th className="p-3">Tithe Status</th>
            <th className="p-3">Welfare Eligible</th>
            <th className="p-3">Attendance</th>
            <th className="p-3">Ministry</th>
            <th className="p-3">Last Tithe</th>
            <th className="p-3">Actions</th>
          </tr>
        </thead>
        <tbody>
          {members.map((m: Member, i: number) => (
            <tr key={i} className="bg-white hover:shadow-md transition-shadow">
              {/* Member Column */}
              <td className="p-3 align-top">
                <div className="flex items-center gap-3">
                  <User className="w-6 h-6 text-gray-400" />
                  <div>
                    <p className="font-medium text-gray-900">{m.name}</p>
                    <p className="text-xs text-gray-500">Joined {m.joinDate}</p>
                  </div>
                </div>
              </td>

              {/* Contact Column */}
              <td className="p-3 align-top">
                <p className="text-gray-900">{m.email}</p>
                <p className="text-xs text-gray-500 mt-1">{m.phone}</p>
              </td>

              {/* Tithe Status */}
              <td className="p-3 align-top">
                <span
                  className={`inline-block px-2 py-1 text-xs font-medium rounded-full ${
                    m.titheStatus === "Paid"
                      ? "bg-green-100 text-green-700"
                      : m.titheStatus === "Pending"
                      ? "bg-yellow-100 text-yellow-700"
                      : "bg-red-100 text-red-700"
                  }`}
                >
                  {m.titheStatus}
                </span>
              </td>

              {/* Welfare Eligible */}
              <td className="p-3 align-top">
                <span
                  className={`inline-block px-2 py-1 text-xs font-medium rounded-full ${
                    m.welfareEligible
                      ? "bg-purple-100 text-purple-700"
                      : "bg-gray-100 text-gray-500"
                  }`}
                >
                  {m.welfareEligible ? "Eligible" : "Not Eligible"}
                </span>
              </td>

              {/* Attendance */}
              <td className="p-3 align-top">
                <span className="inline-block px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-700">
                  {m.attendanceStatus}
                </span>
              </td>

              {/* Ministry */}
              <td className="p-3 align-top">
                <span className="inline-block px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-700">
                  {m.ministry}
                </span>
              </td>

              {/* Last Tithe */}
              <td className="p-3 align-top">{m.lastTitheDate}</td>

              {/* Actions */}
              <td className="p-3 align-top">
                <button className="text-gray-500 hover:text-gray-700">
                  •••
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
