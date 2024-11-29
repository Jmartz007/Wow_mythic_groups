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
  class: string;
  roles: Record<Role, RoleDetails>;
}

type Role = "tank" | "healer" | "dps";

type Option = {
  id: number;
  DungeonName: string;
};

export default function EntryForm() {
  const [options, setOptions] = useState<Option[]>([]);
  const [formData, setFormData] = useState<FormData>({
    playerName: "",
    characterName: "",
    dungeon: "",
    keylevel: 0,
    class: "",
    roles: {
      tank: { enabled: false, skill: 0, combatRole: "" },
      healer: { enabled: false, skill: 0, combatRole: "" },
      dps: { enabled: false, skill: 0, combatRole: "" },
    },
  });

  useEffect(() => {
    const fetchDungeonOptions = async () => {
      try {
        const response = await fetch(
          "http://localhost:5000/groups/api/dungeons"
        );

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

  const handleRoleChange = (role: Role, key: keyof RoleDetails, value: any) => {
    setFormData((prev) => ({
      ...prev,
      roles: {
        ...prev.roles,
        [role]: {
          ...prev.roles[role],
          [key]: value,
        },
      },
    }));
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
      const response = await fetch("url", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify("formData"),
      });

      console.log(JSON.stringify);

      if (!response.ok) {
        throw new Error("network response error");
      }

      alert("Form submitted succesffully");
    } catch (error) {
      console.error("error submitting form: ", error);
      alert("there was an error submitting form");
    }
  };

  return (
    <>
      <div className="rounded border border-1 shadow bg-primary-subtle p-4">
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
                <option value="" disabled>
                  Select an option ...
                </option>
                {options.map((option) => (
                  <option key={option.id} value={option.DungeonName}>
                    {option.DungeonName}
                  </option>
                ))}
                {/* <option value="Unknown">Unknown</option>
                  <option value="City of Threads">City of Threads</option> */}
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
          <label htmlFor="class">Select your class:</label>
          <div id="class" className="container grid gap-0 row-gap-5">
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
                  name="class"
                  value={cls}
                  checked={formData.class === cls}
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
                  disabled={!formData.roles[role].enabled}
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
                  disabled={!formData.roles[role].enabled}
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
      </div>
    </>
  );
}
