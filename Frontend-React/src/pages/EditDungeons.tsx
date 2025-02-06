import React, { useState, useEffect } from "react";
import Table from "../components/Table";

export default function EditDungeons() {
  const [tableData, setTableData] = useState<Array<Record<string, any>>>([]);

  const identifier = "dungeon";
  const url = `/groups/api/dungeons`;

  useEffect(() => {
    fetchTableData();
  }, []);

  const fetchTableData = async () => {
    try {
      const response = await fetch(url, {
        headers: { "Cache-Control": "no-cache" },
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error("failed to fetch data");
      }

      setTableData(data); // Update table data
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleFormSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const formData = new FormData(event.target as HTMLFormElement);

    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        console.log("dungeon added successfully");
        await fetchTableData();
        (event.target as HTMLFormElement).reset();
      } else {
        const data = await response.json();
        console.error(`failed to add dungeon ${data.error.message}`);
        throw new Error(data.error.message);
      }
    } catch (error) {
      alert(`${error}`);
    }
  };

  const deleteRow = async (row: Record<string, any>) => {
    const dungeonRow = row[identifier];
    console.log("row to be deleted: ", dungeonRow);
    try {
      const response = await fetch(`/groups/api/dungeons/${dungeonRow}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`failed to delete dungeon ${errorData.error.details}`);
      }

      const data = await response.json();
      console.log(data);

      setTableData((prevData) =>
        prevData.filter((row) => row[identifier] !== dungeonRow)
      );
    } catch (error) {
      if (error instanceof Error) {
        console.error("error deleting row: ", error);
        alert(`Error: ${error.message}`);
      } else {
        console.error("unknown error deleting row: ", error);
        alert("An unknown error occurred");
      }
    }
  };

  return (
    <>
      <div className="container rounded border border-1 shadow bg-primary-subtle p-4">
        <h1>Dungeons</h1>
        <h3 className="title">Current Dungeons</h3>
        <Table
          data={tableData}
          identifier={identifier}
          onDelete={deleteRow}
        ></Table>
        <h3>Add Dungeon:</h3>
        <form onSubmit={handleFormSubmit}>
          <label htmlFor="Dungeon" className="col-2 mx-4">
            Enter New Dungeon
          </label>
          <input
            className="p-2 col-4"
            type="text"
            id="Dungeon"
            name="Dungeon"
            pattern="[a-z ':A-Z]+"
          />
          <button className="col-1 mx-4 btn btn-primary" type="submit">
            Add
          </button>
        </form>
      </div>
    </>
  );
}
