import { styled, TableCell, tableCellClasses, TableRow } from "@mui/material";

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

const StyledTableRow = styled(TableRow)(() => ({
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

export { StyledTableCell, StyledTableRow };
