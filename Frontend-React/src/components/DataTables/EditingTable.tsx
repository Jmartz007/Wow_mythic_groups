import { useEffect, useMemo, useState } from "react";

import DeleteIcon from "@mui/icons-material/Delete";
import {
  Alert,
  Box,
  FormControl,
  IconButton,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  SelectChangeEvent,
  Table,
  TableBody,
  TableContainer,
} from "@mui/material";
import { Player } from "../../types/Player";
import EnhancedTableHead from "./EnhancedTableHead";
import "./Table.css";
import { StyledTableCell, StyledTableRow } from "./StyledTableItems";

interface TableProps {
  data: Array<Record<string, any>>;
  setData: React.Dispatch<React.SetStateAction<Player[]>>;
  editingColumns: Array<string>;
  onDelete: (row: Record<string, any>) => Promise<void>;
  columnOrder?: string[];
}

type Option = {
  id: number;
  dungeon: string;
};

function descendingComparator<T>(a: T, b: T, orderBy: keyof T) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

type Order = "asc" | "desc";

function getComparator(
  order: Order,
  orderBy: string
): (a: Record<string, any>, b: Record<string, any>) => number {
  return order === "desc"
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function EditingTable({
  data,
  setData,
  editingColumns,
  onDelete,
  columnOrder,
}: TableProps) {
  const [order, setOrder] = useState<Order>("asc");
  const [orderBy, setOrderBy] = useState<keyof Player>("Player");
  // const [selected, setSelected] = useState<readonly number[]>([]);
  const [options, setOptions] = useState<Option[]>([]);

  // useEffect(() => {
  //   if (data.length > 0) {
  //     const initialSelected = data
  //       .map((row, index) => (row["Is Active"] === 1 ? index : -1))
  //       .filter((index) => index !== -1);
  //     setSelected(initialSelected);
  //   } else {
  //     setSelected([]);
  //   }
  // }, [data]);

  useEffect(() => {
    const fetchDungeonOptions = async () => {
      try {
        const response = await fetch("/groups/api/dungeons");

        if (!response.ok) {
          throw new Error("Failed to fetch options");
        }
        const data: Option[] = await response.json();
        setOptions(data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchDungeonOptions();
  }, []);

  const handleRequestSort = (property: keyof Player) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleDelete = async (row: Record<string, any>) => {
    try {
      await onDelete(row);
    } catch (error) {
      console.error("error deleting row:", error);
    }
  };

  const sortedRows = useMemo(
    () => [...data].sort(getComparator(order, orderBy)),
    [order, orderBy, data]
  );

  const handleDungeonChange = (
    e: SelectChangeEvent<string>,
    rowIndex: number
  ) => {
    const { value } = e.target;
    const playerID = data[rowIndex]["Player"];
    const characterID = data[rowIndex]["Character"];
    const updateDungeon = async () => {
      try {
        const response = await fetch(
          `/groups/api/players/${playerID}/characters/${characterID}`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ Dungeon: value }),
          }
        );
        const resp = await response.text();
        console.log("response: ", resp);
        if (!response.ok) {
          throw new Error("Failed to update character");
        }
        setData((prevData) => {
          const newData = [...prevData];
          newData[rowIndex] = { ...newData[rowIndex], Dungeon: value };
          return newData;
          // prevData.map((row, index) =>
          //   index === rowIndex ? { ...row, Dungeon: value } : row
        });
      } catch (error) {
        console.error(error);
        alert("failed to update character");
      }
    };
    updateDungeon();
  };

  const renderCellContent = (
    col: string,
    row: Record<string, any>,
    rowIndex: number
  ) => {
    // console.log(`col: ${col}, row: ${row}, rowIndex: ${rowIndex}`);
    // console.log(`row at col ${col}: ${row[col]}`);
    if (row[col] === undefined || row[col] === null) {
      return "";
    }
    if (editingColumns.includes(col)) {
      if (typeof row === "number") {
        return "editing number";
      }
      if (col === "Dungeon") {
        return (
          <FormControl sx={{ minWidth: 120, maxWidth: 400, flexShrink: 1 }}>
            <InputLabel id={`${col}-label`}>{col}</InputLabel>
            <Select
              name={col}
              id={col}
              labelId={`${col}-label`}
              size="small"
              variant="filled"
              value={data[rowIndex]["Dungeon"]}
              onChange={(e) => handleDungeonChange(e, rowIndex)}
            >
              {options.map((option) => (
                <MenuItem key={option.id} value={option.dungeon}>
                  {option.dungeon}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        );
      }
      return "Editing Content";
    }
    return row[col].toString();
  };

  return (
    <Box>
      <Paper>
        <TableContainer>
          <Table>
            <EnhancedTableHead
              order={order}
              orderBy={orderBy}
              onRequestSort={handleRequestSort}
              rowCount={data.length}
              data={data}
              columnOrder={columnOrder}
            />

            <TableBody>
              {sortedRows.map((row, index) => {
                const columnsToDisplay = columnOrder || Object.keys(row);
                console.log("rendering table");
                return (
                  <StyledTableRow
                    hover
                    role="checkbox"
                    tabIndex={-1}
                    key={index}
                  >
                    {columnsToDisplay.map((col) => (
                      <StyledTableCell key={`${index}-${col}`} align="center">
                        {renderCellContent(col, row, index)}
                      </StyledTableCell>
                    ))}
                    <StyledTableCell align="center">
                      <IconButton
                        color="error"
                        onClick={(e) => {
                          e.stopPropagation();
                          console.log("row is: ", row);
                          handleDelete(row);
                        }}
                      >
                        <DeleteIcon fontSize="inherit" />
                      </IconButton>
                    </StyledTableCell>
                  </StyledTableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
}

export default EditingTable;
