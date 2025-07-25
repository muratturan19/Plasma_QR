import { useMemo, useState } from 'react'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import Home from './pages/Home'
import Header from './components/Header'

function App() {
  const [mode, setMode] = useState('light')
  const toggleColorMode = () => {
    setMode((prev) => (prev === 'light' ? 'dark' : 'light'))
  }

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          primary: {
            main: '#002855'
          },
          secondary: {
            main: '#14397c'
          }
        },
        shape: { borderRadius: 12 },
        typography: {
          fontFamily: "'Poppins','Inter','Roboto','Helvetica','Arial',sans-serif",
          fontSize: 14
        },
        components: {
          MuiButton: { defaultProps: { size: 'small' } },
          MuiTextField: { defaultProps: { size: 'small' } },
          MuiSelect: { defaultProps: { size: 'small' } },
          MuiAutocomplete: { defaultProps: { size: 'small' } }
        }
      }),
    [mode]
  )

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Header toggleColorMode={toggleColorMode} mode={mode} />
      <Home />
    </ThemeProvider>
  )
}

export default App
