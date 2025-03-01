import { useEffect, useState } from "react";

interface GroupTableProps {
  data: Array<Record<string, any>>;
  onRowClick: (row: Record<string, any>) => void;
}

const columnMapping: Record<string, string> = {
  char_name: "Character Name",
  dpsConf: "DPS Confidence",
  dungeon: "Dungeon",
  hConf: "Healer Confidence",
  is_active: "Active",
  key_level: "Key Level",
  playerName: "Player Name",
  range: "Range",
  role: "Role",
  tConf: "Tank Confidence",
  wow_class: "Class",
};

const columnOrder: string[] = [
  "char_name",
  "playerName",
  "wow_class",
  "role",
  "range",
  "dungeon",
  "key_level",
  "dpsConf",
  "hConf",
  "tConf",
];

export default function GroupTable({ data, onRowClick }: GroupTableProps) {
  const [columns, setColumns] = useState<string[]>([]);
  const clickableColumns = ["Character Name"];

  useEffect(() => {
    setColumns(columnOrder);
  }, []);

  return (
    <div className="container mt-5 table-responsive-lg">
      {Object.entries(data).map(([groupName, groupData]) => (
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
                      {row[col] !== undefined && row[col] !== null
                        ? row[col].toString()
                        : ""}
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
