import { useState, useEffect } from "react";
import Table from "../components/Table";
import useCharacters from "../hooks/useCharacters";

export default function Home() {
  const characterData = useCharacters();

  const [tableData, setTableData] = useState(characterData);

  useEffect(() => {
    setTableData(characterData);
  }, [characterData]);

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

  return (
    <>
      <div className="rounded border border-1 shadow bg-primary-subtle p-4">
        <h1> Home</h1>

        <Table data={tableData} onDelete={deleteRow} />
      </div>
    </>
  );
}
