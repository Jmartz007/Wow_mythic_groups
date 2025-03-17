import { useEffect, useMemo, useState } from "react";
import {
  type MRT_TableOptions,
  type MRT_ColumnDef,
  type MRT_Row,
  MaterialReactTable,
  useMaterialReactTable,
} from "material-react-table";
import { Box, Link, Typography } from "@mui/material";
// import { data, type Person } from "./makeData";
import { Player } from "../../types/Player";

interface Group {
  [playerKey: string]: Player;
}

interface GroupedPlayers {
  [groupId: string]: Group;
}

interface GroupTableProps {
  data: GroupedPlayers;
}

async function fetchRaiderIo(char_name: string) {
  const baseUrl = "https://raider.io/api/v1/characters/profile";
  const params = new URLSearchParams({
    region: "us",
    realm: "lightbringer",
    name: char_name,
    fields: "gear,mythic_plus_highest_level_runs",
  });
  try {
    const response = await fetch(`${baseUrl}?${params.toString()}`);

    if (!response.ok) {
      console.error(`Failed to fetch data for ${char_name}`);
      throw new Error(
        `Failed to fetch data for ${char_name}: ${response.statusText}`
      );
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

const GroupTableDragable = ({ data }: GroupTableProps) => {
  const columns = useMemo<MRT_ColumnDef<Player>[]>(
    //column definitions...
    () => [
      {
        accessorKey: "char_name",
        header: "Character Name",
      },
      {
        accessorKey: "iLvl",
        header: "iLvl",
        size: 60,
        minSize: 40,
        maxSize: 100,
      },
      {
        accessorKey: "dungeon",
        header: "Dungeon",
      },
      {
        accessorKey: "key_level",
        header: "Key Level",
        grow: false,
        size: 30,
      },
      {
        accessorKey: "role",
        header: "Role",
        size: 40,
      },
      {
        accessorKey: "wow_class",
        header: "Class",
        size: 40,
      },

      {
        accessorKey: "Highest Key",
        header: "Highest Key",
        size: 50,
      },
      {
        accessorKey: "playerName",
        header: "Player Name",
      },
      {
        accessorKey: "profileUrl",
        header: "Profile",
        grow: true,
        Cell: ({ cell }) => (
          <Link href={cell.getValue<string>()} target="_blank">
            {cell.getValue<string>()}
          </Link>
        ),
      },
    ],
    []
    //end
  );

  // const groupKeys = Object.keys(data);
  // const initialDataStates = groupKeys.map((key) => Object.values(data[key]));

  // const [dataStates, setDataStates] = useState<Player[][]>(initialDataStates);
  const [draggingRow, setDraggingRow] = useState<MRT_Row<Player> | null>(null);
  const [hoveredTable, setHoveredTable] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [enrichedData, setEnrichedData] = useState<GroupedPlayers>(data);

  useEffect(() => {
    async function fetchAdditionalData() {
      const newData = { ...data };

      const fetchPromises: Promise<void>[] = [];

      for (const [groupName, groupData] of Object.entries(newData)) {
        for (const [charKey, row] of Object.entries(groupData)) {
          const promise = fetchRaiderIo(String(row.char_name)).then(
            (apiData) => {
              if (apiData) {
                const { gear, profile_url, mythic_plus_highest_level_runs } =
                  apiData;
                const { item_level_equipped } = gear;
                let highestKey = "";

                if (
                  mythic_plus_highest_level_runs &&
                  mythic_plus_highest_level_runs.length > 0
                ) {
                  const { mythic_level, short_name } =
                    mythic_plus_highest_level_runs[0];
                  highestKey = `${short_name} ${mythic_level}`;
                }

                newData[groupName][charKey] = {
                  ...row,
                  profileUrl: profile_url,
                  iLvl: item_level_equipped,
                  "Highest Key": highestKey,
                };
              }
            }
          );
          fetchPromises.push(promise);
        }
      }

      await Promise.all(fetchPromises);
      setEnrichedData(newData);
      setLoading(false);
    }

    fetchAdditionalData();
  }, [data]);

  const commonTableProps: Partial<MRT_TableOptions<Player>> & {
    columns: MRT_ColumnDef<Player>[];
  } = {
    columns,
    enableRowDragging: true,
    enableFullScreenToggle: false,
    enablePagination: false,
    muiTableContainerProps: {
      sx: {
        minHeight: "400px",
      },
    },
    onDraggingRowChange: setDraggingRow,
    state: { draggingRow },
  };

  const tables = Object.keys(enrichedData).map((groupName, index) => {
    const tableId = `table-${index + 1}`;
    const dataState = Object.values(enrichedData[groupName]);
    return useMaterialReactTable({
      ...commonTableProps,
      defaultColumn: {
        minSize: 20,
      },
      data: dataState,
      getRowId: (originalRow) => `${tableId}-${originalRow.char_name}`,
      muiRowDragHandleProps: {
        onDragEnd: () => {
          if (hoveredTable && hoveredTable !== tableId) {
            const targetIndex = parseInt(hoveredTable.split("-")[1]) - 1;
            setEnrichedData((prevStates) => {
              const newStates: GroupedPlayers = { ...prevStates };
              const sourceGroup = Object.keys(newStates)[index];
              const targetGroup = Object.keys(newStates)[targetIndex];

              newStates[targetGroup] = {
                ...newStates[targetGroup],
                [draggingRow!.original.char_name as string]:
                  draggingRow!.original,
              };
              delete newStates[sourceGroup][
                draggingRow!.original.char_name as string
              ];
              return newStates;
            });
          }
          setHoveredTable(null);
        },
      },
      muiTableProps: {
        onDragEnter: () => setHoveredTable(tableId),
        sx: {
          outline: hoveredTable === tableId ? "3px dashed pink" : undefined,
        },
      },
      renderTopToolbarCustomActions: () => (
        <Typography
          color={index % 2 === 0 ? "success.main" : "error.main"}
          component="span"
          variant="h4"
        >
          {`Group ${index + 1}`}
        </Typography>
      ),
    });
  });
  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Box
      sx={{
        display: "grid",
        gridTemplateColumns: { xs: "auto", lg: "1fr" },
        gap: "1rem",
        overflow: "auto",
        p: "4px",
      }}
    >
      {tables.map((table, index) => (
        <MaterialReactTable key={index} table={table} />
      ))}
    </Box>
  );
};

export default GroupTableDragable;
