import React, { useState, useEffect } from "react";
import Table from "../components/Table";

export default function EditDungeons() {
  const url = `/groups/api/dungeons`;
  const [tableData, setTableData] = useState<Array<Record<string, any>>>([]);

  const identifier = "dungeon";

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

      const response = await fetch(`/groups/api/dungeons`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestPayload),
      });
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
          {/* <div id="Dungeons List" className="grid column-gap-2"> */}
          <label htmlFor="newdungeon" className="col-2 mx-4">
            Enter New Dungeon
          </label>
          <input
            className="p-2 col-4"
            type="text"
            id="newdungeon"
            name="newdungeon"
            pattern="[a-z ':A-Z]+"
          />
          <button className="col-1 mx-4 btn btn-primary" type="submit">
            Add
          </button>
          {/* </div> */}
        </form>
      </div>
    </>
  );
}
