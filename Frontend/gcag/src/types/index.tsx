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

export interface Member {
  name: string;
  joinDate: string;
  status: string;
  groups: string[];
}
