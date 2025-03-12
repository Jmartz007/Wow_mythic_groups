import { useDraggable } from "@dnd-kit/core";
import { Player, PlayerValue } from "../../types/Player";

type GroupRowProps = {
  player: Player;
  columns: string[];
};

export default function GroupRow({ player, columns }: GroupRowProps) {
  return (
    <tr key={player.Character}>
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
