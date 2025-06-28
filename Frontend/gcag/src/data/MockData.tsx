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

//  Dashboard statistics (top cards)
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

//  Recent members list
export const recentMembers: Member[] = [
  {
    name: "Gideon Darso",
    joinDate: "May 12, 2019",
    status: "ACTIVE",
    groups: ["Music", "Youth", "Pain Raiser"],
  },
  {
    name: "Gideon Darso",
    joinDate: "May 12, 2019",
    status: "ACTIVE",
    groups: ["Music", "Youth", "Pain Raiser"],
  },
];
