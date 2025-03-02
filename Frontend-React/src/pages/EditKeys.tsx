import { Player } from "../types/Player";
import { Box, Container, Typography } from "@mui/material";
import EditingTable from "../components/DataTables/EditingTable";

interface EditKeysProps {
  data: Player[];
  setData: React.Dispatch<React.SetStateAction<Player[]>>;
  onDelete: (row: Record<string, any>) => Promise<void>;
}

export default function EditKeys({ data, setData, onDelete }: EditKeysProps) {
  const editingColumns: string[] = ["Dungeon", "Key Level"];

  const columnOrder: string[] = [
    "Character",
    "Class",
    "Player",
    "Dungeon",
    "Key Level",
  ];

  return (
    <Container>
      <Box paddingBottom={12}>
        <Box
          display="flex"
          flexDirection="row"
          justifyContent="start"
          sx={{ padding: 2, margin: 2 }}
        >
          <Typography variant="h3">Edit Keys</Typography>
        </Box>

        <Box display="flex" flexDirection="column" alignContent="space-between">
          <EditingTable
            data={data}
            setData={setData}
            onDelete={onDelete}
            columnOrder={columnOrder}
            editingColumns={editingColumns}
          />
        </Box>
      </Box>
    </Container>
  );
}
