import { useState, useEffect } from 'react'
import Box from '@mui/material/Box'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Autocomplete from '@mui/material/Autocomplete'
import Alert from '@mui/material/Alert'
import Snackbar from '@mui/material/Snackbar'
import CircularProgress from '@mui/material/CircularProgress'
import Typography from '@mui/material/Typography'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Grow from '@mui/material/Grow'
import Grid from '@mui/material/Grid'
import InputAdornment from '@mui/material/InputAdornment'
import PersonIcon from '@mui/icons-material/Person'
import LabelIcon from '@mui/icons-material/Label'
import QrCode2Icon from '@mui/icons-material/QrCode2'
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf'
import FileDownloadIcon from '@mui/icons-material/FileDownload'
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

const inputSx = {
  transition: 'border-color 0.3s',
  '& .MuiOutlinedInput-root': {
    '&:hover fieldset': { borderColor: 'primary.main' },
    '&.Mui-focused fieldset': { borderColor: 'primary.main' }
  },
  '& .MuiSvgIcon-root': {
    transition: 'color 0.3s'
  },
  '& .MuiOutlinedInput-root.Mui-focused .MuiSvgIcon-root': {
    color: 'primary.main'
  }
}

function AnalysisForm() {
  const [complaint, setComplaint] = useState('')
  const [customer, setCustomer] = useState('')
  const [subject, setSubject] = useState('')
  const [partCode, setPartCode] = useState('')
  const [method, setMethod] = useState(null)
  const [directives, setDirectives] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)
  const [finalText, setFinalText] = useState('')
  const [downloads, setDownloads] = useState(null)
  const [customerOptions, setCustomerOptions] = useState([])
  const [subjectOptions, setSubjectOptions] = useState([])
  const [partCodeOptions, setPartCodeOptions] = useState([])

  useEffect(() => {
    const fetchOptions = async (field, setter) => {
      try {
        const res = await fetch(`${API_BASE}/options/${field}`)
        if (res.ok) {
          const data = await res.json()
          setter(data.values || [])
        }
      } catch {
        // ignore errors
      }
    }
    fetchOptions('customer', setCustomerOptions)
    fetchOptions('subject', setSubjectOptions)
    fetchOptions('part_code', setPartCodeOptions)
  }, [])

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!complaint || !customer || !subject || !partCode || !method) {
      setError('All fields are required.')
      return
    }
    setError('')
    setSuccess('')
    setLoading(true)
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
      setSuccess('Report created successfully.')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card
      sx={{
        mt: 2,
        background: 'linear-gradient(180deg, #ffffff 0%, #f0f4fa 100%)',
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
      }}
    >
      <CardContent>
        <Box component="form" onSubmit={handleSubmit} noValidate>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <TextField
                label="Complaint"
                value={complaint}
                onChange={(e) => setComplaint(e.target.value)}
                fullWidth
                margin="normal"
                multiline
                minRows={5}
                sx={inputSx}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <Autocomplete
                freeSolo
                options={customerOptions}
                inputValue={customer}
                onInputChange={(e, v) => setCustomer(v)}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Customer"
                    margin="normal"
                    sx={inputSx}
                    InputProps={{
                      ...params.InputProps,
                      startAdornment: (
                        <InputAdornment position="start">
                          <PersonIcon />
                        </InputAdornment>
                      )
                    }}
                    inputProps={{
                      ...params.inputProps,
                      'data-testid': 'customer-input'
                    }}
                  />
                )}
              />
              <Autocomplete
                freeSolo
                options={subjectOptions}
                inputValue={subject}
                onInputChange={(e, v) => setSubject(v)}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Subject"
                    margin="normal"
                    sx={inputSx}
                    InputProps={{
                      ...params.InputProps,
                      startAdornment: (
                        <InputAdornment position="start">
                          <LabelIcon />
                        </InputAdornment>
                      )
                    }}
                    inputProps={{
                      ...params.inputProps,
                      'data-testid': 'subject-input'
                    }}
                  />
                )}
              />
              <Autocomplete
                freeSolo
                options={partCodeOptions}
                inputValue={partCode}
                onInputChange={(e, v) => setPartCode(v)}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Part Code"
                    margin="normal"
                    sx={inputSx}
                    InputProps={{
                      ...params.InputProps,
                      startAdornment: (
                        <InputAdornment position="start">
                          <QrCode2Icon />
                        </InputAdornment>
                      )
                    }}
                    inputProps={{
                      ...params.inputProps,
                      'data-testid': 'partcode-input'
                    }}
                  />
                )}
              />
              <Autocomplete
                options={METHODS}
                value={method}
                onChange={(event, newValue) => setMethod(newValue)}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Method"
                    margin="normal"
                    sx={inputSx}
                    InputProps={{
                      ...params.InputProps,
                      startAdornment: (
                        <InputAdornment position="start">
                          <ArrowDropDownIcon />
                        </InputAdornment>
                      )
                    }}
                    inputProps={{
                      ...params.inputProps,
                      'data-testid': 'method-input'
                    }}
                  />
                )}
              />
              {method && (
                <Alert severity="info" sx={{ mt: 1 }} data-testid="guide-text">
                  {GUIDE_TEXT[method]}
                </Alert>
              )}
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                label="Directives"
                value={directives}
                onChange={(e) => setDirectives(e.target.value)}
                fullWidth
                margin="normal"
                multiline
                minRows={3}
                sx={inputSx}
              />
            </Grid>
          </Grid>
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
      <Button
        type="submit"
        variant="contained"
        startIcon={<QrCode2Icon />}
        sx={{ mt: 2, px: 4, py: 1.5, fontSize: '1rem', transition: 'transform 0.2s', '&:hover': { transform: 'translateY(-2px)' } }}
      >
        Analyze
      </Button>
      {loading && (
        <CircularProgress sx={{ mt: 2 }} data-testid="loading-indicator" />
      )}
      <Snackbar
        open={Boolean(error)}
        autoHideDuration={6000}
        onClose={() => setError('')}
        message={error}
      />
      <Snackbar
        open={Boolean(success)}
        autoHideDuration={6000}
        onClose={() => setSuccess('')}
        message={success}
      />
      {finalText && (
        <Box sx={{ mt: 2 }}>
          <Grow in={Boolean(success)}>
            <Box display="flex" justifyContent="center" sx={{ mb: 1 }}>
              <CheckCircleIcon
                color="success"
                fontSize="large"
                data-testid="CheckCircleIcon"
              />
            </Box>
          </Grow>
          <Typography variant="h6">Final Report</Typography>
          <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
            {finalText}
          </Typography>
          {downloads && (
            <Box sx={{ mt: 1 }}>
              <Button
                component="a"
                href={downloads.pdf}
                download
                variant="outlined"
                startIcon={<PictureAsPdfIcon />}
                sx={{ mr: 1, px: 3, py: 1 }}
              >
                PDF
              </Button>
              <Button
                component="a"
                href={downloads.excel}
                download
                variant="outlined"
                startIcon={<FileDownloadIcon />}
                sx={{ px: 3, py: 1 }}
              >
                Excel
              </Button>
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
