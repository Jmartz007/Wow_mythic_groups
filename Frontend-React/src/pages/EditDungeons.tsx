import React, { useState, useEffect } from "react";
import Table from "../components/Table";
// import React from "react";

export default function EditDungeons() {
  const url = "http://localhost:5000/groups/api/dungeons";
  const [tableData, setTableData] = useState<Array<Record<string, any>>>([]);

  const identifier = "dungeon";

  const fetchTableData = async () => {
    try {
      const response = await fetch(url);
      const data = await response.json();
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
        console.log("data sent");
        await fetchTableData();
        (event.target as HTMLFormElement).reset();
      } else {
        console.error("failed to add dungeon");
      }
    } catch (error) {
      console.error("error submitting form", error);
    }
  };

  const deleteRow = async (identifier: string, value: string | number) => {
    try {
      const requestPayload = { [identifier]: value };
      console.log("the identifier is: ", identifier);
      console.log("the id is: ", value);

      const response = await fetch(
        `http://localhost:5000/groups/api/dungeons`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestPayload),
        }
      );
      const data = await response.json();
      console.log(data);

      if (!response.ok) {
        throw new Error("failed to delete dungeon");
      }
      setTableData((prevData) =>
        prevData.filter((row) => row[identifier] !== value)
      );
    } catch (error) {
      console.error("error deleting row: ", error);
    }
  };

  useEffect(() => {
    fetchTableData();
  }, []);

  return (
    <>
      <div className="container rounded border border-1 shadow bg-primary-subtle p-4">
        <h3>Edit Dungeons</h3>
        <form onSubmit={handleFormSubmit}>
          <div id="Dungeons List" className="grid column-gap-4">
            <label htmlFor="newdungeon" className="col-2">
              Enter New Dungeon
            </label>
            <input
              className="p-2 col-4"
              type="text"
              id="newdungeon"
              name="newdungeon"
              pattern="[a-z ':A-Z]+"
            />
            <button className="col-1 btn btn-primary" type="submit">
              Add
            </button>
          </div>
        </form>
        <h1 className="title">Current Dungeons</h1>
        <Table
          data={tableData}
          identifier={identifier}
          onDelete={deleteRow}
        ></Table>
      </div>
    </>
  );
}
