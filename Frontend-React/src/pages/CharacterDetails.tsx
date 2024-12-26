import { useParams } from "react-router-dom";
import Table from "../components/Table";
import { useEffect, useState } from "react";

function CharacterDetails() {
  const { charactername, playername } = useParams<{
    charactername: string;
    playername: string;
  }>();

  const [data, setData] = useState([]);
  const identifier = "Character";

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

  const onDelete = async (identifier: string, value: any) => {
    try {
      const response = await fetch(
        `/groups/api/players/${playername}/characters/${charactername}`,
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

  return (
    <div className="rounded border border-1 shadow bg-primary-subtle p-4">
      <h1>Player Details</h1>
      <p>Player Name: {charactername}</p>
      <Table data={data} identifier={identifier} onDelete={onDelete} />
    </div>
  );
}

export default CharacterDetails;
