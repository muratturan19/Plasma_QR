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
  const [useCustomer, setUseCustomer] = useState(false)
  const [useSubject, setUseSubject] = useState(false)
  const [usePartCode, setUsePartCode] = useState(false)
  const currentYear = new Date().getFullYear()
  const years = Array.from({ length: 5 }, (_, i) => `${currentYear - i}`)
  const [selectedYear, setSelectedYear] = useState('')

  const fetchData = async () => {
    const params = new URLSearchParams()
    if (useCustomer) params.append('customer', '1')
    if (useSubject) params.append('subject', '1')
    if (usePartCode) params.append('part_code', '1')
    if (selectedYear) params.append('year', selectedYear)
    const url =
      params.toString().length > 0
        ? `${API_BASE}/complaints?${params.toString()}`
        : `${API_BASE}/complaints`
    try {
      const res = await fetch(url)
      if (!res.ok) {
        throw new Error(`HTTP error ${res.status}`)
      }
      const jsonData = await res.json()
      setData(jsonData)
      setError(null)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <Box sx={{ mt: 2, background: 'linear-gradient(180deg,#ffffff,#f0f4fa)', p: 2, borderRadius: 2, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 2 }}>
        <FormControlLabel
          control={<Checkbox checked={useCustomer} onChange={(e) => setUseCustomer(e.target.checked)} />}
          label="Müşteri"
        />
        <FormControlLabel
          control={<Checkbox checked={useSubject} onChange={(e) => setUseSubject(e.target.checked)} />}
          label="Konu"
        />
        <FormControlLabel
          control={<Checkbox checked={usePartCode} onChange={(e) => setUsePartCode(e.target.checked)} />}
          label="Parça Kodu"
        />
        <Select
          value={selectedYear}
          onChange={(e) => setSelectedYear(e.target.value)}
          displayEmpty
          size="small"
          data-testid="year-select"
        >
          <MenuItem value="">
            <em>Yıl (opsiyonel)</em>
          </MenuItem>
          {years.map((y) => (
            <MenuItem key={y} value={y}>
              {y}
            </MenuItem>
          ))}
        </Select>
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
