import GroupTable from "../components/GroupTable";
import { useLocation } from "react-router-dom";

export default function GroupListPage() {
  const location = useLocation();
  const { data } = location.state || {};

  return (
    <>
      <div className="rounded border border-1 shadow bg-primary-subtle p-4">
        <h1>Groups</h1>
        <GroupTable data={data} onRowClick={() => {}} />
      </div>
      "
    </>
  );
}
