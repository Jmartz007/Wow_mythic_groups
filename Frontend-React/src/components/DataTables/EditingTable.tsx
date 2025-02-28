import { useCallback, useEffect, useMemo, useState } from "react";

import DeleteIcon from "@mui/icons-material/Delete";
import {
  Box,
  CircularProgress,
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
  TextField,
} from "@mui/material";
import { Player, PlayerKey, PlayerValue } from "../../types/Player";
import EnhancedTableHead from "./EnhancedTableHead";
import "./Table.css";
import { StyledTableCell, StyledTableRow } from "./StyledTableItems";
import debounce from "../../hooks/debounce";

interface TableProps {
  data: Player[];
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
  orderBy: PlayerKey
): (a: Record<string, any>, b: Record<string, any>) => number {
  return order === "desc"
    ? (a, b) => descendingComparator(a, b, orderBy as string)
    : (a, b) => -descendingComparator(a, b, orderBy as string);
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
  const [options, setOptions] = useState<Option[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchDungeonOptions = async () => {
    try {
      const response = await fetch("/groups/api/dungeons");

      if (!response.ok) {
        throw new Error("Failed to fetch dungeons");
      }
      const data: Option[] = await response.json();
      setOptions(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
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

  const updateDungeon = async (
    playerID: string,
    characterID: string,
    property: string,
    value: string
  ): Promise<Response> => {
    const body = { [property]: value };
    const response = await fetch(
      `/groups/api/players/${playerID}/characters/${characterID}`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    );
    return response;
  };

  const debouncedUpdateDungeon = useCallback(
    debounce(
      async (
        playerID: string,
        characterID: string,
        property: string,
        value: string
      ): Promise<Response> => {
        const response = await updateDungeon(
          playerID,
          characterID,
          property,
          value
        );
        return response;
      },
      750
    ),
    []
  );

  const handleDungeonChange = async (
    property: PlayerKey,
    value: PlayerValue,
    rowIndex: number,
    row: Record<string, any>
  ) => {
    const playerID = row.Player;
    const characterID = row.Character;
    console.log(`rowindex: ${rowIndex}`);
    console.log(`updating: ${playerID} ${characterID} with ${value}`);

    const oldData: Player[] = [...data];
    console.log("old data");
    console.log(oldData);

    setData((prevData) => {
      const newData = [...prevData];
      // console.log(newData);
      const rowToUpdate = newData.find((r) => r.Character === characterID);
      if (rowToUpdate) {
        rowToUpdate[property] = value;
      }
      // console.log(`newdata: ${newData[rowIndex]}`);
      // console.log(newData[rowIndex])
      // newData[rowIndex] = { ...newData[rowIndex], Dungeon: value };
      // console.log(rowToUpdate);
      // console.log(newData);
      return newData;
    });
    try {
      const response: Response = await debouncedUpdateDungeon(
        playerID,
        characterID,
        property as string,
        value as string
      );

      console.log("response: ");
      console.log(response);

      if (!response.ok) {
        throw new Error("failed to update key");
      }
    } catch (error) {
      console.error("failed to update dungeon", error);
      console.log("reverting to old data");
      console.log(oldData);
      setData(oldData);
    }
  };

  const renderCellContent = (
    col: string,
    row: Record<string, any>,
    rowIndex: number
  ) => {
    // console.log(`col: ${col}, value: ${row[col]} rowIndex: ${rowIndex}`);
    if (row[col] === undefined || row[col] === null) {
      return "";
    }
    if (editingColumns.includes(col)) {
      if (col === "Key Level") {
        return (
          <TextField
            // className="row"
            type="number"
            name={col}
            id={row.Player}
            label="Key Level"
            size="small"
            value={row[col]}
            onChange={(e) => {
              handleDungeonChange("Key Level", e.target.value, rowIndex, row);
            }}
            sx={{ maxWidth: 120 }}
          />
        );
      }
      if (col === "Dungeon") {
        return (
          <FormControl sx={{ minWidth: 120, maxWidth: 400, flexShrink: 1 }}>
            <InputLabel id={`${col}-label`}>{col}</InputLabel>
            <Select
              name={col}
              id={row.Player}
              labelId={`${col}-label`}
              size="small"
              variant="filled"
              value={row[col]}
              onChange={(e) =>
                handleDungeonChange("Dungeon", e.target.value, rowIndex, row)
              }
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

  if (loading) {
    return <CircularProgress />;
  }

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
                // console.log(`rendering row: ${index}`);
                // console.log(row);
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
