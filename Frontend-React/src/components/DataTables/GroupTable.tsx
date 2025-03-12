import {
  DndContext,
  closestCenter,
  DragOverlay,
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
import { useEffect, useState } from "react";
import { Item } from "./Item";
import { SortableItem } from "./SortableItem";
import GroupBox from "./GroupBox";
import { Player } from "../../types/Player";

interface GroupTableProps {
  data: Player[];
  onRowClick: (row: Player) => void;
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

export default function GroupTable({ data, onRowClick }: GroupTableProps) {
  const [columns, setColumns] = useState<string[]>([]);
  const [items, setItems] = useState<UniqueIdentifier[]>(["1", "2"]);
  const [activeId, setActiveId] = useState<UniqueIdentifier | null>(null);
  const [groups, setGroups] = useState(groupTables);

  const uniqueGroupIds = Array.from(
    new Set(
      data.map((row) => {
        row.group_id;
      })
    )
  );

  function handleDragStart(event: DragStartEvent) {
    const { active } = event;
    setActiveId(active.id);
  }
  const clickableColumns = ["Character Name"];
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  useEffect(() => {
    setColumns(columnOrder);
  }, []);

  return (
    <>
      <div className="container mt-5 table-responsive-lg">
        {groupTables.map((group) => {
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
      </div>
    </>
  );
}
