import { Box, Checkbox, TableHead, TableSortLabel } from "@mui/material";
import { visuallyHidden } from "@mui/utils";
import { useEffect, useState } from "react";
import { Player } from "../../types/Player";
import { Order } from "./DataTable";
import { StyledTableCell, StyledTableRow } from "./TableStyles";

interface EnhancedTableProps {
  numSelected: number;
  onRequestSort: (property: keyof Player) => void;
  onSelectAllClick: (event: React.ChangeEvent<HTMLInputElement>) => void;
  order: Order;
  orderBy: keyof Player;
  rowCount: number;
  data: Array<Record<string, any>>;
  selectCheckBox?: boolean;
  columnOrder?: string[];
}
export default function EnhancedTableHead(props: EnhancedTableProps) {
  const {
    onSelectAllClick,
    order,
    orderBy,
    numSelected,
    rowCount,
    onRequestSort,
    data,
    selectCheckBox,
    columnOrder,
  } = props;

  const [columns, setColumns] = useState<string[]>([]);

  const createSortHandler = (property: keyof Player) => () => {
    onRequestSort(property);
  };

  useEffect(() => {
    if (data.length > 0) {
      const cols = columnOrder
        ? [...new Set(columnOrder)]
        : Object.keys(data[0]);
      cols.push("Actions");
      setColumns(cols);
    } else {
      setColumns([]);
    }
  }, [data, selectCheckBox, columnOrder]);

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
