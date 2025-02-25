import { Box, Container, Typography } from "@mui/material";
import GroupTable from "../components/DataTables/GroupTable";
import { useLocation } from "react-router-dom";

export default function GroupListPage() {
  const location = useLocation();
  const { data } = location.state || {};

  return (
    <Container>
      <Box paddingBottom={12}>
        <Box
          display="flex"
          flexDirection="row"
          justifyContent="start"
          sx={{ padding: 2, margin: 2 }}
        >
          <Typography variant="h3">Groups</Typography>
        </Box>
        <GroupTable data={data} onRowClick={() => {}} />
      </Box>
    </Container>
  );
}
