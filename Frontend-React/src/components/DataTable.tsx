import { useState, useEffect, useMemo } from "react";

import "./Table.css";
import {
  Box,
  Checkbox,
  IconButton,
  Paper,
  styled,
  Table,
  TableBody,
  TableCell,
  tableCellClasses,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { visuallyHidden } from "@mui/utils";
import { Player } from "../types/Player";

interface TableProps {
  selectCheckBox?: boolean;
  data: Array<Record<string, any>>;
  identifier: string;
  onDelete: (row: Record<string, any>) => Promise<void>;
  onRowClick?: (row: Record<string, any>) => void;
}

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

interface EnhancedTableProps {
  numSelected: number;
  onRequestSort: (
    event: React.MouseEvent<unknown>,
    property: keyof Player
  ) => void;
  onSelectAllClick: (event: React.ChangeEvent<HTMLInputElement>) => void;
  order: Order;
  orderBy: keyof Player;
  rowCount: number;
  data: Array<Record<string, any>>;
  selectCheckBox?: boolean;
}

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.primary.light,
    color: theme.palette.text.primary,
    fontSize: 12,
    Padding: theme.spacing(1),
    Margin: theme.spacing(0.5),
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 12,
    Padding: theme.spacing(0.5),
    Margin: theme.spacing(0.5),
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  "&:nth-of-type(odd)": {
    // backgroundColor: theme.palette.background.default,
    Margin: 0.5,
    Padding: 0.5,
  },
  // hide last border
  "&:last-child td, &:last-child th": {
    border: 0,
  },
}));

function EnhancedTableHead(props: EnhancedTableProps) {
  const {
    onSelectAllClick,
    order,
    orderBy,
    numSelected,
    rowCount,
    onRequestSort,
    data,
    selectCheckBox,
  } = props;

  const [columns, setColoumns] = useState<string[]>([]);

  const createSortHandler =
    (property: keyof Player) => (event: React.MouseEvent<unknown>) => {
      onRequestSort(event, property);
    };

  useEffect(() => {
    if (data.length > 0) {
      const cols = [...Object.keys(data[0])];
      cols.push("Actions");
      setColoumns(cols);
    } else {
      setColoumns([]);
    }
  }, [data, selectCheckBox]);

  return (
    <TableHead>
      <StyledTableRow>
        {selectCheckBox && (
          <StyledTableCell sx={{ padding: 0.5 }}>
            <Checkbox
              // color="primary"
              indeterminate={numSelected > 0 && numSelected < rowCount}
              checked={rowCount > 0 && numSelected === rowCount}
              onChange={onSelectAllClick}
              inputProps={{
                "aria-label": "select all options",
              }}
            />
          </StyledTableCell>
        )}
        {columns.map((col) => (
          <StyledTableCell
            key={col}
            align={"center"}
            // padding={"normal"}
            sortDirection={orderBy === col ? order : false}
          >
            <TableSortLabel
              active={orderBy === col}
              direction={orderBy === col ? order : "asc"}
              onClick={createSortHandler(col as keyof Player)}
            >
              {col}
              {orderBy === col ? (
                <Box component="span" sx={visuallyHidden}>
                  {order === "desc" ? "sorted descending" : "sorted ascending"}
                </Box>
              ) : null}
            </TableSortLabel>
          </StyledTableCell>
        ))}
      </StyledTableRow>
    </TableHead>
  );
}

function DataTable({
  data,
  identifier,
  onDelete,
  onRowClick,
  selectCheckBox,
}: TableProps) {
  const [order, setOrder] = useState<Order>("asc");
  const [orderBy, setOrderBy] = useState<keyof Player>("Player");
  const [selected, setSelected] = useState<readonly number[]>([]);

  const clickableColumns = ["Player", "character name"];

  useEffect(() => {
    if (data.length > 0) {
      const initialSelected = data
        .map((row, index) => (row["Is Active"] === 1 ? index : -1))
        .filter((index) => index !== -1);
      setSelected(initialSelected);
    } else {
      setSelected([]);
    }
  }, [data, selectCheckBox]);

  const handleClick = (event: React.MouseEvent<unknown>, id: number) => {
    const selectedIndex = selected.indexOf(id);
    let newSelected: readonly number[] = [];

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, id);
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1)
      );
    }
    setSelected(newSelected);
  };

  const handleRequestSort = (
    event: React.MouseEvent<unknown>,
    property: keyof Player
  ) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleSelectAllClick = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.checked) {
      const newSelected = data.map((n, index) => index);
      setSelected(newSelected);
      return;
    }
    setSelected([]);
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

  // const sortedRows = [...data].sort(getComparator(order, orderBy));

  return (
    <Box>
      <Paper>
        <TableContainer>
          <Table>
            <EnhancedTableHead
              selectCheckBox={selectCheckBox}
              numSelected={selected.length}
              order={order}
              orderBy={orderBy}
              onSelectAllClick={handleSelectAllClick}
              onRequestSort={handleRequestSort}
              rowCount={data.length}
              data={data}
            />

            <TableBody>
              {sortedRows.map((row, index) => {
                const isItemSelected = selected.includes(index);
                const labelId = `enhanced-table-checkbox-${index}`;
                // console.log("sorted row:", row);

                return (
                  <StyledTableRow
                    hover
                    // onClick={(event) => handleClick(event, index)}
                    role="checkbox"
                    aria-checked={isItemSelected}
                    tabIndex={-1}
                    key={index}
                    selected={isItemSelected}
                  >
                    {selectCheckBox && (
                      <StyledTableCell padding="checkbox">
                        <label className="checkbox-label">
                          <Checkbox
                            color="primary"
                            value="is_active"
                            name={row[identifier]}
                            checked={isItemSelected}
                            onClick={(e) => handleClick(e, index)}
                          />
                        </label>
                      </StyledTableCell>
                    )}
                    {Object.keys(row).map((col) => (
                      <StyledTableCell
                        key={`${index}-${col}`}
                        align="center"
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
                      </StyledTableCell>
                    ))}
                    <StyledTableCell>
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

export default DataTable;
