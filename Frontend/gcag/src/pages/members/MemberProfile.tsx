// src/pages/members/MemberProfile.tsx
import { useParams } from "react-router-dom";

export default function MemberProfile() {
  const { id } = useParams<{ id: string }>();
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4">Profile: Member #{id}</h3>
      {/* Fetch & display that member’s details here */}
    </div>
  );
}
