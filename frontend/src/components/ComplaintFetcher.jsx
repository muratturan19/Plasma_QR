import { useState } from 'react'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import { API_BASE } from '../api'
import FileDownloadIcon from '@mui/icons-material/FileDownload'

function ComplaintFetcher() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  const fetchData = async () => {
    try {
      const response = await fetch(`${API_BASE}/complaints`)
      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`)
      }
      const json = await response.json()
      setData(json)
      setError(null)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <Box sx={{ mt: 2, background: 'linear-gradient(180deg,#ffffff,#f0f4fa)', p: 2, borderRadius: 2, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
      <Button
        variant="contained"
        onClick={fetchData}
        startIcon={<FileDownloadIcon />}
        sx={{ mb: 2, px: 3, py: 1.2 }}
      >
        Fetch Complaints
      </Button>
      {error && (
        <Typography color="error" variant="body2">{error}</Typography>
      )}
      {data && (
        <pre style={{ whiteSpace: 'pre-wrap' }}>
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </Box>
  )
}

export default ComplaintFetcher
