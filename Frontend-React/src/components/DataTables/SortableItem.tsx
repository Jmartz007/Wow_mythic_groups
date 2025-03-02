import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { Item } from "./Item";
import { UniqueIdentifier } from "@dnd-kit/core";

interface SortableItemProps {
  id: UniqueIdentifier;
}

export function SortableItem(props: SortableItemProps) {
  const { attributes, listeners, setNodeRef, transform, transition } =
    useSortable({ id: props.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <Item
      id={props.id.toString()}
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
    >
      {"value"}
    </Item>
  );
}
