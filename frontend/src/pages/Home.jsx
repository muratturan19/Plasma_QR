import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import AnalysisForm from '../components/AnalysisForm'
import Footer from '../components/Footer'

function Home() {
  const headingMarginTop = 3
  const headingMarginLeft = 2
  return (
    <>
      <Box
        sx={{
          width: '100%',
          maxWidth: 'none',
          minWidth: 1100,
          height: '100%',
          overflow: 'auto',
          margin: '0 auto',
          p: 3,
          boxSizing: 'border-box',
          minHeight: 700
        }}
      >
        <Box sx={{ mt: headingMarginTop, ml: headingMarginLeft }}>
          <Typography
            variant="h4"
            component="h1"
            gutterBottom
            sx={{ color: '#002855', fontFamily: 'Poppins, Inter, sans-serif' }}
          >
            Plasma QR
          </Typography>
        </Box>
        <AnalysisForm />
      </Box>
      <Footer />
    </>
  )
}

export default Home
