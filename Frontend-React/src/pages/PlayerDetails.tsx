import { useNavigate, useParams } from "react-router-dom";
import Table from "../components/Table";
import { useEffect, useState } from "react";

function PlayerDetails() {
  const { playername } = useParams<{ playername: string }>();
  const [data, setData] = useState([]);
  const navigate = useNavigate();

  const identifier = "Character";
  const detailsID = "character name";

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

  const onDelete = async (identifier: string, value: any) => {
    try {
      const resourceName = { [identifier]: value };
      const response = await fetch(
        `/groups/api/players/${playername}/characters/${resourceName}`,
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
        prevData.filter((row) => row[identifier] !== value)
      );
    } catch (error) {
      console.error("error deleting row: ", error);
    }
  };

  const handleRowClick = (row: Record<string, any>) => {
    navigate(`/players/${playername}/characters/${row[detailsID]}`);
  };

  return (
    <div className="rounded border border-1 shadow bg-primary-subtle p-4">
      <h1>Player Details</h1>
      <h5>Player Name: {playername}</h5>
      <Table
        data={data}
        identifier={identifier}
        onDelete={onDelete}
        onRowClick={handleRowClick}
      />
    </div>
  );
}

export default PlayerDetails;
