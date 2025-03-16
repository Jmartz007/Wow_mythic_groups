import { useEffect, useState } from "react";
import { Player } from "../../types/Player";
import { Link } from "@mui/material";

interface Group {
  [playerKey: string]: Player;
}

interface GroupedPlayers {
  [groupId: string]: Group;
}

interface GroupTableProps {
  data: GroupedPlayers;
  onRowClick: (row: Record<string, any>) => void;
}

const columnMapping: Record<string, string> = {
  char_name: "Character Name",
  dpsConf: "DPS Skill",
  dungeon: "Dungeon",
  hConf: "Healer Skill",
  is_active: "Active",
  key_level: "Key Level",
  playerName: "Player Name",
  range: "Range",
  role: "Role",
  tConf: "Tank Skill",
  wow_class: "Class",
  iLvl: "iLvl",
  "Highest Key": "Highest Key",
  profileUrl: "Profile",
};

const columnOrder: string[] = [
  "char_name",
  "iLvl",
  "Highest Key",
  "playerName",
  "wow_class",
  "role",
  "range",
  "dungeon",
  "key_level",
  "dpsConf",
  "hConf",
  "tConf",
  "profileUrl",
];

function renderCellContent(value: any): React.ReactNode {
  if (value === null || value === undefined) {
    return "";
  } else if (typeof value == "string" && value.includes("https://")) {
    return (
      <Link href={value} target="_blank">
        {value}
      </Link>
    );
  }
  return value.toString();
}

async function fetchRaiderIo(char_name: string) {
  const baseUrl = "https://raider.io/api/v1/characters/profile";
  const params = new URLSearchParams({
    region: "us",
    realm: "lightbringer",
    name: char_name,
    fields: "gear,mythic_plus_highest_level_runs",
  });
  try {
    const response = await fetch(`${baseUrl}?${params.toString()}`);

    if (!response.ok) {
      console.error(`Failed to fetch data for ${char_name}`);
      throw new Error(
        `Failed to fetch data for ${char_name}: ${response.statusText}`
      );
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

export default function GroupTable({ data, onRowClick }: GroupTableProps) {
  const [columns, setColumns] = useState<string[]>([]);
  const [enrichedData, setEnrichedData] = useState(data);
  const [loading, setLoading] = useState(true);
  const clickableColumns = ["Character Name"];

  useEffect(() => {
    async function fetchAdditionalData() {
      const newData = { ...data };

      const fetchPromises: Promise<void>[] = [];

      for (const [groupName, groupData] of Object.entries(newData)) {
        for (const [charKey, row] of Object.entries(groupData)) {
          const promise = fetchRaiderIo(String(row.char_name)).then(
            (apiData) => {
              if (apiData) {
                const { gear, profile_url, mythic_plus_highest_level_runs } =
                  apiData;
                const { item_level_equipped } = gear;
                let highestKey = "";

                if (
                  mythic_plus_highest_level_runs &&
                  mythic_plus_highest_level_runs.length > 0
                ) {
                  const { mythic_level, short_name } =
                    mythic_plus_highest_level_runs[0];
                  highestKey = `${short_name} ${mythic_level}`;
                }

                newData[groupName][charKey] = {
                  ...row,
                  profileUrl: profile_url,
                  iLvl: item_level_equipped,
                  "Highest Key": highestKey,
                };
              }
            }
          );
          fetchPromises.push(promise);
        }
      }

      await Promise.all(fetchPromises);
      setEnrichedData(newData);
      setLoading(false);
    }

    fetchAdditionalData();
  }, [data]);

  useEffect(() => {
    setColumns(columnOrder);
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mt-5 table-responsive-lg">
      {Object.entries(enrichedData).map(([groupName, groupData]) => (
        <div key={groupName}>
          <h2>Group {groupName}</h2>

          <table className="table table-striped table-hover ">
            <thead className="table-dark">
              <tr>
                {columns.map((col) => (
                  <th key={col}>{columnMapping[col]}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {Object.values(groupData).map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {columns.map((col) => (
                    <td
                      key={`${rowIndex}-${col}`}
                      onClick={
                        clickableColumns.includes(col)
                          ? () => onRowClick && onRowClick(row)
                          : undefined
                      }
                      className={
                        clickableColumns.includes(col) ? "clickable-cell" : ""
                      }
                    >
                      {renderCellContent(row[col])}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}
