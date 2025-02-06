import { useState, useEffect } from "react";

import "./Table.css";

interface TableProps {
  selectCheckBox?: boolean;
  data: Array<Record<string, any>>;
  identifier: string;
  // detailsID?: string;
  // onDelete: (identifier: keyof Player, value: string | number, detailsID?:string) => Promise<void>;
  onDelete: (row: Record<string, any>) => Promise<void>;
  onRowClick?: (row: Record<string, any>) => void;
}

function Table({
  data,
  identifier,
  // detailsID,
  onDelete,
  onRowClick,
  selectCheckBox,
}: TableProps) {
  const [columns, setColoumns] = useState<string[]>([]);

  const clickableColumns = ["Player", "character name"];

  // console.log("the identifier is: ", identifier);

  useEffect(() => {
    if (data.length > 0) {
      const cols = [...Object.keys(data[0])];
      if (selectCheckBox) {
        cols.unshift("Select");
      }
      cols.push("Actions");
      setColoumns(cols);
    } else {
      setColoumns([]);
    }
  }, [data, selectCheckBox]);

  const handleDelete = async (row: Record<string, any>) => {
    try {
      // await onDelete(identifier, value, detailsID);
      await onDelete(row);
    } catch (error) {
      console.error("error deleting row:", error);
    }
  };

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
              {selectCheckBox && (
                <td>
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      value="is_active"
                      name={row[identifier]}
                      defaultChecked={row["Is Active"] === 1}
                      onClick={(e) => e.stopPropagation()}
                    />
                  </label>
                </td>
              )}
              {Object.keys(row).map((col) => (
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
              <td>
                <button
                  type="button"
                  className="btn btn-danger btn-sm"
                  onClick={(e) => {
                    e.stopPropagation(); // Prevent row click
                    console.log("row is: ", row);
                    console.log("row.identifier is", row[identifier]);
                    handleDelete(row);
                  }}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Table;
