import { createTheme, ThemeOptions } from "@mui/material/styles";

const darkTheme: ThemeOptions = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: "#38796f",
    },
    secondary: {
      main: "#b5a756",
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: "8px", // Rounded buttons
          padding: "10px 20px",
        },
      },
    },
    // MuiTableHead: {
    //   styleOverrides: {
    //     root: {
    //       backgroundColor: "#38796f"
    //     }
    //   }
    // }
    // MuiAppBar: { styleOverrides: { root: { backgroundColor: "#b5a756" } } },
  },
});

const lightTheme: ThemeOptions = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#38796f",
    },
    secondary: {
      main: "#b5a756",
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: "8px", // Rounded buttons
          padding: "10px 20px",
        },
      },
    },
  },
});

export { lightTheme, darkTheme };
