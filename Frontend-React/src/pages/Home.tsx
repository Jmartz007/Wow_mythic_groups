import React, { useState } from "react";
import Table from "../components/Table";

export default function Home() {
  //   const url = "http://localhost:5000/groups/api/dungeons";
  const url = "http://localhost:5000/groups/api/current-players";
  const [tableData, setTableData] = useState<Array<Record<string, any>>>([]);

  const fetchTableData = async () => {
    try {
      const response = await fetch(url);
      const data = await response.json();
      setTableData(data); // Update table data
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  React.useEffect(() => {
    fetchTableData();
  }, []);

  return (
    <>
      <div className="rounded border border-1 shadow bg-primary-subtle p-4">
        <h1> Home</h1>

        <Table data={tableData} />
      </div>
    </>
  );
}
