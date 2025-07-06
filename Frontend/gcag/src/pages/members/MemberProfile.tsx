// src/pages/members/MemberProfile.tsx
import { useParams } from "react-router-dom";
import { User } from "lucide-react";
import { recentMembers } from "../../data/MockData";

export default function MemberProfile() {
  const { id } = useParams<{ id: string }>();
  const member = recentMembers.find((_, i) => String(i + 1) === id);

  if (!member) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <p className="text-gray-500">Member not found.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <div className="w-24 h-24 rounded-full bg-gray-100 flex items-center justify-center">
          <User className="w-12 h-12 text-gray-400" />
        </div>
        <div>
          <h2 className="text-2xl font-semibold">{member.name}</h2>
          <p className="text-sm text-gray-500">Joined: {member.joinDate}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Personal Details */}
        <div>
          <h3 className="text-lg font-semibold text-[#5D0676] mb-3">
            Personal Details
          </h3>
          <div className="space-y-2 text-sm">
            <p>
              <span className="font-medium">Email:</span> {member.email}
            </p>
            <p>
              <span className="font-medium">Phone:</span> {member.phone}
            </p>
          </div>
        </div>

        {/* Church Details */}
        <div>
          <h3 className="text-lg font-semibold text-[#5D0676] mb-3">
            Church Details
          </h3>
          <div className="space-y-2 text-sm">
            <p>
              <span className="font-medium">Ministry:</span> {member.ministry}
            </p>
            <p>
              <span className="font-medium">Tithe Status:</span>{" "}
              {member.titheStatus}
            </p>
            <p>
              <span className="font-medium">Welfare Eligible:</span>{" "}
              {member.welfareEligible ? "Yes" : "No"}
            </p>
            <p>
              <span className="font-medium">Attendance:</span>{" "}
              {member.attendanceStatus}
            </p>
            <p>
              <span className="font-medium">Last Tithe Date:</span>{" "}
              {member.lastTitheDate}
            </p>
          </div>
        </div>
      </div>

      {/* Additional Information */}
    </div>
  );
}
