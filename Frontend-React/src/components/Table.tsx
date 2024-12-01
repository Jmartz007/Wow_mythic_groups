import { useState, useEffect } from "react";

interface TableProps {
  data: Array<Record<string, any>>;
  onDelete: (id: any) => Promise<void>;
}

function Table({ data, onDelete }: TableProps) {
  const [columns, setColoumns] = useState<string[]>([]);
  //   const [tableData, setTableData] = useState(data);

  useEffect(() => {
    if (data.length > 0) {
      setColoumns([...Object.keys(data[0]), "Actions"]);
    } else {
      setColoumns([]);
    }
  }, [data]);

  const handleDelete = async (rowId: any) => {
    try {
      await onDelete(rowId);
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
                  onClick={() => handleDelete(row.id)}
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
