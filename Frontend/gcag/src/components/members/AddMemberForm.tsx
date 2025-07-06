import { useState } from "react";

export default function AddMemberForm() {
  // Profile photo
  const [photo, setPhoto] = useState<File | null>(null);

  // Personal Details
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [maritalStatus, setMaritalStatus] = useState("single");
  const [occupation, setOccupation] = useState("");

  // Church Details
  const [joinDate, setJoinDate] = useState("");
  const [membershipType, setMembershipType] = useState("Full Member");
  const ministryOptions = [
    "Youth",
    "Children Ministry",
    "Church Board",
    "Women Ministry",
    "Young Singles",
    "Men Ministry",
    "Pathfinder",
  ];
  const [ministries, setMinistries] = useState<string[]>([]);
  const toggleMinistry = (name: string) =>
    setMinistries((prev) =>
      prev.includes(name) ? prev.filter((m) => m !== name) : [...prev, name]
    );

  // Emergency Contact
  const [emergencyName, setEmergencyName] = useState("");
  const [emergencyPhone, setEmergencyPhone] = useState("");
  const [notes, setNotes] = useState("");

  return (
    <form className="space-y-8 w-full">
      {/* Personal Details */}
      <div>
        <h3 className="text-lg font-semibold text-[#5D0676] mb-4">
          Personal Details
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-start">
          {/* Photo Upload */}
          <div className="flex flex-col items-center">
            <div className="w-32 h-32 rounded-full overflow-hidden border border-gray-300 bg-gray-100 flex items-center justify-center">
              {photo ? (
                <img
                  src={URL.createObjectURL(photo)}
                  alt="Profile"
                  className="w-full h-full object-cover"
                />
              ) : (
                <span className="text-gray-400 text-sm">No Photo</span>
              )}
            </div>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => {
                if (e.target.files?.[0]) setPhoto(e.target.files[0]);
              }}
              className="mt-2 text-sm"
            />
          </div>

          {/* Fields */}
          <div className="md:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm mb-1">First Name *</label>
              <input
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                className="w-full border rounded-md px-4 py-2"
              />
            </div>
            <div>
              <label className="block text-sm mb-1">Last Name *</label>
              <input
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                className="w-full border rounded-md px-4 py-2"
              />
            </div>
            <div>
              <label className="block text-sm mb-1">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full border rounded-md px-4 py-2"
              />
            </div>
            <div>
              <label className="block text-sm mb-1">Phone</label>
              <input
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="w-full border rounded-md px-4 py-2"
              />
            </div>
            <div>
              <label className="block text-sm mb-1">Marital Status</label>
              <select
                value={maritalStatus}
                onChange={(e) => setMaritalStatus(e.target.value)}
                className="w-full border rounded-md px-4 py-2"
              >
                <option>Single</option>
                <option>Married</option>
                <option>Divorced</option>
                <option>Widowed</option>
              </select>
            </div>
            <div>
              <label className="block text-sm mb-1">Occupation</label>
              <input
                value={occupation}
                onChange={(e) => setOccupation(e.target.value)}
                className="w-full border rounded-md px-4 py-2"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Church Details */}
      <div>
        <h3 className="text-lg font-semibold text-[#5D0676] mb-4">
          Church Details
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm mb-1">Join Date</label>
            <input
              type="date"
              value={joinDate}
              onChange={(e) => setJoinDate(e.target.value)}
              className="w-full border rounded-md px-4 py-2"
            />
          </div>
          <div>
            <label className="block text-sm mb-1">Membership Type</label>
            <select
              value={membershipType}
              onChange={(e) => setMembershipType(e.target.value)}
              className="w-full border rounded-md px-4 py-2"
            >
              <option>Full Member</option>
              <option>Visitor</option>
              <option>Associate Member</option>
            </select>
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm mb-1">Ministry Involvement</label>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {ministryOptions.map((m) => (
                <label key={m} className="flex items-center gap-2 text-sm">
                  <input
                    type="checkbox"
                    checked={ministries.includes(m)}
                    onChange={() => toggleMinistry(m)}
                    className="form-checkbox"
                  />
                  {m}
                </label>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Emergency Contact & Notes */}
      <div>
        <h3 className="text-lg font-semibold text-[#5D0676] mb-4">
          Emergency Contact
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm mb-1">Contact Name</label>
            <input
              value={emergencyName}
              onChange={(e) => setEmergencyName(e.target.value)}
              className="w-full border rounded-md px-4 py-2"
            />
          </div>
          <div>
            <label className="block text-sm mb-1">Contact Phone</label>
            <input
              value={emergencyPhone}
              onChange={(e) => setEmergencyPhone(e.target.value)}
              className="w-full border rounded-md px-4 py-2"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm mb-1">Notes</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={4}
              className="w-full border rounded-md px-4 py-2"
            />
          </div>
        </div>
      </div>

      {/* Submit */}
      <div>
        <button
          type="submit"
          className="bg-[#5D0676] text-white px-6 py-2 rounded-md cursor-pointer"
        >
          Save Member
        </button>
      </div>
    </form>
  );
}
