import { useNavigate, useParams } from "react-router-dom";
import Table from "../components/DataTable";
import { useEffect, useState } from "react";
import { Box, Container, Typography } from "@mui/material";

function PlayerDetails() {
  const { playername } = useParams<{ playername: string }>();
  const [data, setData] = useState([]);
  const navigate = useNavigate();

  const identifier = "character name";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `/groups/api/players/${playername}/characters`
        );
        const data = await response.json();
        setData(data);
      } catch (error) {
        console.error("error fetching data: ", error);
      }
    };
    fetchData();
  }, [playername]);

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

  const handleRowClick = (row: Record<string, any>) => {
    navigate(`/players/${playername}/characters/${row[identifier]}`);
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
          <Typography variant="h6">Player Name: {playername}</Typography>
        </Box>
        <Table
          data={data}
          identifier={identifier}
          onDelete={onDelete}
          onRowClick={handleRowClick}
        />
      </Box>
    </Container>
  );
}

export default PlayerDetails;
