import React, { useState, useEffect } from 'react';
import {
  Card,
  Box,
  TextField,
  Button,
  Typography,
  Autocomplete,
  InputAdornment,
  Alert
} from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import LabelIcon from '@mui/icons-material/Label';
import QrCode2Icon from '@mui/icons-material/QrCode2';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';

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
      <Box
        sx={{
          width: '68%',
          minWidth: 0,
          height: 540,
          display: 'flex',
          flexDirection: 'column',
          pr: 3,
          background: 'rgba(33,150,243,0.08)',
          border: '2px dashed #2196f3',
          borderRadius: 2
        }}
      >
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'row',
            gap: 2,
            mb: 2,
            height: '38%',
            minHeight: 120
          }}
        >
          <Box sx={{ width: '56%', minWidth: 0 }}>
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
          <Box
            sx={{
              width: '44%',
              minWidth: 0,
              display: 'flex',
              flexDirection: 'column',
              gap: 1,
              justifyContent: 'space-between'
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
                  label="Müşteri"
                  sx={inputSx}
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

        <Box
          sx={{
            width: '100%',
            mb: 2,
            height: '38%',
            minHeight: 90,
            background: 'rgba(33,150,243,0.07)',
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
          <Button variant="outlined" color="primary">
            ŞİKAYETLERİ GETİR
          </Button>
        </Box>
      </Box>

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
          background: 'rgba(76,175,80,0.07)',
          border: '2px dashed #4caf50',
          borderRadius: 2
        }}
      >
        <Box
          sx={{
            width: '100%',
            height: '49%',
            bgcolor: '#fff',
            borderRadius: 2,
            mb: 1,
            p: 2,
            display: 'flex',
            alignItems: 'flex-start'
          }}
        >
          <Typography sx={{ fontWeight: 'bold' }}>2025 Aylık Şikayet</Typography>
        </Box>
        <Box
          sx={{
            width: '100%',
            height: '49%',
            bgcolor: '#fff',
            borderRadius: 2,
            p: 2,
            display: 'flex',
            alignItems: 'flex-start'
          }}
        >
          <Typography sx={{ fontWeight: 'bold' }}>Son 10 Yıl Şikayet</Typography>
        </Box>
      </Box>
    </Card>
  );
}

export default AnalysisForm;
