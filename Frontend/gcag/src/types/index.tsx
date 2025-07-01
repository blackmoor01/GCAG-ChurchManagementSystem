import type { JSX } from "react";

export interface Stat {
  title: string;
  value: string;
  change: string;
  icon: JSX.Element;
}

export interface QuickAction {
  title: string;
  description: string;
  icon: JSX.Element;
}

// Expanded Member type to match the new table columns
export interface Member {
  name: string;
  joinDate: string;
  email: string;
  phone: string;
  titheStatus: "Paid" | "Pending" | "Overdue";
  welfareEligible: boolean;
  attendanceStatus: "Active" | "Inactive" | "Pending";
  ministry: string;
  lastTitheDate: string;
}
