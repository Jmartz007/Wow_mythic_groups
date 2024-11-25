import React, { useEffect, useState } from "react";

interface TableProps {
  url: string;
  //   items: string[];
}
// PlayerName: string;
// CharacterName: string;
// Class: string;
// "DPS Skill"?: number;
// "Healer Skill"?: number;
// Dungeon: string;
// "Key Level": number;
// Range: string;
// Role: string[];
// "Skill Level": number;
// is_active: number;

function Table({ url }: TableProps) {
  const [data, setData] = useState<Array<Record<string, any>>>([]);
  const [columns, setColoumns] = useState<string[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const jsonData: Array<Record<string, any>> = await response.json();

        setData(jsonData);

        if (jsonData.length > 0) {
          setColoumns(Object.keys(jsonData[0]));
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="container mt-5 table-responsive-lg">
      <table className="table table-striped table-hover ">
        <thead className="table-dark">
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((col) => (
                <td key={`${rowIndex}-${col}`}>
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
  );
}

export default Table;
