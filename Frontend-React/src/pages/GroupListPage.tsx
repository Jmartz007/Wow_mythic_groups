import { Box, Container, Typography } from "@mui/material";
import GroupTable from "../components/GroupTable";
import { useLocation } from "react-router-dom";
import { useState } from "react";
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
import { SortableItem } from "../components/SortableItem";
import { Item } from "../components/Item";

export default function GroupListPage() {
  const location = useLocation();
  const [activeId, setActiveId] = useState<UniqueIdentifier | null>(null);
  const { data } = location.state || {};
  const [items, setItems] = useState<UniqueIdentifier[]>(["1", "2", "3"]);
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  function handleDragStart(event: DragStartEvent) {
    const { active } = event;

    setActiveId(active.id);
  }

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      setItems((items) => {
        const oldIndex = items.indexOf(active.id);
        const newIndex = items.indexOf(over.id);

        return arrayMove(items, oldIndex, newIndex);
      });
    }
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
      <SortableContext items={items} strategy={verticalListSortingStrategy}>
        {items.map((id) => (
          <SortableItem key={id} id={id} />
        ))}
      </SortableContext>
      <DragOverlay>
        {activeId ? <Item id={activeId.toString()} /> : null}
      </DragOverlay>
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
    </DndContext>
  );
}
