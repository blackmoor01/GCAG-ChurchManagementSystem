import { Select, SelectTrigger, SelectContent, SelectItem } from "../ui/select";

import { User } from "lucide-react";
import { roles } from "../../constants/roles";

interface RoleSelectorProps {
  value: string;
  onChange: (value: string) => void;
}

export default function RoleSelector({ value, onChange }: RoleSelectorProps) {
  return (
    <div className="flex items-center gap-2 p-2 bg-gradient-to-r from-purple-700 to-purple-700 rounded-md shadow-md">
      <User className="text-white" />
      <Select onValueChange={onChange} value={value}>
        <SelectTrigger className="w-full text-black bg-white ">
          {value}
        </SelectTrigger>
        <SelectContent>
          {roles.map((role: string) => (
            <SelectItem key={role} value={role}>
              {role}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
