import { useState } from 'react'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import FormControlLabel from '@mui/material/FormControlLabel'
import Checkbox from '@mui/material/Checkbox'
import Select from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import { API_BASE } from '../api'
import FileDownloadIcon from '@mui/icons-material/FileDownload'

function ComplaintFetcher() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [useA, setUseA] = useState(false)
  const [useB, setUseB] = useState(false)
  const [useC, setUseC] = useState(false)
  const currentYear = new Date().getFullYear()
  const years = Array.from({ length: 5 }, (_, i) => `${currentYear - i}`)
  const [yearA, setYearA] = useState(years[0])
  const [yearB, setYearB] = useState(years[0])
  const [yearC, setYearC] = useState(years[0])

  const fetchData = async () => {
    const queries = []
    if (useA) queries.push(`year=${yearA}`)
    if (useB) queries.push(`year=${yearB}`)
    if (useC) queries.push(`year=${yearC}`)
    const urls =
      queries.length > 0
        ? queries.map((q) => `${API_BASE}/complaints?${q}`)
        : [`${API_BASE}/complaints`]
    try {
      const responses = await Promise.all(urls.map((u) => fetch(u)))
      const jsonData = []
      for (const res of responses) {
        if (!res.ok) {
          throw new Error(`HTTP error ${res.status}`)
        }
        jsonData.push(await res.json())
      }
      const merged = { store: [], excel: [] }
      jsonData.forEach((j) => {
        merged.store.push(...(j.store || []))
        merged.excel.push(...(j.excel || []))
      })
      setData(merged)
      setError(null)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <Box sx={{ mt: 2, background: 'linear-gradient(180deg,#ffffff,#f0f4fa)', p: 2, borderRadius: 2, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 2 }}>
        <FormControlLabel
          control={<Checkbox checked={useA} onChange={(e) => setUseA(e.target.checked)} />}
          label={
            <Select value={yearA} onChange={(e) => setYearA(e.target.value)} size="small">
              {years.map((y) => (
                <MenuItem key={y} value={y}>
                  {y}
                </MenuItem>
              ))}
            </Select>
          }
        />
        <FormControlLabel
          control={<Checkbox checked={useB} onChange={(e) => setUseB(e.target.checked)} />}
          label={
            <Select value={yearB} onChange={(e) => setYearB(e.target.value)} size="small">
              {years.map((y) => (
                <MenuItem key={y} value={y}>
                  {y}
                </MenuItem>
              ))}
            </Select>
          }
        />
        <FormControlLabel
          control={<Checkbox checked={useC} onChange={(e) => setUseC(e.target.checked)} />}
          label={
            <Select value={yearC} onChange={(e) => setYearC(e.target.value)} size="small">
              {years.map((y) => (
                <MenuItem key={y} value={y}>
                  {y}
                </MenuItem>
              ))}
            </Select>
          }
        />
      </Box>
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
