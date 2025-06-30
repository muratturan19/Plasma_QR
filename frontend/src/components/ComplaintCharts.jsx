import { useState } from 'react'
import Grid from '@mui/material/Grid'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Typography from '@mui/material/Typography'
import Slider from '@mui/material/Slider'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from 'recharts'

function ComplaintCharts({ form }) {
  const [monthRange, setMonthRange] = useState([0, 11])
  const [yearRange, setYearRange] = useState([2016, 2025])

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
  ]

  const monthlyData = months.map((m) => ({
    name: m,
    count: Math.floor(Math.random() * 15) + 5
  }))

  const filteredMonths = monthlyData.slice(monthRange[0], monthRange[1] + 1)

  const yearlyData = Array.from({ length: 10 }, (_, idx) => ({
    name: 2016 + idx,
    count: Math.floor(Math.random() * 200) + 50
  }))

  const filteredYears = yearlyData.filter(
    (d) => d.name >= yearRange[0] && d.name <= yearRange[1]
  )

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={6}>
        {form}
      </Grid>
      <Grid item xs={12} md={6}>
        <Grid container spacing={2} direction="column">
          <Grid item>
            <Card sx={{ backgroundColor: '#ccffcc' }}>
              <CardContent>
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
              </CardContent>
            </Card>
          </Grid>
          <Grid item>
            <Card sx={{ backgroundColor: '#ccffcc' }}>
              <CardContent>
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
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  )
}

export default ComplaintCharts
