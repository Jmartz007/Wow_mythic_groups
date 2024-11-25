import React, { useState } from "react";

interface TableProps {
  data: Array<Record<string, any>>;
}

function Table({ data }: TableProps) {
  const [columns, setColoumns] = useState<string[]>([]);
  React.useEffect(() => {
    if (data.length > 0) {
      setColoumns(Object.keys(data[0]));
    } else {
      setColoumns([]);
    }
  }, [data]);

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
