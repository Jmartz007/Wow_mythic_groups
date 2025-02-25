import { useState, useEffect, FormEvent } from "react";
import useCharacters from "../hooks/useCharacters";
import { useNavigate } from "react-router-dom";
import { Player } from "../types/Player";
import { Box, Container, Typography } from "@mui/material";
import EditingTable from "../components/DataTables/EditingTable";

export default function EditKeys() {
  const characterData = useCharacters();
  const navigate = useNavigate();

  const identifier = "Character";
  const detailsID = "Player";

  const [tableData, setTableData] = useState<Player[]>([]);

  const columnOrder: string[] = [
    "Character",
    "Class",
    "Player",
    "Dungeon",
    "Key Level",
  ];

  useEffect(() => {
    setTableData(characterData);
    console.log("editing keys");
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

  return (
    <Container>
      <Box paddingBottom={12}>
        <Box
          display="flex"
          flexDirection="row"
          justifyContent="start"
          sx={{ padding: 2, margin: 2 }}
        >
          <Typography variant="h3">Edit Keys</Typography>
        </Box>
        <form onSubmit={handleSubmit}>
          <Box
            display="flex"
            flexDirection="column"
            alignContent="space-between"
          >
            <EditingTable
              data={tableData}
              identifier={identifier}
              onDelete={rowDelete}
              selectCheckBox={true}
              columnOrder={columnOrder}
            />
          </Box>
        </form>
      </Box>
    </Container>
  );
}
