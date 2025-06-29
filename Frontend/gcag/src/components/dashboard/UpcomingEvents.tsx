// src/components/dashboard/UpcomingEvents.tsx
import { Calendar as CalendarIcon, Repeat, Star } from "lucide-react";

type WeeklyEvent = {
  day: string;
  title: string;
};

type SpecialEvent = {
  title: string;
  start: string;
  end: string;
};

const weeklyEvents: WeeklyEvent[] = [
  { day: "Sunday", title: "Recurring Service" },
  { day: "Wednesday", title: "Teaching (Recurring)" },
  { day: "Friday", title: "Miracle Service (Recurring)" },
];

const specialEvents: SpecialEvent[] = [
  {
    title: "Destiny Summit",
    start: "June 23, 2025",
    end: "July 6, 2025",
  },
];

export default function UpcomingEvents() {
  return (
    <div className="bg-white shadow-sm rounded-lg p-4">
      {/* Weekly Recurring */}
      <h3 className="text-lg font-semibold mb-3">Weekly Events</h3>
      <div className="space-y-2 mb-6">
        {weeklyEvents.map((ev) => (
          <div
            key={ev.day}
            className="flex items-center bg-gray-50 rounded-lg p-3"
          >
            <div className="p-2 bg-purple-100 text-purple-700 rounded-full">
              <Repeat className="w-5 h-5" />
            </div>
            <div className="ml-3">
              <p className="font-medium">{ev.day}</p>
              <p className="text-sm text-gray-600">{ev.title}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Special Programs */}
      <h3 className="text-lg font-semibold mb-3">Special Programs</h3>
      <div className="space-y-2">
        {specialEvents.map((ev) => (
          <div
            key={ev.title}
            className="flex items-center bg-gray-50 rounded-lg p-3"
          >
            <div className="p-2 bg-yellow-100 text-yellow-700 rounded-full">
              <Star className="w-5 h-5" />
            </div>
            <div className="ml-3 flex-1">
              <p className="font-medium">{ev.title}</p>
              <p className="text-sm text-gray-600">
                <CalendarIcon className="inline w-4 h-4 mr-1 align-text-bottom" />
                {ev.start} — {ev.end}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
