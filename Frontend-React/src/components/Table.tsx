import { useState, useEffect } from "react";

interface TableProps {
  selectCheckBox?: boolean;
  data: Array<Record<string, any>>;
  identifier: string;
  onDelete: (identifier: string, value: any) => Promise<void>;
  onRowClick?: (row: Record<string, any>) => void;
}

function Table({
  data,
  identifier,
  onDelete,
  onRowClick,
  selectCheckBox,
}: TableProps) {
  const [columns, setColoumns] = useState<string[]>([]);

  console.log("the identifier is: ", identifier);

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

  const handleDelete = async (identifier: string, value: any) => {
    try {
      await onDelete(identifier, value);
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
            <tr key={rowIndex} onClick={() => onRowClick && onRowClick(row)}>
              {selectCheckBox && (
                <td>
                  <input
                    type="checkbox"
                    value="is_active"
                    name={row[identifier]}
                    onClick={(e) => e.stopPropagation()}
                  />
                </td>
              )}
              {Object.keys(row).map((col) => (
                <td key={`${rowIndex}-${col}`}>
                  {row[col] !== undefined && row[col] !== null
                    ? row[col].toString()
                    : ""}
                </td>
              ))}
              <td>
                <button
                  className="btn btn-danger btn-sm"
                  onClick={(e) => {
                    e.stopPropagation(); // Prevent row click
                    console.log("row is: ", row);
                    console.log("row.identifier is", row[identifier]);
                    handleDelete(identifier, row[identifier]);
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
