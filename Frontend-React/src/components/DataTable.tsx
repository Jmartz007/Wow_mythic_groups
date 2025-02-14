import { useState, useEffect } from "react";

import "./Table.css";
import {
  Box,
  Button,
  Checkbox,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import { CheckBox } from "@mui/icons-material";
import DeleteIcon from "@mui/icons-material/Delete";

interface TableProps {
  selectCheckBox?: boolean;
  data: Array<Record<string, any>>;
  identifier: string;
  onDelete: (row: Record<string, any>) => Promise<void>;
  onRowClick?: (row: Record<string, any>) => void;
}

function DataTable({
  data,
  identifier,
  onDelete,
  onRowClick,
  selectCheckBox,
}: TableProps) {
  const [columns, setColoumns] = useState<string[]>([]);

  const clickableColumns = ["Player", "character name"];

  useEffect(() => {
    if (data.length > 0) {
      const cols = [...Object.keys(data[0])];
      // if (selectCheckBox) {
      //   cols.unshift("Select");
      // }
      cols.push("Actions");
      setColoumns(cols);
    } else {
      setColoumns([]);
    }
  }, [data, selectCheckBox]);

  const handleDelete = async (row: Record<string, any>) => {
    try {
      await onDelete(row);
    } catch (error) {
      console.error("error deleting row:", error);
    }
  };

  return (
    <Box>
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                {selectCheckBox && (
                  <TableCell padding="checkbox">
                    <CheckBox color="primary"></CheckBox>
                  </TableCell>
                )}
                {columns.map((col, index) => (
                  <TableCell key={col}>{col}</TableCell>
                ))}
              </TableRow>
            </TableHead>

            <TableBody>
              {data.map((row, rowIndex) => (
                <TableRow hover key={rowIndex}>
                  {selectCheckBox && (
                    <TableCell padding="checkbox">
                      <label className="checkbox-label">
                        <Checkbox
                          color="primary"
                          value="is_active"
                          name={row[identifier]}
                          defaultChecked={row["Is Active"] === 1}
                          onClick={(e) => e.stopPropagation()}
                        />
                      </label>
                    </TableCell>
                  )}
                  {Object.keys(row).map((col) => (
                    <TableCell
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
                    </TableCell>
                  ))}
                  <TableCell>
                    <IconButton
                      color="error"
                      onClick={(e) => {
                        e.stopPropagation();
                        console.log("row is: ", row);
                        console.log("row.identifier is", row[identifier]);
                        handleDelete(row);
                      }}
                    >
                      <DeleteIcon fontSize="inherit" />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
}

export default DataTable;
