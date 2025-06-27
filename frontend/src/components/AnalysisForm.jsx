import { useState } from 'react'
import Box from '@mui/material/Box'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Autocomplete from '@mui/material/Autocomplete'
import Alert from '@mui/material/Alert'
import Typography from '@mui/material/Typography'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import { API_BASE } from '../api'

const METHODS = ['8D', 'A3', 'Ishikawa', '5N1K', 'DMAIC']

const GUIDE_TEXT = {
  '8D':
    '8D (Eight Disciplines) metodu, ürün ve süreç kaynaklı problemleri sistematik şekilde çözmek için geliştirilmiş etkili bir problem çözme tekniğidir.',
  A3:
    'A3 Problem Solving, problemi sistematik biçimde tanımlamak, analiz etmek ve çözüm geliştirmek için kullanılan yalın düşünce temelli bir yaklaşımdır.',
  Ishikawa:
    'Ishikawa (Balık Kılçığı) Diyagramı, problemin kök nedenlerini sistematik olarak analiz etmeye yarayan neden-sonuç diyagramıdır.',
  '5N1K':
    '5N1K (5W1H) yöntemi, bir problemi tüm yönleriyle incelemek için kullanılan klasik sorgulama metodudur.',
  DMAIC:
    'DMAIC, süreç iyileştirme için kullanılan sistematik bir problem çözme metodudur.'
}

function AnalysisForm() {
  const [complaint, setComplaint] = useState('')
  const [customer, setCustomer] = useState('')
  const [subject, setSubject] = useState('')
  const [partCode, setPartCode] = useState('')
  const [method, setMethod] = useState(null)
  const [directives, setDirectives] = useState('')
  const [error, setError] = useState('')
  const [finalText, setFinalText] = useState('')
  const [downloads, setDownloads] = useState(null)

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!complaint || !customer || !subject || !partCode || !method) {
      setError('All fields are required.')
      return
    }
    setError('')
    setFinalText('')
    setDownloads(null)
    try {
      const details = { complaint, customer, subject, part_code: partCode }
      const analyzeBody = { details, guideline: { method }, directives }
      const analyzeRes = await fetch(`${API_BASE}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(analyzeBody)
      })
      if (!analyzeRes.ok) {
        throw new Error(`HTTP ${analyzeRes.status}`)
      }
      const analysis = await analyzeRes.json()
      const reviewRes = await fetch(`${API_BASE}/review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: JSON.stringify(analysis), context: { method } })
      })
      if (!reviewRes.ok) {
        throw new Error(`HTTP ${reviewRes.status}`)
      }
      const { result } = await reviewRes.json()
      analysis.full_report = { response: result }
      const reportRes = await fetch(`${API_BASE}/report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          analysis,
          complaint_info: { customer, subject, part_code: partCode },
          output_dir: '.'
        })
      })
      if (!reportRes.ok) {
        throw new Error(`HTTP ${reportRes.status}`)
      }
      const downloadsData = await reportRes.json()
      setFinalText(result)
      setDownloads(downloadsData)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <Card sx={{ mt: 2 }}>
      <CardContent>
        <Box component="form" onSubmit={handleSubmit} noValidate>
      <TextField
        label="Complaint"
        value={complaint}
        onChange={(e) => setComplaint(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Customer"
        value={customer}
        onChange={(e) => setCustomer(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Subject"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Part Code"
        value={partCode}
        onChange={(e) => setPartCode(e.target.value)}
        fullWidth
        margin="normal"
      />
      <Autocomplete
        options={METHODS}
        value={method}
        onChange={(event, newValue) => setMethod(newValue)}
        renderInput={(params) => <TextField {...params} label="Method" margin="normal" />}
      />
      {method && (
        <Alert severity="info" sx={{ mt: 1 }} data-testid="guide-text">
          {GUIDE_TEXT[method]}
        </Alert>
      )}
      <TextField
        label="Directives"
        value={directives}
        onChange={(e) => setDirectives(e.target.value)}
        fullWidth
        margin="normal"
        multiline
        minRows={3}
      />
      <Button type="submit" variant="contained" sx={{ mt: 2 }}>
        Analyze
      </Button>
      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
      {finalText && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="h6">Final Report</Typography>
          <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
            {finalText}
          </Typography>
          {downloads && (
            <Box sx={{ mt: 1 }}>
              <a href={downloads.pdf} download>
                Download PDF
              </a>{' '}
              |{' '}
              <a href={downloads.excel} download>
                Download Excel
              </a>
            </Box>
          )}
        </Box>
      )}
        </Box>
      </CardContent>
    </Card>
  )
}

export default AnalysisForm
