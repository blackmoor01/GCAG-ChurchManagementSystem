import { useState } from "react";
import type { Member } from "../../types";
import { User } from "lucide-react";

type Props = {
  members: Member[];
};

export default function RecentMembersTable({ members }: Props) {
  const itemsPerPage = 5;
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(members.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentMembers = members.slice(startIndex, startIndex + itemsPerPage);

  const goToPage = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-6 mt-6 overflow-x-hidden">
      <h3 className="text-lg font-semibold mb-4">Church Members</h3>
      <div className="w-full overflow-x-auto">
        <table className="w-full text-sm text-left table-auto border-separate border-spacing-y-3">
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
            {currentMembers.map((m, i) => (
              <tr
                key={i}
                className="bg-white hover:shadow-md transition-shadow"
              >
                <td className="p-3 align-top">
                  <div className="flex items-center gap-3">
                    <User className="w-6 h-6 text-gray-400" />
                    <div>
                      <p className="font-medium text-gray-900">{m.name}</p>
                      <p className="text-xs text-gray-500">
                        Joined {m.joinDate}
                      </p>
                    </div>
                  </div>
                </td>
                <td className="p-3 align-top">
                  <p className="text-gray-900">{m.email}</p>
                  <p className="text-xs text-gray-500 mt-1">{m.phone}</p>
                </td>
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
                <td className="p-3 align-top">
                  <span className="inline-block px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-700">
                    {m.attendanceStatus}
                  </span>
                </td>
                <td className="p-3 align-top">
                  <span className="inline-block px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-700">
                    {m.ministry}
                  </span>
                </td>
                <td className="p-3 align-top">{m.lastTitheDate}</td>
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

      {/* Pagination Controls */}
      <div className="flex justify-end items-center mt-4 gap-2">
        <button
          onClick={() => goToPage(currentPage - 1)}
          disabled={currentPage === 1}
          className="px-3 py-1 text-sm border rounded disabled:opacity-50"
        >
          Prev
        </button>
        {[...Array(totalPages)].map((_, i) => (
          <button
            key={i + 1}
            onClick={() => goToPage(i + 1)}
            className={`px-3 py-1 text-sm border rounded ${
              currentPage === i + 1
                ? "bg-purple-700 text-white"
                : "hover:bg-gray-100"
            }`}
          >
            {i + 1}
          </button>
        ))}
        <button
          onClick={() => goToPage(currentPage + 1)}
          disabled={currentPage === totalPages}
          className="px-3 py-1 text-sm border rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  );
}
