import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import IconButton from '@mui/material/IconButton'
import useMediaQuery from '@mui/material/useMediaQuery'
import Box from '@mui/material/Box'
import { useTheme } from '@mui/material/styles'
import Brightness4Icon from '@mui/icons-material/Brightness4'
import Brightness7Icon from '@mui/icons-material/Brightness7'
import HelpOutlineIcon from '@mui/icons-material/HelpOutline'
import SettingsIcon from '@mui/icons-material/Settings'
import logo from '/logo.png'

function Header({ toggleColorMode, mode }) {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))

  return (
    <AppBar
      position="static"
      sx={{
        backgroundColor: theme.palette.background.paper,
        color: theme.palette.text.primary,
        boxShadow: theme.shadows[1]
      }}
    >
      <Toolbar>
        <Box component="img" src={logo} alt="Company Logo" sx={{ height: isMobile ? 40 : 50, mr: 2 }} />
        <Typography variant={isMobile ? 'h6' : 'h5'} sx={{ flexGrow: 1 }}>
          Plasma QR
        </Typography>
        <IconButton color="inherit" aria-label="help">
          <HelpOutlineIcon />
        </IconButton>
        <IconButton color="inherit" aria-label="settings">
          <SettingsIcon />
        </IconButton>
        <IconButton color="inherit" onClick={toggleColorMode} aria-label="toggle color mode">
          {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
        </IconButton>
      </Toolbar>
    </AppBar>
  )
}

export default Header
