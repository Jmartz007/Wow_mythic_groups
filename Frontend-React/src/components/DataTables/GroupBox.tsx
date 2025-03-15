import { useDroppable } from "@dnd-kit/core";
import { Player } from "../../types/Player";
import GroupRow from "./GroupRow";

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

type GroupProps = {
  groupTable: {
    group_id: string;
    title: string;
  };
  members: Player[];
  columns: string[];
};

export function GroupBox({ groupTable, members, columns }: GroupProps) {
  // TODO: fetch only the specific data for the group
  const { setNodeRef } = useDroppable({
    id: groupTable.group_id,
  });

  return (
    <div ref={setNodeRef}>
      <h2>{groupTable.title}</h2>
      <table className="table table-striped table-hover">
        <thead className="table-dark">
          <tr>
            {columns.map((col) => (
              <th key={col}>{columnMapping[col]}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Object.values(members).map((player) => (
            <GroupRow
              key={player.Character}
              player={player}
              columns={columns}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default GroupBox;
export type { GroupProps };
