import AddMemberForm from "../../components/members/AddMemberForm";

export default function AddMember() {
  return (
    <div className="bg-white rounded-lg shadow p-6 overflow-x-hidden">
      <h3 className="text-lg font-semibold mb-4">Add New Member</h3>
      <AddMemberForm />
    </div>
  );
}
