import type { Stat } from "../../types";

type Props = {
  data: Stat;
};

export default function StatsCard({ data }: Props) {
  return (
    <div className="transform transition-transform duration-300 hover:-translate-y-1 hover:shadow-lg bg-white shadow-sm rounded-lg p-4 flex items-center justify-between">
      <div>
        <p className="text-sm text-gray-500">{data.title}</p>
        <h2 className="text-xl font-bold">{data.value}</h2>
        <p className="text-xs text-green-600">{data.change}</p>
      </div>
      <div className="text-purple-700">{data.icon}</div>
    </div>
  );
}
