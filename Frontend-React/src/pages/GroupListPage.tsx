import { Box, Container, Typography } from "@mui/material";
import { useLocation } from "react-router-dom";
import GroupTableDragable from "../components/DataTables/GroupTableMUI";
import AffixInfo from "../components/Affixes";

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
        <Box
          display="flex"
          flexDirection="row"
          justifyContent="start"
          sx={{
            padding: 2,
            margin: 2,
          }}
        >
          <AffixInfo />
        </Box>
        <GroupTableDragable data={data} />
      </Box>
    </Container>
  );
}
