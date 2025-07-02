import React, { useState, useEffect } from 'react';
import {
  Card,
  Box,
  TextField,
  Button,
  Typography,
  Autocomplete,
  InputAdornment,
  Alert,
  Slider,
  FormControlLabel,
  Checkbox,
  Select,
  MenuItem,
  CircularProgress
} from '@mui/material';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import TableBody from '@mui/material/TableBody';
import TableRow from '@mui/material/TableRow';
import TableCell from '@mui/material/TableCell';
import MuiTooltip from '@mui/material/Tooltip';
import PersonIcon from '@mui/icons-material/Person';
import LabelIcon from '@mui/icons-material/Label';
import QrCode2Icon from '@mui/icons-material/QrCode2';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import DescriptionIcon from '@mui/icons-material/Description';
import FishboneDiagram from './FishboneDiagram';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from 'recharts';
import { API_BASE } from '../api';
const METHODS = ['8D', 'A3', 'Ishikawa', '5N1K', 'DMAIC'];
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
};
const FISHBONE_DATA = {
  Problem: {
    Method: [],
    Material: [],
    Machine: [],
    Measurement: [],
    Man: [],
    Environment: []
  }
};
const inputSx = {
  '& .MuiOutlinedInput-root': {
    '&:hover fieldset': { borderColor: 'primary.main' },
    '&.Mui-focused fieldset': { borderColor: 'primary.main' }
  }
};
function AnalysisForm({
  instructionsBoxProps = {},
  methodBoxProps = {},
  filterBoxProps = {},
  initialMethod = ''
}) {
  const [customerOptions, setCustomerOptions] = useState([]);
  const [subjectOptions, setSubjectOptions] = useState([]);
  const [partCodeOptions, setPartCodeOptions] = useState([]);
  const [customer, setCustomer] = useState('');
  const [subject, setSubject] = useState('');
  const [partCode, setPartCode] = useState('');
  const [method, setMethod] = useState(initialMethod);
  const [complaint, setComplaint] = useState('');
  const [directives, setDirectives] = useState('');
  const [useCustomerFilter, setUseCustomerFilter] = useState(false);
  const [usePartCodeFilter, setUsePartCodeFilter] = useState(false);
  const [useSubjectFilter, setUseSubjectFilter] = useState(false);
  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: 10 }, (_, i) => `${currentYear - i}`);
  const [selectedYear, setSelectedYear] = useState('');
  const [claims, setClaims] = useState(null);
  const [claimsError, setClaimsError] = useState('');
  const [error, setError] = useState('');
  const [reviewText, setReviewText] = useState('');
  const [analysisText, setAnalysisText] = useState('');
  const [rawAnalysis, setRawAnalysis] = useState('');
  const [reportPaths, setReportPaths] = useState(null);
  const [loading, setLoading] = useState(false);
  const [rawClaims, setRawClaims] = useState('');
  const [monthRange, setMonthRange] = useState([0, 11]);
  const [yearRange, setYearRange] = useState([2016, 2025]);
  const months = [
    'Oca',
    'Şub',
    'Mar',
    'Nis',
    'May',
    'Haz',
    'Tem',
    'Ağu',
    'Eyl',
    'Eki',
    'Kas',
    'Ara'
  ];
  const monthlyData = months.map((m) => ({
    name: m,
    count: Math.floor(Math.random() * 15) + 5
  }));
  const filteredMonths = monthlyData.slice(monthRange[0], monthRange[1] + 1);
  const yearlyData = Array.from({ length: 10 }, (_, idx) => ({
    name: 2016 + idx,
    count: Math.floor(Math.random() * 200) + 50
  }));
  const filteredYears = yearlyData.filter(
    (d) => d.name >= yearRange[0] && d.name <= yearRange[1]
  );
  useEffect(() => {
    const fetchOptions = async (field, setter) => {
      try {
        const res = await fetch(`${API_BASE}/options/${field}`);
        if (res.ok) {
          const data = await res.json();
          setter(data.values || data || []);
        }
      } catch {
        setter([]);
      }
    };
    fetchOptions('customer', setCustomerOptions);
    fetchOptions('subject', setSubjectOptions);
    fetchOptions('part_code', setPartCodeOptions);
  }, []);
  const handleAnalyze = async () => {
    // DEBUG: API_BASE kontrolü
    console.log('API_BASE:', API_BASE);
    setError('');
    setLoading(true);
    setRawAnalysis('');
    setAnalysisText('');
    setReviewText('');
    setReportPaths(null);
    const details = {
      complaint,
      customer,
      subject,
      part_code: partCode
    };
    try {
      const guideRes = await fetch(`${API_BASE}/guide/${method}`);
      if (!guideRes.ok) {
        setError(await guideRes.text());
        return;
      }
      const guideline = await guideRes.json();

      const analyzeRes = await fetch(`${API_BASE}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ details, guideline, directives })
      });
      if (!analyzeRes.ok) {
        setError(await analyzeRes.text());
        return;
      }
      const analysis = await analyzeRes.json();
      let text = analysis.full_text || analysis.analysisText;
      if (!text) {
        const steps = Object.values(analysis)
          .map((s) => (s && typeof s === 'object' ? s.response : undefined))
          .filter(Boolean);
        text = steps.join('\n\n');
      }
      if (!text) {
        setRawAnalysis(JSON.stringify(analysis, null, 2));
        setError('Sunucudan beklenmeyen boş yanıt alındı');
        return;
      }
      setRawAnalysis('');
      setAnalysisText(text);

      const reviewRes = await fetch(`${API_BASE}/review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text || JSON.stringify(analysis) })
      });
      if (!reviewRes.ok) {
        setError(await reviewRes.text());
        return;
      }
      const reviewData = await reviewRes.json();
      if (!reviewData?.result) {
        setError('Sunucudan beklenmeyen boş yanıt alındı');
        return;
      }
      setReviewText(reviewData.result);

      // DEBUG: Report kısmı
      console.log('Starting report generation...');
      const reportRes = await fetch(`${API_BASE}/report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          analysis,
          complaint_info: details,
          output_dir: '.'
        })
      });

      console.log('Report response status:', reportRes.status);
      console.log('Report response ok:', reportRes.ok);

      if (!reportRes.ok) {
        const errorText = await reportRes.text();
        console.log('Report error:', errorText);
        setError(errorText);
        setReportPaths(null);
        return;
      } else {
        const paths = await reportRes.json();
        console.log('Backend response paths:', paths);
        console.log('API_BASE value:', API_BASE);

        if (!paths?.pdf) {
          console.log('No PDF path in response');
          setError('Sunucudan beklenmeyen boş yanıt alındı');
        } else {
          const finalReportPaths = {
            pdf: `${API_BASE}${paths.pdf}`,
            excel: `${API_BASE}${paths.excel}`,
          };
          console.log('Final report URLs:', finalReportPaths);
          console.log('Setting reportPaths state...');
          setReportPaths(finalReportPaths);
          console.log('reportPaths state set successfully');
        }
      }
    } catch (err) {
      console.error(err);
      setError(err.message || 'Bir hata oluştu');
    } finally {
      setLoading(false);
    }
  };
  const handleFetchClaims = async () => {
    const params = new URLSearchParams();
    if (useCustomerFilter && customer) params.append('customer', customer);
    if (useSubjectFilter && subject) params.append('subject', subject);
    if (usePartCodeFilter && partCode) params.append('part_code', partCode);
    if (selectedYear) params.append('start_year', selectedYear);
    const url =
      params.toString().length > 0
        ? `${API_BASE}/complaints?${params.toString()}`
        : `${API_BASE}/complaints`;
    try {
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`HTTP error ${res.status}`);
      }
      const data = await res.json();
      const results = data.results || data;
      if (
        Array.isArray(results) ||
        results.store !== undefined ||
        results.excel !== undefined
      ) {
        const records = Array.isArray(results)
          ? results
          : [...(results.store || []), ...(results.excel || [])];
        console.log('claims data', records);
        setRawClaims('');
        setClaims(records);
        setClaimsError('');
      } else {
        setClaims([]);
        const raw = JSON.stringify(data, null, 2);
        console.log('raw claims', raw);
        setRawClaims(raw);
        setClaimsError('');
      }
    } catch (err) {
      setClaimsError(err.message);
      setClaims(null);
      setRawClaims('');
    }
  };
  console.log('analysisText:', analysisText);
  console.log('reviewText:', reviewText);
  console.log('reportPaths:', reportPaths);
  return (
    <Card
      sx={{
        width: 1600,
        margin: '40px auto',
        minHeight: 700,
        p: 4,
        display: 'flex',
        flexDirection: 'row',
        boxShadow: 4,
        background: 'linear-gradient(180deg, #fff 0%, #f4f7fb 100%)',
        position: 'relative',
        overflowY: 'auto'
      }}
    >
      {/* Sol Form Alanı */}
      <Box
        sx={{
          width: '68%',
          minWidth: 0,
          height: { xs: 'auto', md: 540 },
          display: 'flex',
          flexDirection: 'column',
          pr: 3,
          borderRadius: 2
        }}
      >
        {/* Şikayet ve Müşteri Bilgileri */}
        <Box
          sx={{
            width: '100%',
            display: 'flex',
            flexDirection: 'row',
            gap: 2,
            mb: 16,
            height: 'auto',
            minHeight: 120
          }}
        >
          {/* Şikayet Alanı */}
          <Box sx={{ width: '56%', minWidth: 0, height: '100%' }}>
            <TextField
              label="Şikayet (Complaint)"
              multiline
              minRows={10}
              fullWidth
              value={complaint}
              onChange={(e) => setComplaint(e.target.value)}
              sx={{ height: '100%' }}
            />
          </Box>
          {/* Müşteri/Kod/Metot Alanı */}
          <Box
            sx={{
              width: '44%',
              minWidth: 0,
              display: 'flex',
              flexDirection: 'column',
              gap: 2,
              justifyContent: 'flex-start',
              height: '100%',
              ...methodBoxProps
            }}
          >
            <Autocomplete
              fullWidth
              freeSolo
              options={customerOptions}
              inputValue={customer}
              onInputChange={(e, v) => setCustomer(v)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Müşteri Adı"
                  sx={inputSx}
                  inputProps={{
                    ...params.inputProps,
                    'data-testid': 'customer-input',
                    'aria-label': 'customer-input'
                  }}
                  InputProps={{
                    ...params.InputProps,
                    startAdornment: (
                      <InputAdornment position="start">
                        <PersonIcon />
                      </InputAdornment>
                    )
                  }}
                />
              )}
            />
            <Autocomplete
              fullWidth
              freeSolo
              options={subjectOptions}
              inputValue={subject}
              onInputChange={(e, v) => setSubject(v)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Konu"
                  sx={inputSx}
                  InputProps={{
                    ...params.InputProps,
                    startAdornment: (
                      <InputAdornment position="start">
                        <LabelIcon />
                      </InputAdornment>
                    )
                  }}
                />
              )}
            />
            <Autocomplete
              fullWidth
              freeSolo
              options={partCodeOptions}
              inputValue={partCode}
              onInputChange={(e, v) => setPartCode(v)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Parça Kodu"
                  sx={inputSx}
                  InputProps={{
                    ...params.InputProps,
                    startAdornment: (
                      <InputAdornment position="start">
                        <QrCode2Icon />
                      </InputAdornment>
                    )
                  }}
                />
              )}
            />
            <Autocomplete
              fullWidth
              options={METHODS}
              value={method}
              onChange={(event, newValue) => setMethod(newValue)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Metot"
                  sx={inputSx}
                  InputProps={{
                    ...params.InputProps,
                    startAdornment: (
                      <InputAdornment position="start">
                        <ArrowDropDownIcon />
                      </InputAdornment>
                    )
                  }}
                />
              )}
            />
            {method === 'Ishikawa' && (
              <Box sx={{ mt: 2 }}>
                <FishboneDiagram data={FISHBONE_DATA} />
              </Box>
            )}
          </Box>
        </Box>
        {/* Özel Talimatlar Alanı */}
        <Box
          sx={{
            width: '100%',
            mt: 6,
            height: { xs: 'auto', md: '38%' },
            minHeight: 90,
            borderRadius: 1,
            p: 1,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-start',
            ...instructionsBoxProps
          }}
        >
          <Typography sx={{ fontWeight: 'bold', mb: 1 }}>Özel Talimatlar</Typography>
          <TextField
            multiline
            minRows={3}
            fullWidth
            value={directives}
            onChange={(e) => setDirectives(e.target.value)}
            sx={{ height: '100%' }}
          />
        </Box>
        {/* Filtreler */}
        <Box
          sx={{
            width: '100%',
            display: 'flex',
			mt: 12,
            gap: 16,
            flexWrap: 'wrap',
            alignItems: 'center',
            mb: 1,
            ...filterBoxProps
          }}
        >
          <FormControlLabel
            control={
              <Checkbox
                checked={useCustomerFilter}
                onChange={(e) => setUseCustomerFilter(e.target.checked)}
              />
            }
            label="Müşteri"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={usePartCodeFilter}
                onChange={(e) => setUsePartCodeFilter(e.target.checked)}
              />
            }
            label="Parça Kodu"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={useSubjectFilter}
                onChange={(e) => setUseSubjectFilter(e.target.checked)}
              />
            }
            label="Konu"
          />
          <Select
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            displayEmpty
            size="small"
            sx={{ minWidth: 80 }}
          >
            <MenuItem value="">
              <em>Yıl</em>
            </MenuItem>
            {years.map((y) => (
              <MenuItem key={y} value={y}>
                {y}
              </MenuItem>
            ))}
          </Select>
        </Box>
        {/* Buton Alanı */}
        <Box
          sx={{
            width: '100%',
            display: 'flex',
            gap: 8,
            mt: 'auto',
			mb: 14,
            height: '24%',
            minHeight: 60,
            alignItems: 'flex-end'
          }}
        >
          <Button variant="contained" color="primary" onClick={handleAnalyze}>
            ANALİZ ET
          </Button>
          <Button variant="outlined" color="primary" onClick={handleFetchClaims}>
            Şikayetleri Getir
          </Button>
        </Box>
        {method && (
          <Alert severity="info" sx={{ mt: 2, mb: 2, fontSize: 15 }}>
            {GUIDE_TEXT[method]}
          </Alert>
        )}
        {claimsError && (
          <Alert severity="error" sx={{ mt: 1 }}>
            {claimsError}
          </Alert>
        )}
        {claims && claims.length > 0 && (
          <Table size="small" sx={{ mt: 2 }}>
            <TableHead>
              <TableRow>
                <TableCell>Tarih</TableCell>
                <TableCell>Müşteri</TableCell>
                <TableCell>Şikayet</TableCell>
                <TableCell>Konu</TableCell>
                <TableCell>Parça Kodu</TableCell>
                <TableCell>Açıklama</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {claims.map((c, i) => (
                <TableRow key={i}>
                  <TableCell>
                    {new Date(c.date).toLocaleDateString('tr-TR', {
                      day: '2-digit',
                      month: 'long',
                      year: 'numeric',
                    })}
                  </TableCell>
                  <TableCell>{c.customer}</TableCell>
                  <TableCell>
                    <MuiTooltip title={c.complaint || ''}>
                      <span
                        style={{
                          maxWidth: 150,
                          display: 'inline-block',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                        }}
                      >
                        {c.complaint}
                      </span>
                    </MuiTooltip>
                  </TableCell>
                  <TableCell>{c.subject}</TableCell>
                  <TableCell>{c.part_code}</TableCell>
                  <TableCell>
                    <MuiTooltip title={c.description || ''}>
                      <span
                        style={{
                          maxWidth: 150,
                          display: 'inline-block',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                        }}
                      >
                        {c.description}
                      </span>
                    </MuiTooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
        {claims && claims.length === 0 && (
          <Typography sx={{ mt: 2 }}>Şikayet bulunamadı</Typography>
        )}
        {rawClaims && console.log('raw claims', rawClaims)}
        {loading && (
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: 'rgba(255,255,255,0.6)',
              zIndex: 2
            }}
          >
            <CircularProgress data-testid="loading-indicator" />
          </Box>
        )}
        {error && (
          <Alert severity="error" sx={{ mt: 1 }}>
            {error}
          </Alert>
        )}
        {rawAnalysis && (
          <pre
            data-testid="raw-analysis"
            style={{ whiteSpace: 'pre-wrap', marginTop: '8px' }}
          >
            {rawAnalysis}
          </pre>
        )}
        {analysisText && (
          <Box sx={{ mt: 2 }}>
            <Card variant="outlined" sx={{ p: 2, backgroundColor: '#f9f9f9' }}>
              <Typography data-testid="analysis-text" sx={{ whiteSpace: 'pre-line' }}>
                {analysisText}
              </Typography>
            </Card>
          </Box>
        )}
        {reviewText && (
          <Box sx={{ mt: 2 }}>
            <Card variant="outlined" sx={{ p: 2, backgroundColor: '#f9f9f9' }}>
              <Typography data-testid="review-text" sx={{ whiteSpace: 'pre-line' }}>
                {reviewText}
              </Typography>

              {reportPaths && (
                <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    href={reportPaths.pdf}
                    target="_blank"
                    rel="noopener noreferrer"
                    download
                    startIcon={<PictureAsPdfIcon />}
                  >
                    PDF indir
                  </Button>
                  <Button
                    variant="contained"
                    color="success"
                    href={reportPaths.excel}
                    target="_blank"
                    rel="noopener noreferrer"
                    download
                    startIcon={<DescriptionIcon />}
                  >
                    Excel indir
                  </Button>
                </Box>
              )}
            </Card>
          </Box>
        )}
      </Box>
      {/* Grafikler Alanı */}
      <Box
        sx={{
          width: '32%',
          minWidth: 0,
          height: 540,
          display: 'flex',
          flexDirection: 'column',
          gap: 3,
          alignItems: 'stretch',
          pl: 3,
          borderRadius: 2
        }}
      >
        <Box
          sx={{
            width: '100%',
            height: '49%',
            borderRadius: 2,
            mb: 1,
            p: 2,
            display: 'flex',
            flexDirection: 'column'
          }}
        >
          <Typography variant="h6" gutterBottom>
            2025 Aylık Şikayet
          </Typography>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={filteredMonths}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#2196f3" />
            </BarChart>
          </ResponsiveContainer>
          <Slider
            value={monthRange}
            min={0}
            max={11}
            step={1}
            marks={[
              { value: 0, label: 'Oca' },
              { value: 11, label: 'Ara' }
            ]}
            valueLabelDisplay="auto"
            onChange={(_, v) => setMonthRange(v)}
          />
        </Box>
        <Box
          sx={{
            width: '100%',
            height: '49%',
            borderRadius: 2,
            p: 2,
            display: 'flex',
            flexDirection: 'column'
          }}
        >
          <Typography variant="h6" gutterBottom>
            Son 10 Yıl Şikayet
          </Typography>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={filteredYears}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#90caf9" />
            </BarChart>
          </ResponsiveContainer>
          <Slider
            value={yearRange}
            min={2016}
            max={2025}
            step={1}
            marks={[
              { value: 2016, label: 2016 },
              { value: 2025, label: 2025 }
            ]}
            valueLabelDisplay="auto"
            onChange={(_, v) => setYearRange(v)}
          />
        </Box>
      </Box>
    </Card>
  );
}
export default AnalysisForm;
