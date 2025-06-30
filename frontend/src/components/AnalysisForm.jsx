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
  MenuItem
} from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import LabelIcon from '@mui/icons-material/Label';
import QrCode2Icon from '@mui/icons-material/QrCode2';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from 'recharts';
const API_BASE = '/api';
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
const inputSx = {
  '& .MuiOutlinedInput-root': {
    '&:hover fieldset': { borderColor: 'primary.main' },
    '&.Mui-focused fieldset': { borderColor: 'primary.main' }
  }
};
function AnalysisForm() {
  const [customerOptions, setCustomerOptions] = useState([]);
  const [subjectOptions, setSubjectOptions] = useState([]);
  const [partCodeOptions, setPartCodeOptions] = useState([]);
  const [customer, setCustomer] = useState('');
  const [subject, setSubject] = useState('');
  const [partCode, setPartCode] = useState('');
  const [method, setMethod] = useState('');
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
  const handleAnalyze = () => {
    console.log({
      complaint,
      customer,
      subject,
      partCode,
      method,
      directives
    });
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
      setClaims(data);
      setClaimsError('');
    } catch (err) {
      setClaimsError(err.message);
      setClaims(null);
    }
  };
  return (
    <Card
      sx={{
        width: 1600,
        margin: '40px auto',
        minHeight: 650,
        p: 4,
        display: 'flex',
        flexDirection: 'row',
        boxShadow: 4,
        background: 'linear-gradient(180deg, #fff 0%, #f4f7fb 100%)'
      }}
    >
      {/* Sol Form Alanı */}
      <Box
        sx={{
          width: '68%',
          minWidth: 0,
          height: 540,
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
            mb: 2,
            height: '38%',
            minHeight: 120
          }}
        >
          {/* Şikayet Alanı */}
          <Box sx={{ width: '56%', minWidth: 0, height: '100%' }}>
            <TextField
              label="Şikayet (Complaint)"
              multiline
              minRows={6}
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
              gap: 1,
              justifyContent: 'space-between',
              height: '100%'
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
            {method && (
              <Alert severity="info" sx={{ mt: 1, fontSize: 15 }}>
                {GUIDE_TEXT[method]}
              </Alert>
            )}
          </Box>
        </Box>
        {/* Özel Talimatlar Alanı */}
        <Box
          sx={{
            width: '100%',
            mb: 2,
            height: '38%',
            minHeight: 90,
            borderRadius: 1,
            p: 1,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-start'
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
            gap: 2,
            flexWrap: 'wrap',
            alignItems: 'center',
            mb: 1
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
            gap: 2,
            mt: 'auto',
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
        {claimsError && (
          <Alert severity="error" sx={{ mt: 1 }}>
            {claimsError}
          </Alert>
        )}
        {claims && (
          <pre style={{ whiteSpace: 'pre-wrap', marginTop: '8px' }}>
            {JSON.stringify(claims, null, 2)}
          </pre>
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
