import { useState } from 'react'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import FormControlLabel from '@mui/material/FormControlLabel'
import Checkbox from '@mui/material/Checkbox'
import MenuItem from '@mui/material/MenuItem'
import Select from '@mui/material/Select'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Alert from '@mui/material/Alert'

function ComplaintQuery() {
  const [complaint, setComplaint] = useState('')
  const [customer, setCustomer] = useState('')
  const [subject, setSubject] = useState('')
  const [partCode, setPartCode] = useState('')
  const [useComplaint, setUseComplaint] = useState(false)
  const [useCustomer, setUseCustomer] = useState(false)
  const [useSubject, setUseSubject] = useState(false)
  const [usePartCode, setUsePartCode] = useState(false)
  const [year, setYear] = useState('')
  const [rows, setRows] = useState([])
  const [error, setError] = useState('')

  const handleQuery = async () => {
    const params = new URLSearchParams()
    if (useComplaint && complaint) params.append('complaint', complaint)
    if (useCustomer && customer) params.append('customer', customer)
    if (useSubject && subject) params.append('subject', subject)
    if (usePartCode && partCode) params.append('part_code', partCode)
    if (year) params.append('year', year)
    try {
      const res = await fetch(`/complaints?${params.toString()}`)
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`)
      }
      const data = await res.json()
      const records = [...(data.store || []), ...(data.excel || [])]
      setRows(records)
      setError('')
    } catch (err) {
      setError(err.message)
      setRows([])
    }
  }

  const currentYear = new Date().getFullYear()
  const years = Array.from({ length: 10 }, (_, i) => `${currentYear - i}`)

  return (
    <Box sx={{ mt: 4 }}>
      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
        <FormControlLabel
          control={<Checkbox checked={useComplaint} onChange={(e) => setUseComplaint(e.target.checked)} />}
          label={
            <TextField label="Complaint" value={complaint} onChange={(e) => setComplaint(e.target.value)} />
          }
        />
        <FormControlLabel
          control={<Checkbox checked={useCustomer} onChange={(e) => setUseCustomer(e.target.checked)} />}
          label={<TextField label="Customer" value={customer} onChange={(e) => setCustomer(e.target.value)} />}
        />
        <FormControlLabel
          control={<Checkbox checked={useSubject} onChange={(e) => setUseSubject(e.target.checked)} />}
          label={<TextField label="Subject" value={subject} onChange={(e) => setSubject(e.target.value)} />}
        />
        <FormControlLabel
          control={<Checkbox checked={usePartCode} onChange={(e) => setUsePartCode(e.target.checked)} />}
          label={<TextField label="Part Code" value={partCode} onChange={(e) => setPartCode(e.target.value)} />}
        />
        <Select
          value={year}
          onChange={(e) => setYear(e.target.value)}
          displayEmpty
          data-testid="year-select"
        >
          <MenuItem value="">
            <em>All Years</em>
          </MenuItem>
          {years.map((y) => (
            <MenuItem key={y} value={y}>
              {y}
            </MenuItem>
          ))}
        </Select>
        <Button variant="outlined" onClick={handleQuery} sx={{ alignSelf: 'center' }}>
          Query
        </Button>
      </Box>
      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
      {rows.length > 0 && (
        <Table sx={{ mt: 2 }} size="small">
          <TableHead>
            <TableRow>
              <TableCell>Complaint</TableCell>
              <TableCell>Customer</TableCell>
              <TableCell>Subject</TableCell>
              <TableCell>Part Code</TableCell>
              <TableCell>Date</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((r, i) => (
              <TableRow key={i}>
                <TableCell>{r.complaint}</TableCell>
                <TableCell>{r.customer}</TableCell>
                <TableCell>{r.subject}</TableCell>
                <TableCell>{r.part_code}</TableCell>
                <TableCell>{r.date}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </Box>
  )
}

export default ComplaintQuery
