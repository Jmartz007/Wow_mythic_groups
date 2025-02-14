import { useState, useEffect, FormEvent } from "react";
import Table from "../components/DataTable";
import useCharacters from "../hooks/useCharacters";
import { useNavigate } from "react-router-dom";
import { Player } from "../types/Player";
import { Box, Container, Typography } from "@mui/material";
import DataTable from "../components/DataTable";

export default function PlayersList() {
  const characterData = useCharacters();
  const navigate = useNavigate();

  const identifier = "Character";
  const detailsID = "Player";

  const [tableData, setTableData] = useState<Player[]>([]);

  useEffect(() => {
    setTableData(characterData);
  }, [characterData]);

  const rowDelete = async (row: Record<string, any>) => {
    const rowPlayer = row[detailsID];
    const rowCharacter = row[identifier];
    console.log("rowPlayer: ", rowPlayer, " rowCharacter: ", rowCharacter);
    try {
      const response = await fetch(
        `/groups/api/players/${row[detailsID]}/characters/${rowCharacter}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data = await response.json();
      console.log(data);

      if (!response.ok) {
        throw new Error(`failed to delete ${rowPlayer}`);
      }
      setTableData((prevData) =>
        prevData.filter((row) => row[identifier] !== rowCharacter)
      );
    } catch (error) {
      console.error("error deleting row: ", error);
      alert("There was an error deleting the row");
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
        const errorResponse = await response.json();
        console.log(errorResponse);
        const errorMessage = errorResponse.error;
        throw new Error(errorMessage);
      }

      const responseData = await response.json();
      console.log("Form submitted succesffully");
      console.log(responseData);
      navigate("/create-groups", { state: { data: responseData } });
    } catch (error) {
      console.error("error submitting form: ", error);
      if (error instanceof Error) {
        alert(`there was an error submitting form: ${error.message}`);
      } else {
        alert("there was an error submitting form");
      }
    }
  };

  // Sorting function to place tanks and healers up top
  const sortedTableData = [...tableData].sort((a, b) => {
    const rolePriority: Record<string, number> = { Tank: 1, Healer: 2 };
    const aRole = a["Role Type"].find((r) => rolePriority[r]) || "";
    const bRole = b["Role Type"].find((r) => rolePriority[r]) || "";
    return (rolePriority[aRole] || 3) - (rolePriority[bRole] || 3);
  });

  return (
    <Container>
      <Box>
        <Typography variant="h3">Players</Typography>
        <form onSubmit={handleSubmit}>
          <DataTable
            data={sortedTableData}
            identifier={identifier}
            onDelete={rowDelete}
            onRowClick={handleRowClick}
            selectCheckBox={true}
          />
          <button className="col-1 mx-4 btn btn-primary" type="submit">
            Create Groups
          </button>
        </form>
      </Box>
    </Container>
  );
}
