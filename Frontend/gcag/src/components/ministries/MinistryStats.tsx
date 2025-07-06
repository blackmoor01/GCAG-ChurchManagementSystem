// src/components/ministries/MinistryStats.tsx
import { Church, Users, CreditCard } from "lucide-react";

type StatCardProps = {
  title: string;
  value: string | number;
  subtext?: string;
  icon: React.ReactNode;
};

export default function MinistryStats() {
  const stats: StatCardProps[] = [
    {
      title: "Total Ministries",
      value: 6,
      subtext: "6 active",
      icon: <Church className="w-5 h-5 text-[#5D0676]" />,
    },
    {
      title: "Total Members",
      value: 336,
      subtext: "Across all ministries",
      icon: <Users className="w-5 h-5 text-[#5D0676]" />,
    },
    {
      title: "Average Size",
      value: 56,
      subtext: "Members per ministry",
      icon: <Users className="w-5 h-5 text-[#5D0676]" />,
    },
    {
      title: "Total Budget",
      value: "GH₵11,900",
      subtext: "Annual allocation",
      icon: <CreditCard className="w-5 h-5 text-[#5D0676]" />,
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {stats.map((stat) => (
        <div
          key={stat.title}
          className="transform transition-transform duration-300 hover:-translate-y-2 hover:shadow-lg bg-white rounded-lg shadow p-4 border border-gray-100 flex items-center justify-between hover:"
        >
          <div>
            <h4 className="text-sm text-gray-600 font-medium">{stat.title}</h4>
            <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
            {stat.subtext && (
              <p className="text-xs text-gray-500 mt-1">{stat.subtext}</p>
            )}
          </div>
          <div>{stat.icon}</div>
        </div>
      ))}
    </div>
  );
}
