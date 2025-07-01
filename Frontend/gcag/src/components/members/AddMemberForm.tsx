import { useState } from "react";

export default function AddMemberForm() {
  const [firstName, setFirstName] = useState("");
  // ...other fields

  return (
    <form className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm mb-1">First Name *</label>
          <input
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            className="w-full border rounded-md px-4 py-2"
          />
        </div>
        {/* Last name, email, phone, etc. */}
      </div>
      <button
        type="submit"
        className="mt-4 bg-[#5D0676] text-white px-6 py-2 rounded-md"
      >
        Save Member
      </button>
    </form>
  );
}
