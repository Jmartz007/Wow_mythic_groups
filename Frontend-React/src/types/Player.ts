export interface Player {
    Character: string;
    Class: string;
    Dungeon: string;
    "Is Active": number;
    "Key Level": number;
    Player: string;
    Range: string;
    "Role Skill": number[];
    "Role Type": string[];
    "Skill Level": number;
    group_id?: number;
    [key: string]: string | number| number[] | string[] | undefined;
  }

export type PlayerKey = keyof Player;
export type PlayerValue = Player[PlayerKey];

