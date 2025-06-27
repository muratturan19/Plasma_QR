import { useState } from 'react'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import { API_BASE } from '../api'

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
    <Box sx={{ mt: 2 }}>
      <Button variant="outlined" onClick={fetchData} sx={{ mb: 2 }}>
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
