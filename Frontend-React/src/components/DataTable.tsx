import { useState, useEffect } from "react";

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
import { CheckBox, Margin, Padding } from "@mui/icons-material";
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

interface HeadCell {
  disablePadding: boolean;
  id: keyof Player;
  label: string;
  numeric: boolean;
}
type Order = "asc" | "desc";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.primary.light,
    color: theme.palette.text.primary,
    fontSize: 12,
    Padding: 0.5,
    Margin: 0.5,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 12,
    Padding: 0.5,
    Margin: 0.5,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  "&:nth-of-type(odd)": {
    backgroundColor: theme.palette.action.selected,
    Margin: 0.5,
    Padding: 0.5,
  },
  // hide last border
  "&:last-child td, &:last-child th": {
    border: 0,
  },
}));

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
  data: Player[];
  selectCheckBox?: boolean;
}

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
          <StyledTableCell>
            <Checkbox
              color="primary"
              indeterminate={numSelected > 0 && numSelected < rowCount}
              checked={rowCount > 0 && numSelected === rowCount}
              onChange={onSelectAllClick}
              inputProps={{
                "aria-label": "select all options",
              }}
            />
          </StyledTableCell>
        )}
        {columns.map((headCell) => (
          <TableCell
            key={headCell}
            align={headCell ? "right" : "left"}
            padding={headCell ? "none" : "normal"}
            sortDirection={orderBy === headCell ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell}
              direction={orderBy === headCell ? order : "asc"}
              onClick={createSortHandler(headCell as keyof Player)}
            >
              {headCell}
              {orderBy === headCell ? (
                <Box component="span" sx={visuallyHidden}>
                  {order === "desc" ? "sorted descending" : "sorted ascending"}
                </Box>
              ) : null}
            </TableSortLabel>
          </TableCell>
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
  const [columns, setColoumns] = useState<string[]>([]);

  const clickableColumns = ["Player", "character name"];

  useEffect(() => {
    if (data.length > 0) {
      const cols = [...Object.keys(data[0])];
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
              <StyledTableRow>
                {selectCheckBox && (
                  <StyledTableCell padding="checkbox">
                    <label className="checkbox-label">
                      <CheckBox color="secondary" sx={{ marginLeft: 1 }} />
                    </label>
                  </StyledTableCell>
                )}
                {columns.map((col, index) => (
                  <StyledTableCell key={col}>
                    <TableSortLabel>{col}</TableSortLabel>
                  </StyledTableCell>
                ))}
              </StyledTableRow>
            </TableHead>

            <TableBody>
              {data.map((row, rowIndex) => (
                <StyledTableRow hover key={rowIndex}>
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
                    <StyledTableCell
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
                    </StyledTableCell>
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
                </StyledTableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
}

export default DataTable;
