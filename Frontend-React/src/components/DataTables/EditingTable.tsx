import { useEffect, useMemo, useState } from "react";

import DeleteIcon from "@mui/icons-material/Delete";
import {
  Box,
  Checkbox,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableContainer,
} from "@mui/material";
import { Player } from "../../types/Player";
import EnhancedTableHead from "./EnhancedTableHead";
import "./Table.css";
import { StyledTableCell, StyledTableRow } from "./TableStyles";

interface TableProps {
  selectCheckBox?: boolean;
  data: Array<Record<string, any>>;
  identifier: string;
  onDelete: (row: Record<string, any>) => Promise<void>;
  onRowClick?: (row: Record<string, any>) => void;
  columnOrder?: string[];
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

function EditingTable({
  data,
  identifier,
  onDelete,
  onRowClick,
  selectCheckBox,
  columnOrder,
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

  const handleClick = (id: number) => {
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

  const handleRequestSort = (property: keyof Player) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleSelectAllClick = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.checked) {
      const newSelected = data.map((_, index) => index);
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
              columnOrder={columnOrder}
            />

            <TableBody>
              {sortedRows.map((row, index) => {
                const isItemSelected = selected.includes(index);
                const columnsToDisplay = columnOrder || Object.keys(row);

                return (
                  <StyledTableRow
                    hover
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
                            onClick={() => handleClick(index)}
                          />
                        </label>
                      </StyledTableCell>
                    )}
                    {columnsToDisplay.map((col) => (
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
                    <StyledTableCell align="center">
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

export default EditingTable;
