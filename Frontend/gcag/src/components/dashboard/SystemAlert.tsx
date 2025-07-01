import { AlertTriangle, Calendar } from "lucide-react";

export default function SystemAlerts() {
  return (
    <div className="bg-white shadow-sm rounded-lg p-4">
      <h3 className="text-lg font-bold text-gray-900 mb-1">System Alerts</h3>
      <p className="text-sm text-gray-500 mb-4">
        Important notifications and reminders
      </p>

      <div className="space-y-3">
        {/* Tithe Alert */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 flex items-start gap-3">
          <div className="text-yellow-600 mt-1">
            <AlertTriangle className="w-5 h-5" />
          </div>
          <div>
            <p className="font-semibold text-yellow-800">
              Tithe Collection Due
            </p>
            <p className="text-sm text-yellow-700">
              5 members haven't paid their monthly tithe
            </p>
          </div>
        </div>

        {/* SMS Reminder */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 flex items-start gap-3">
          <div className="text-blue-600 mt-1">
            <Calendar className="w-5 h-5" />
          </div>
          <div>
            <p className="font-semibold text-blue-800">
              Sunday Service Reminder
            </p>
            <p className="text-sm text-blue-700">
              Send SMS reminder to all members
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
