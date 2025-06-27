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
            main: mode === 'light' ? '#0d47a1' : '#90caf9'
          }
        },
        shape: { borderRadius: 12 },
        typography: {
          fontFamily: "'Inter','Roboto','Helvetica','Arial',sans-serif"
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
