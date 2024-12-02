import { useState, useEffect } from "react";

interface TableProps {
  data: Array<Record<string, any>>;
  identifier: string;
  onDelete: (identifier: string, value: any) => Promise<void>;
}

function Table({ data, identifier, onDelete }: TableProps) {
  const [columns, setColoumns] = useState<string[]>([]);
  //   const [tableData, setTableData] = useState(data);

  console.log("the identifier is: ", identifier)

  useEffect(() => {
    if (data.length > 0) {
      setColoumns([...Object.keys(data[0]), "Actions"]);
    } else {
      setColoumns([]);
    }
  }, [data]);

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
            <tr key={rowIndex}>
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
                  onClick={() => {
                    console.log("row is: ", row)
                    console.log("row.identifier is", row[identifier])
                    handleDelete(identifier, row[identifier])}
                  }
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
