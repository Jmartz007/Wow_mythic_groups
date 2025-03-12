import { Box, Container, Typography } from "@mui/material";
import GroupTable from "../components/DataTables/GroupTable";
import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import {
  closestCenter,
  DndContext,
  DragEndEvent,
  DragOverlay,
  DragStartEvent,
  KeyboardSensor,
  PointerSensor,
  UniqueIdentifier,
  useSensor,
  useSensors,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { SortableItem } from "../components/DataTables/SortableItem";
import { Item } from "../components/DataTables/Item";
import { Player } from "../types/Player";
import GroupBox from "../components/DataTables/GroupBox";

const groupTables = [
  {
    group_id: "1",
    title: "Group 1",
  },
  {
    group_id: "2",
    title: "Group 2",
  },
  {
    group_id: "3",
    title: "Group 3",
  },
];

const columnOrder: string[] = [
  "char_name",
  "playerName",
  "wow_class",
  "role",
  "range",
  "dungeon",
  "key_level",
  "dpsConf",
  "hConf",
  "tConf",
];

export default function GroupListPage() {
  const location = useLocation();
  // const [activeId, setActiveId] = useState<UniqueIdentifier | null>(null);
  const { data } = location.state || {};
  const playerData = data as Player[]; // Type assertion
  const [playerRows, setPlayerRows] = useState<Player[]>(playerData);
  const [columns, setColumns] = useState<string[]>([]);

  useEffect(() => {
    setColumns(columnOrder);
  }, []);

  

  // const [items, setItems] = useState<UniqueIdentifier[]>(["1", "2", "3"]);


  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  // function handleDragStart(event: DragStartEvent) {
  //   const { active } = event;

  //   setActiveId(active.id);
  // }

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;

    if (!active) {
      return
    }

    const charGroupId = active.id as string;
    const newGroupId = over.id as Player['group_id'];

    setPlayerRows(() => playerRows.map(row => String(row.group_id) === charGroupId ? {...row, group_id: newGroupId} : row))
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      // onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >

<>
      <div className="container mt-5 table-responsive-lg">
        {groupTables.map((group) => {
          return (
            <GroupBox
              key={group.group_id}
              groupTable={group}
              members={playerData.filter(
                (p) => String(p.group_id) === group.group_id
              )}
              columns={columns}
            />
          );
        })}
      </div>
    </>
    </DndContext>
  );
}
