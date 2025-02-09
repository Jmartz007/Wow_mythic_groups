import { createTheme, ThemeOptions } from "@mui/material/styles";

const darkTheme: ThemeOptions = createTheme({
    palette: {
        mode: 'dark',
        primary: {
          main: '#38796f',
        },
        secondary: {
          main: '#793841',
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



const lightTheme: ThemeOptions = createTheme({
    palette: {
        mode: 'light',
        primary: {
          main: '#38796f',
        },
        secondary: {
          main: '#793841',
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
    })

export {lightTheme, darkTheme};