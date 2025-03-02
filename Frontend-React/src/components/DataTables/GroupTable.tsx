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

interface GroupTableProps {
  data: Array<Record<string, any>>;
  onRowClick: (row: Record<string, any>) => void;
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

export default function GroupTable({ data, onRowClick }: GroupTableProps) {
  const [columns, setColumns] = useState<string[]>([]);
  const [items, setItems] = useState<UniqueIdentifier[]>(["1", "2"]);
  const [activeId, setActiveId] = useState<UniqueIdentifier | null>(null);

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
    <div className="container mt-5 table-responsive-lg">
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
        {Object.entries(data).map(([groupName, groupData]) => (
          <div key={groupName}>
            <h2>Group {groupName}</h2>

            <table className="table table-striped table-hover ">
              <thead className="table-dark">
                <tr>
                  {columns.map((col) => (
                    <th key={col}>{columnMapping[col]}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {Object.values(groupData).map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {columns.map((col) => (
                      <td
                        key={`${rowIndex}-${col}`}
                        onClick={
                          clickableColumns.includes(col)
                            ? () => onRowClick && onRowClick(row)
                            : undefined
                        }
                        className={
                          clickableColumns.includes(col) ? "clickable-cell" : ""
                        }
                      >
                        {row[col] !== undefined && row[col] !== null
                          ? row[col].toString()
                          : ""}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </DndContext>
    </div>
  );
}
