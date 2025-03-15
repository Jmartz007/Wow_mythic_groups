import {
  DndContext,
  closestCenter,
  DragEndEvent,
  DragStartEvent,
  UniqueIdentifier,
  useSensors,
  useSensor,
  PointerSensor,
  KeyboardSensor,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { useEffect, useMemo, useState } from "react";
import GroupBox from "./GroupBox";
import { Player } from "../../types/Player";

interface GroupTableProps {
  columns: string[];
  data: Player[];
  setData: (arg: Player[]) => void;
  // onRowClick: (row: Player) => void;
}

const columnMapping: Record<string, string> = {
  char_name: "Character Name",
  dpsConf: "DPS Confidence",
  dungeon: "Dungeon",
  hConf: "Healer Confidence",
  is_active: "Active",
  key_level: "Key Level",
  playerName: "Player Name",
  range: "Range",
  role: "Role",
  tConf: "Tank Confidence",
  wow_class: "Class",
};

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

export default function GroupTable({
  columns,
  data,
  setData,
}: GroupTableProps) {
  const [activeId, setActiveId] = useState<UniqueIdentifier | null>(null);

  const items = useMemo(
    () =>
      data
        ?.map(({ id }) => id)
        .filter((id): id is UniqueIdentifier => id !== undefined),
    [data]
  );

  function handleDragStart(event: DragStartEvent) {
    const { active } = event;
    setActiveId(active.id);
  }

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    if (over && active.id !== over.id) {
      const oldIndex: number = items.indexOf(active.id);
      const newIndex: number = items.indexOf(over.id);
      const newData = arrayMove(data, oldIndex, newIndex);
      setData(newData);
    }

    setActiveId(null);
  }

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  // useEffect(() => {
  //   setColumns(columnOrder);
  // }, []);

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
      <table className="table table-striped table-hover">
        <thead className="table-dark">
          <tr>
            {columns.map((col) => (
              <th key={col}>{columnMapping[col]}</th>
            ))}
          </tr>
        </thead>
        <div className="container mt-5 table-responsive-lg">
          <tbody>
            <SortableContext
              items={items}
              strategy={verticalListSortingStrategy}
            >
              {data.map((group) => {
                return (
                  <GroupBox
                    key={group.group_id}
                    groupTable={group}
                    members={data.filter(
                      (p) => String(p.group_id) === group.group_id
                    )}
                    columns={columns}
                  />
                );
              })}
            </SortableContext>
          </tbody>
        </div>
      </table>
    </DndContext>
  );
}
