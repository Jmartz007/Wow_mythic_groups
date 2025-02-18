import { Box } from "@mui/material";
import React, { useState, useEffect, FormEvent } from "react";
import Button from "react-bootstrap/Button";

interface RoleDetails {
  enabled: boolean;
  skill: number;
  combatRole: string;
}

interface FormData {
  playerName: string;
  characterName: string;
  dungeon: string;
  keylevel: number;
  className: string;
  roles: Record<Role, RoleDetails>;
}

type Role = "tank" | "healer" | "dps";

type Option = {
  id: number;
  dungeon: string;
};

const initialFormData = {
  playerName: "",
  characterName: "",
  dungeon: "",
  keylevel: 0,
  className: "",
  roles: {
    tank: { enabled: false, skill: 1, combatRole: "" },
    healer: { enabled: false, skill: 1, combatRole: "" },
    dps: { enabled: false, skill: 1, combatRole: "" },
  },
};
export default function EntryForm() {
  const [options, setOptions] = useState<Option[]>([]);
  const [formData, setFormData] = useState<FormData>(initialFormData);

  useEffect(() => {
    const fetchDungeonOptions = async () => {
      try {
        const response = await fetch("/groups/api/dungeons");

        if (!response.ok) {
          throw new Error("Failed to fetch options");
        }
        const data: Option[] = await response.json();
        setOptions(data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchDungeonOptions();
  }, []);

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleRoleChange = (
    role: Role,
    key: string,
    value: string | boolean
  ) => {
    setFormData((prev) => {
      const newRoles = { ...prev.roles };

      if (key === "skill") {
        newRoles[role] = {
          ...newRoles[role],
          skill: Number(value),
        };
      } else if (key === "combatRole") {
        newRoles[role] = {
          ...newRoles[role],
          combatRole: value as string,
        };
      } else if (key === "enabled") {
        if (value) {
          newRoles[role] = {
            ...prev.roles[role],
            enabled: true,
          };
        } else {
          delete newRoles[role];
        }
      }

      return {
        ...prev,
        roles: newRoles,
      };
    });
  };

  const toggleRole = (role: Role, checked: boolean) => {
    setFormData((prev) => ({
      ...prev,
      roles: {
        ...prev.roles,
        [role]: { ...prev.roles[role], enabled: checked },
      },
    }));
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const response = await fetch("/groups/api/players", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      console.log(JSON.stringify(formData));

      if (!response.ok) {
        throw new Error("network response error");
      }

      console.log("Form submitted succesffully");
      alert("Form submitted successfully");
      setFormData(initialFormData);
    } catch (error) {
      console.error("error submitting form: ", error);
      alert("there was an error submitting form");
    }
  };

  return (
<Box>
        <form onSubmit={handleSubmit}>
          <h1 className="title">Player Entry Form</h1>

          <div id="names">
            <label htmlFor="player">Player Name</label>
            <input
              type="text"
              id="player"
              name="playerName"
              placeholder="Your Main's Name(Jmartz)"
              required
              size={30}
              pattern="[a-zA-Z]+"
              value={formData.playerName}
              onChange={handleInputChange}
            />
            <br />
            <label htmlFor="charName">Character's Name</label>
            <input
              type="text"
              id="charName"
              name="characterName"
              placeholder="Character Name(Calioma)"
              required
              size={25}
              pattern="[a-zA-Z]+"
              value={formData.characterName}
              onChange={handleInputChange}
            />
          </div>

          <div id="keyInfo" className="container grid row gap-3">
            <div className="col">
              <label htmlFor="dungeon" className="row">
                Dungeon
              </label>
              <select
                className="form-select row p-1"
                name="dungeon"
                id="dungeon"
                value={formData.dungeon}
                onChange={handleInputChange}
              >
                <option value="">Select an option ...</option>
                {options.map((option) => (
                  <option key={option.id} value={option.dungeon}>
                    {option.dungeon}
                  </option>
                ))}
              </select>
            </div>

            <div className="col">
              <label htmlFor="keylevel" className="row">
                Key Level
              </label>
              <input
                className="row"
                type="text"
                id="keylevel"
                name="keylevel"
                value={formData.keylevel}
                pattern="[0-9]+"
                onChange={handleInputChange}
              />
            </div>
          </div>

          <br />
          <label htmlFor="className">Select your class:</label>
          <div id="className" className="container grid gap-0 row-gap-5">
            {[
              "Warrior",
              "Paladin",
              "Hunter",
              "Rogue",
              "Priest",
              "Shaman",
              "Mage",
              "Warlock",
              "Monk",
              "Druid",
              "Demon Hunter",
              "Death Knight",
              "Evoker",
            ].map((cls) => (
              <div key={cls}>
                <input
                  type="radio"
                  id={cls.toLocaleLowerCase()}
                  name="className"
                  value={cls}
                  checked={formData.className === cls}
                  onChange={handleInputChange}
                />
                <label htmlFor={cls.toLocaleLowerCase()}>{cls}</label>
              </div>
            ))}
          </div>

          <label>Select the roles you play with this character</label>
          {(["tank", "healer", "dps"] as Role[]).map((role) => (
            <div key={role}>
              <input
                type="checkbox"
                id={role}
                value={role}
                name="role"
                checked={formData.roles[role].enabled}
                onChange={(e) => toggleRole(role, e.target.checked)}
              />
              <label htmlFor={role}>
                {role.charAt(0).toLocaleUpperCase() + role.slice(1)}
              </label>

              <input
                type="range"
                min="1"
                max="3"
                id={`${role}-skill`}
                name={`${role}-skill`}
                value={formData.roles[role].skill}
                disabled={!formData.roles[role].enabled}
                onChange={(e) =>
                  handleRoleChange(role, "skill", e.target.value)
                }
              />
              <div>
                <input
                  type="radio"
                  id={`${role}-melee`}
                  name={`combat_role_${role}`}
                  value="Melee"
                  disabled={!formData.roles[role]?.enabled}
                  required={formData.roles[role]?.enabled}
                  onChange={(e) =>
                    handleRoleChange(role, "combatRole", e.target.value)
                  }
                />
                <label htmlFor={`${role}-melee`}>Melee</label>

                <input
                  type="radio"
                  id={`${role}-ranged`}
                  name={`combat_role_${role}`}
                  value="Ranged"
                  disabled={!formData.roles[role]?.enabled}
                  required={formData.roles[role]?.enabled}
                  onChange={(e) =>
                    handleRoleChange(role, "combatRole", e.target.value)
                  }
                />
                <label htmlFor={`${role}-ranged`}>Ranged</label>
              </div>
            </div>
          ))}

          <Button variant="primary" type="submit">
            Submit
          </Button>
        </form>
        </Box>
  );
}
