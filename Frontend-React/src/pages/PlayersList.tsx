import { useState, useEffect, FormEvent } from "react";
import Table from "../components/Table";
import useCharacters from "../hooks/useCharacters";
import { Navigate, NavLink, useNavigate } from "react-router-dom";

export default function PlayersList() {
  const characterData = useCharacters();
  const [formData, setFormData] = useState<Record<string, any>>({});
  const navigate = useNavigate();

  const identifier = "Character";
  const detailsID = "Player";

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

  const handleRowClick = (row: Record<string, any>) => {
    navigate(`/players/${row[detailsID]}`);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const formData = new FormData(e.currentTarget);
      const jsonData = Object.fromEntries(formData.entries());

      const response = await fetch("/groups/api/create-groups", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData),
      });

      console.log(JSON.stringify(jsonData));

      if (!response.ok) {
        throw new Error("network response error");
      }

      console.log("Form submitted succesffully");
      navigate("/create-groups");
    } catch (error) {
      console.error("error submitting form: ", error);
      alert(`there was an error submitting form: ${error}`);
    }
  };

  return (
    <>
      <div className="rounded border border-1 shadow bg-primary-subtle p-4">
        <h1>Players</h1>
        <form onSubmit={handleSubmit}>
          <Table
            data={tableData}
            identifier={identifier}
            onDelete={deleteRow}
            onRowClick={handleRowClick}
            selectCheckBox={true}
          />
          <button className="col-1 mx-4 btn btn-primary" type="submit">
            Create Groups
          </button>
        </form>
      </div>
    </>
  );
}
