import { useDraggable } from "@dnd-kit/core";
import { Player } from "../../types/Player";
import { useSortable } from "@dnd-kit/sortable";

type GroupRowProps = {
  player: Player;
  columns: string[];
};

// export default function GroupRow({ player, columns }: GroupRowProps) {
//   const { attributes, listeners, setNodeRef, transform } = useDraggable({
//     id: player.group_id ?? "3",
//   });

//   const style = transform
//     ? {
//         transform: `translate(${transform.x}.px, ${transform.y}px)`,
//       }
//     : undefined;

//   return (
//     <tr
//       ref={setNodeRef}
//       key={player.Character}
//       {...listeners}
//       {...attributes}
//       style={style}
//     >
//       {columns.map((col, index) => {
//         const value = player[col as keyof Player];
//         return (
//           <td key={`${player.Character}-${index}`}>
//             {value !== undefined && value !== null ? value.toString() : ""}
//           </td>
//         );
//       })}
//     </tr>
//   );
// }

export default function GroupRow({ row }: GroupRowProps) {
  const { attributes, listeners, transform, setNodeRef, isDragging } =
    useSortable({
      id: row.original.id,
    });

  return (
    <tr ref={setNodeRef}>
      {isDragging ? (
        <DraggingRow colSpan={row.cells.length}>&nbsp;</DraggingRow>
      ) : (
        row.cells.map()
      )}
    </tr>
  );
}
