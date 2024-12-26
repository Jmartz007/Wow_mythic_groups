import { useState, useEffect } from "react";
import Table from "../components/Table";
import useCharacters from "../hooks/useCharacters";

export default function Home() {
  const characterData = useCharacters();

  const identifier = "Character";

  const [tableData, setTableData] = useState(characterData);

  useEffect(() => {
    setTableData(characterData);
  }, [characterData]);

  const deleteRow = async (identifier: string, value: string | number) => {
    try {
      const requestPayload = { [identifier]: value };
      console.log("the identifier is: ", identifier);
      console.log("the id is: ", value);
      console.log(JSON.stringify(requestPayload));

      const response = await fetch(`/groups/api/characters`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestPayload),
      });

      const data = await response.json();
      console.log(data);

      if (!response.ok) {
        throw new Error("failed to delete row");
      }
      setTableData((prevData) =>
        prevData.filter((row) => row[identifier] !== value)
      );
    } catch (error) {
      console.error("error deleting row: ", error);
    }
  };

  return (
    <>
      <div className="rounded border border-1 shadow bg-primary-subtle p-4">
        <h1> Home</h1>

        <Table data={tableData} identifier={identifier} onDelete={deleteRow} />
      </div>
    </>
  );
}
