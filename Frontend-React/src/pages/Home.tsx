import { useState, useEffect } from "react";
import Table from "../components/Table";
import useCharacters from "../hooks/useCharacters";

export default function Home() {
  // const [tableData, setTableData] = useState<Array<Record<string, any>>>([]);
  const [ tableData, setTableData] = useState(useCharacters)

  // const url = "http://localhost:5000/groups/api/current-players";

  const deleteRow = async (id: number) => {
    try {
      const response = await fetch(`url`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("failed to delete row");
      }
      setTableData((prevData) => prevData.filter((row) => row.id !== id));
    } catch (error) {
      console.error("error deleting row: ", error);
    }
  };

  // const fetchTableData = async () => {
  //   try {
  //     const response = await fetch(url);
  //     const data = await response.json();
  //     setTableData(data); // Update table data
  //   } catch (error) {
  //     console.error("Error fetching data:", error);
  //   }
  // };

  // useEffect(() => {
  //   fetchTableData();
  // }, []);

  return (
    <>
      <div className="rounded border border-1 shadow bg-primary-subtle p-4">
        <h1> Home</h1>

        <Table data={tableData} onDelete={deleteRow} />
      </div>
    </>
  );
}
