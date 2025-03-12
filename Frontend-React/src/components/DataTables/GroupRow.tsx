import { useDraggable } from "@dnd-kit/core";
import { Player} from "../../types/Player";

type GroupRowProps = {
  player: Player;
  columns: string[];
};

export default function GroupRow({ player, columns }: GroupRowProps) {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id: player.group_id ?? "3"
  })

  const style = transform ? {
    transform: `translate(${transform.x}.px, ${transform.y}px)`
  } : undefined

  return (
    <tr key={player.Character}
    ref={setNodeRef}
    {...listeners}
    {...attributes}
    style={style}
    >
      {columns.map((col, index) => {
        const value = player[col as keyof Player];
        return (
          <td key={`${player.Character}-${index}`}>
            {value !== undefined && value !== null ? value.toString() : ""}
          </td>
        );
      })}
    </tr>
  );
}
