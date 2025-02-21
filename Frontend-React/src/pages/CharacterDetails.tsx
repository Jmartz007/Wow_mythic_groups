import { useParams } from "react-router-dom";
import Table from "../components/DataTable";
import { useEffect, useState } from "react";
import { Container } from "react-bootstrap";
import { Box, Typography } from "@mui/material";

// TODO: Need to implement function to edit the character data
function CharacterDetails() {
  const { charactername, playername } = useParams<{
    charactername: string;
    playername: string;
  }>();

  const [data, setData] = useState([]);
  const identifier = "character_name";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `/groups/api/players/${playername}/characters/${charactername}`
        );
        const data = await response.json();
        setData(data);
      } catch (error) {
        console.error("error fetching data: ", error);
      }
    };
    fetchData();
  }, [charactername]);

  const onDelete = async (row: Record<string, any>) => {
    const rowCharacter = row[identifier];
    console.log("item to be deleted: ", rowCharacter);

    try {
      const response = await fetch(
        `/groups/api/players/${playername}/characters/${rowCharacter}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error("failed to delete row");
      }

      setData((prevData) =>
        prevData.filter((row) => row[identifier] !== rowCharacter)
      );
    } catch (error) {}
  };

  return (
    <Container>
      <Box paddingBottom={12}>
        <Box
          display="flex"
          flexDirection="column"
          justifyContent="start"
          alignContent="space-between"
          margin={4}
          gap={2}
        >
          <Typography variant="h3">Player Details</Typography>
          <Typography variant="h6">Player Name: {charactername}</Typography>
        </Box>
        <Table data={data} identifier={identifier} onDelete={onDelete} />
      </Box>
    </Container>
  );
}

export default CharacterDetails;
