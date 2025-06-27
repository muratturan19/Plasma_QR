import { useState } from 'react'
import Box from '@mui/material/Box'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Autocomplete from '@mui/material/Autocomplete'
import Alert from '@mui/material/Alert'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { DatePicker } from '@mui/x-date-pickers/DatePicker'
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'

function AnalysisForm() {
  const [complaint, setComplaint] = useState('')
  const [guideline, setGuideline] = useState(null)
  const [date, setDate] = useState(null)
  const [error, setError] = useState('')
  const [results, setResults] = useState(null)

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!complaint || !guideline || !date) {
      setError('All fields are required.')
      return
    }
    setError('')
    setResults(null)
    const payload = {
      details: { complaint, date: date.toISOString() },
      guideline: { method: guideline },
      directives: ''
    }
    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err.message)
    }
  }

  const rows = results ? Object.entries(results) : []

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 2 }}>
        <TextField
          label="Complaint"
          value={complaint}
          onChange={(e) => setComplaint(e.target.value)}
          fullWidth
          margin="normal"
          helperText="Enter complaint details"
        />
        <Autocomplete
          options={['8D', 'QR', 'Other']}
          value={guideline}
          onChange={(event, newValue) => setGuideline(newValue)}
          renderInput={(params) => (
            <TextField {...params} label="Guideline" margin="normal" helperText="Select analysis guideline" />
          )}
        />
        <DatePicker
          label="Date"
          value={date}
          onChange={(newValue) => setDate(newValue)}
          renderInput={(params) => <TextField {...params} margin="normal" helperText="Choose report date" />}
        />
        <Button type="submit" variant="contained" sx={{ mt: 2 }}>
          Analyze
        </Button>
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
        {rows.length > 0 && (
          <Table sx={{ mt: 2 }} size="small">
            <TableHead>
              <TableRow>
                <TableCell>Key</TableCell>
                <TableCell>Value</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map(([key, value]) => (
                <TableRow key={key}>
                  <TableCell>{key}</TableCell>
                  <TableCell>{String(value)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </Box>
    </LocalizationProvider>
  )
}

export default AnalysisForm
