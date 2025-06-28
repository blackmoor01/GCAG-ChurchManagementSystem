import type { QuickAction } from "../../types";

type Props = {
  actions: QuickAction[];
};

export default function QuickActions({ actions }: Props) {
  return (
    <div className="grid grid-cols-2 gap-4">
      {actions.map((action, idx) => (
        <div key={idx} className="bg-white shadow-sm rounded-lg p-4">
          <div className="text-purple-700 mb-2">{action.icon}</div>
          <h4 className="font-semibold text-sm">{action.title}</h4>
          <p className="text-xs text-gray-500">{action.description}</p>
        </div>
      ))}
    </div>
  );
}
