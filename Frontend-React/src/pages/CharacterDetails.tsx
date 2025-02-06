import { useParams } from "react-router-dom";
import Table from "../components/Table";
import { useEffect, useState } from "react";

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
    <div className="rounded border border-1 shadow bg-primary-subtle p-4">
      <h1>Character Details</h1>
      <p>Character Name: {charactername}</p>
      <Table data={data} identifier={identifier} onDelete={onDelete} />
    </div>
  );
}

export default CharacterDetails;
