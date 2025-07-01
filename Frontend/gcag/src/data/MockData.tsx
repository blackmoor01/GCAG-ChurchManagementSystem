import type { Stat, QuickAction, Member } from "../types";
import {
  Users,
  DollarSign,
  Heart,
  Activity,
  Calendar,
  Settings,
  UsersRound,
} from "lucide-react";

// Dashboard statistics (top cards)
export const stats: Stat[] = [
  {
    title: "Total Members",
    value: "1,230",
    change: "+7.1% this week",
    icon: <Users />,
  },
  {
    title: "Finance",
    value: "$24,800",
    change: "+5.3% finance raised",
    icon: <DollarSign />,
  },
  {
    title: "Welfare",
    value: "$22,800",
    change: "+5.1% this month",
    icon: <Heart />,
  },
  {
    title: "Active Ministries",
    value: "12",
    change: "2 new added this week",
    icon: <Activity />,
  },
];

// Dashboard Quick Actions
export const quickActions: QuickAction[] = [
  {
    title: "Members Management",
    description: "Manage members, profiles, groups",
    icon: <UsersRound />,
  },
  {
    title: "Ministries",
    description: "Manage and monitor church ministries",
    icon: <Activity />,
  },
  {
    title: "Events",
    description: "Schedule and manage church events",
    icon: <Calendar />,
  },
  {
    title: "Settings",
    description: "Manage application and preferences",
    icon: <Settings />,
  },
];

// Recent members list (expanded shape)
export const recentMembers: Member[] = [
  {
    name: "Gideon Danso",
    joinDate: "May 12, 2019",
    email: "gideon.danso@example.com",
    phone: "+233 20 123 4567",
    titheStatus: "Paid",
    welfareEligible: true,
    attendanceStatus: "Active",
    ministry: "Music Ministry",
    lastTitheDate: "06/15/2025",
  },
  {
    name: "Emmanuel Quayson",
    joinDate: "May 12, 2025",
    email: "emmanuel.quayson@example.com",
    phone: "+233 24 234 5678",
    titheStatus: "Pending",
    welfareEligible: false,
    attendanceStatus: "Active",
    ministry: "Media Team",
    lastTitheDate: "05/20/2025",
  },
  {
    name: "Ella Gyan",
    joinDate: "June 12, 2024",
    email: "ella.gyan@example.com",
    phone: "+233 24 345 6789",
    titheStatus: "Overdue",
    welfareEligible: false,
    attendanceStatus: "Inactive",
    ministry: "Young Singles",
    lastTitheDate: "03/01/2025",
  },
  {
    name: "Emmanuel Brannor",
    joinDate: "Jan 12, 2025",
    email: "emmanuel.brannor@example.com",
    phone: "+233 24 456 7890",
    titheStatus: "Paid",
    welfareEligible: true,
    attendanceStatus: "Active",
    ministry: "Men’s Ministry",
    lastTitheDate: "06/01/2025",
  },
  {
    name: "Ofori Amponsah",
    joinDate: "Oct 12, 2023",
    email: "ofori.amponsah@example.com",
    phone: "+233 24 567 8901",
    titheStatus: "Pending",
    welfareEligible: true,
    attendanceStatus: "Active",
    ministry: "Pathfinder Club",
    lastTitheDate: "05/30/2025",
  },
];
