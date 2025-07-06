import MinistryStats from "../../components/ministries/MinistryStats";
import { useState } from "react";

export default function MinistryPage() {
  const [tab, setTab] = useState("list");
  const [search, setSearch] = useState("");

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Ministry Management</h2>
          <p className="text-sm text-gray-600">
            Manage church ministries, leaders, and member communications
          </p>
        </div>
        <button className="bg-[#5D0676] text-white px-4 py-2 rounded-md text-sm">
          + Add Ministry
        </button>
      </div>

      {/* Stats */}
      <MinistryStats />

      {/* Tabs */}
      <div className="flex items-center justify-between border-b">
        <div className="space-x-4">
          <button
            onClick={() => setTab("list")}
            className={`pb-2 text-sm font-medium cursor-pointer ${
              tab === "list"
                ? "text-[#5D0676] border-b-2 border-[#5D0676]"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            Ministry List
          </button>
          <button
            onClick={() => setTab("category")}
            className={`pb-2 text-sm font-medium cursor-pointer ${
              tab === "category"
                ? "text-[#5D0676] border-b-2 border-[#5D0676]"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            By Category
          </button>
        </div>

        {/* Search + Filter */}
        <div className="flex items-center gap-2">
          <input
            type="text"
            placeholder="Search ministries..."
            className="border px-3 py-2 text-sm rounded-md"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <select className=" border border-gray-300 bg-white text-gray-900px-3 py-2 text-sm rounded-md hover:border-[#5D0676]">
            <option className="bg-white text-gray-900">Youth</option>
            <option className="bg-white text-gray-900">Worship</option>
            <option className="bg-white text-gray-900">Service</option>
            <option className="bg-white text-gray-900">Children</option>
            <option className="bg-white text-gray-900">Fellowship</option>
            <option className="bg-white text-gray-900">Evangelism</option>
            <option className="bg-white text-gray-900">Media</option>
            <option className="bg-white text-gray-900">Administration</option>
          </select>
        </div>
      </div>
    </div>
  );
}
