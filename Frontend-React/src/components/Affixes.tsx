import {
  IconButton,
  ImageList,
  ImageListItem,
  ImageListItemBar,
  Popover,
  Tooltip,
  Typography,
} from "@mui/material";
import InfoIcon from "@mui/icons-material/Info";
import { useEffect, useState } from "react";

interface Affix {
  name: string;
  icon_url: string;
  description: string;
}

export default function AffixInfo() {
  const [affixes, setAffixes] = useState<Affix[]>([]);
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
  const [selectedAffix, setSelectedAffix] = useState<Affix | null>(null);

  const fetchAffixes = async () => {
    try {
      const response = await fetch(
        `https://raider.io/api/v1/mythic-plus/affixes?region=us&locale=en`
      );

      if (!response.ok) {
        console.error("error fetching affixes");
        throw Error("error fetching data");
      }
      const data = await response.json();
      return data.affix_details;
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const getAffixes = async () => {
      const affixDetails = await fetchAffixes();
      if (affixDetails) {
        setAffixes(affixDetails);
      }
    };
    getAffixes();
  }, []);

  const handleClick = (event: React.MouseEvent<HTMLElement>, affix: Affix) => {
    setAnchorEl(event.currentTarget);
    setSelectedAffix(affix);
  };

  const handleClose = () => {
    setAnchorEl(null);
    setSelectedAffix(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? "affix-popover" : undefined;

  return (
    <>
      <ImageList sx={{ width: 500, height: 125 }} cols={4} rowHeight={125}>
        {affixes.map((affix) => (
          <ImageListItem
            key={affix.icon_url}
            onClick={(event) => handleClick(event, affix)}
          >
            <Tooltip title={affix.name}>
              <img
                srcSet={`${affix.icon_url}?w=82&h=82&fit=crop&auto=format&dpr=2 2x`}
                src={`${affix.icon_url}?w=82&h=82&fit=crop&auto=format`}
                alt={affix.name}
                loading="lazy"
              />
            </Tooltip>
            <ImageListItemBar
              title={affix.name}
              sx={{
                "& .MuiImageListItemBar-title": { fontSize: 12 },
              }}
            />
          </ImageListItem>
        ))}
      </ImageList>
      {open && (
        <Popover
          id={id}
          open={open}
          anchorEl={anchorEl}
          onClose={handleClose}
          anchorOrigin={{
            vertical: "bottom",
            horizontal: "center",
          }}
          transformOrigin={{
            vertical: "top",
            horizontal: "center",
          }}
        >
          <Typography sx={{ p: 2 }}>{selectedAffix?.description}</Typography>
        </Popover>
      )}
    </>
  );
}
