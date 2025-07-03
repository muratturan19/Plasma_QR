import { useState } from 'react'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import FormControlLabel from '@mui/material/FormControlLabel'
import Checkbox from '@mui/material/Checkbox'
import TextField from '@mui/material/TextField'
import Select from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import { API_BASE } from '../api'
import FileDownloadIcon from '@mui/icons-material/FileDownload'
import Table from '@mui/material/Table'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import TableCell from '@mui/material/TableCell'
import TableBody from '@mui/material/TableBody'
import Tooltip from '@mui/material/Tooltip'

function ComplaintFetcher() {
  const [rows, setRows] = useState([])
  const [error, setError] = useState(null)
  const [useCustomer, setUseCustomer] = useState(false)
  const [useSubject, setUseSubject] = useState(false)
  const [usePartCode, setUsePartCode] = useState(false)
  const [customer, setCustomer] = useState('')
  const [subject, setSubject] = useState('')
  const [partCode, setPartCode] = useState('')
  const currentYear = new Date().getFullYear()
  const years = Array.from({ length: 5 }, (_, i) => `${currentYear - i}`)
  const [selectedYear, setSelectedYear] = useState('')

  const fetchData = async () => {
    const params = new URLSearchParams()
    if (useCustomer && customer) params.append('customer', customer)
    if (useSubject && subject) params.append('subject', subject)
    if (usePartCode && partCode) params.append('part_code', partCode)
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
      const records = [
        ...(jsonData.store || []),
        ...(jsonData.excel || [])
      ]
      setRows(records)
      setError(null)
    } catch (err) {
      setError(err.message)
      setRows([])
    }
  }

  return (
    <Box sx={{ mt: 2, background: 'linear-gradient(180deg,#ffffff,#f0f4fa)', p: 2, borderRadius: 2, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 2 }}>
        <FormControlLabel
          control={<Checkbox checked={useCustomer} onChange={(e) => setUseCustomer(e.target.checked)} />}
          label={
            <TextField
              label="Müşteri"
              size="small"
              value={customer}
              onChange={(e) => setCustomer(e.target.value)}
            />
          }
        />
        <FormControlLabel
          control={<Checkbox checked={useSubject} onChange={(e) => setUseSubject(e.target.checked)} />}
          label={
            <TextField
              label="Konu"
              size="small"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
            />
          }
        />
        <FormControlLabel
          control={<Checkbox checked={usePartCode} onChange={(e) => setUsePartCode(e.target.checked)} />}
          label={
            <TextField
              label="Parça Kodu"
              size="small"
              value={partCode}
              onChange={(e) => setPartCode(e.target.value)}
            />
          }
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
      {rows.length > 0 && (
        <Box sx={{ overflowX: 'auto' }}>
          <Table size="small" sx={{ mt: 2 }}>
            <TableHead>
              <TableRow>
                {Object.keys(rows[0]).map((col) => (
                  <TableCell key={col}>
                    <Tooltip title={col} placement="top">
                      <span
                        style={{
                          maxWidth: 120,
                          display: 'inline-block',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap'
                        }}
                      >
                        {col}
                      </span>
                    </Tooltip>
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((r, i) => (
                <TableRow key={i}>
                  {Object.keys(rows[0]).map((col) => (
                    <TableCell key={col}>{r[col]}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Box>
      )}
    </Box>
  )
}

export default ComplaintFetcher
