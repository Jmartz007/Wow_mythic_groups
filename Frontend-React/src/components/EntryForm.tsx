import {
  Box,
  Button,
  Paper,
  Select,
  TextField,
  SelectChangeEvent,
  MenuItem,
  InputLabel,
  FormControl,
  FormHelperText,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  FormGroup,
  Checkbox,
  Slider,
  Typography,
  useTheme,
} from "@mui/material";
import React, { useState, useEffect, FormEvent } from "react";
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

const Classes = {
  Warrior: "darkkhaki",
  Paladin: "pink",
  Hunter: "lightgreen",
  Rogue: "yellow",
  Priest: "white",
  Shaman: "royalblue",
  Mage: "aqua",
  Warlock: "purple",
  Monk: "springgreen",
  Druid: "orange",
  "Demon Hunter": "darkmagenta",
  "Death Knight": "red",
  Evoker: "darkgreen",
};

const getAdjustedColor = (color: string, isLightTheme: boolean) => {
  if (isLightTheme) {
    switch (color) {
      case "white":
        return "#000"; // Change white to black for visibility
      case "yellow":
        return "#d4a017"; // A darker yellow
      case "royalblue":
        return "darkblue";
      case "darkkhaki":
        return "saddlebrown";
      default:
        return color; // Keep other colors the same
    }
  }
  return color; // No changes for dark theme
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
  const theme = useTheme();
  const isLightTheme = theme.palette.mode === "light";

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
    e:
      | React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
      | SelectChangeEvent<string>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleClassChange = (
    event: React.ChangeEvent<HTMLInputElement>,
    value: string
  ) => {
    const name = event.target.name;
    const targetValue = event.target.value;
    // const value = checked;
    console.log(`name: ${name}, targetValue: ${targetValue}, value: ${value} `);
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleRoleChange = (
    role: Role,
    key: string,
    value: string | boolean | number | number[]
  ) => {
    console.log(`key: ${key}, value: ${value}`);
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

  const toggleRole = (role: Role, value: boolean) => {
    console.log(`value: ${value}`);
    setFormData((prev) => ({
      ...prev,
      roles: {
        ...prev.roles,
        [role]: { ...prev.roles[role], enabled: value },
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
    <Paper elevation={6}>
      <Box padding={4} gap={4}>
        <form onSubmit={handleSubmit}>
          <Box
            display="flex"
            flexDirection="row"
            gap={2}
            marginBottom={2}
            id="names"
          >
            <TextField
              type="text"
              label="Player Name"
              id="player"
              name="playerName"
              placeholder="Your Main's Name"
              helperText="Player Name"
              required
              size="small"
              value={formData.playerName}
              onChange={handleInputChange}
            />
            <TextField
              type="text"
              label="Character's Name"
              id="charName"
              name="characterName"
              placeholder="Character Name"
              helperText="Character Name"
              required
              size="small"
              value={formData.characterName}
              onChange={handleInputChange}
            />
          </Box>

          <Box
            display="flex"
            flexDirection="row"
            gap={4}
            paddingBlockEnd={4}
            id="keyInfo"
          >
            <FormControl sx={{ minWidth: 120, maxWidth: 400, flexShrink: 1 }}>
              <InputLabel id="dungeon-label">Dungeon</InputLabel>
              <Select
                name="dungeon"
                id="dungeon"
                labelId="dungeon-label"
                // label="Dungeon"
                size="small"
                variant="filled"
                value={formData.dungeon}
                onChange={handleInputChange}
              >
                {options.map((option) => (
                  <MenuItem key={option.id} value={option.dungeon}>
                    {option.dungeon}
                  </MenuItem>
                ))}
              </Select>
              <FormHelperText>Dungeon</FormHelperText>
            </FormControl>

            <TextField
              className="row"
              type="number"
              id="keylevel"
              name="keylevel"
              label="Key Level"
              size="small"
              value={formData.keylevel}
              onChange={handleInputChange}
              sx={{ maxWidth: 120 }}
            />
          </Box>

          <Box>
            <FormControl>
              <FormLabel id="className">Select your class:</FormLabel>
              <RadioGroup
                name="className"
                onChange={handleClassChange}
                value={formData.className}
              >
                {Object.entries(Classes).map(([cls, clr]) => {
                  const adjustedColor = getAdjustedColor(clr, isLightTheme);
                  return (
                    <FormControlLabel
                      key={cls}
                      control={<Radio />}
                      label={cls}
                      value={cls}
                      sx={{ color: adjustedColor }}
                    />
                  );
                })}
              </RadioGroup>
            </FormControl>
          </Box>

          <Box marginBlock={4} minWidth={200} maxWidth={400}>
            <Typography variant="h6">
              Select the roles you play with this character
            </Typography>
            {(["tank", "healer", "dps"] as Role[]).map((role) => (
              <Box key={role} marginBlock={2.5}>
                <FormGroup>
                  <FormControlLabel
                    name="role"
                    id={role}
                    control={
                      <Checkbox
                        checked={formData.roles[role].enabled}
                        onChange={(e, value) => toggleRole(role, value)}
                      />
                    }
                    label={role.charAt(0).toLocaleUpperCase() + role.slice(1)}
                  />
                  <Typography>Skill Level</Typography>
                  <Slider
                    step={1}
                    marks
                    min={1}
                    max={5}
                    name={`${role}-skill`}
                    value={formData.roles[role].skill}
                    disabled={!formData.roles[role].enabled}
                    onChange={(e, value) =>
                      handleRoleChange(role, "skill", value)
                    }
                  />

                  <RadioGroup
                    name={`combat_role_${role}`}
                    value={formData.roles[role].combatRole}
                    onChange={(e, value) =>
                      handleRoleChange(role, "combatRole", value)
                    }
                    row
                  >
                    <FormControlLabel
                      value="Melee"
                      control={<Radio />}
                      label="Melee"
                      disabled={!formData.roles[role]?.enabled}
                      required={formData.roles[role]?.enabled}
                    />
                    <FormControlLabel
                      value="Ranged"
                      control={<Radio />}
                      label="Ranged"
                      disabled={!formData.roles[role]?.enabled}
                      required={formData.roles[role]?.enabled}
                    />
                  </RadioGroup>
                </FormGroup>
              </Box>
            ))}
          </Box>

          <Button variant="contained" type="submit">
            Submit
          </Button>
        </form>
      </Box>
    </Paper>
  );
}
