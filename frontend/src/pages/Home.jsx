import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import AnalysisForm from '../components/AnalysisForm'
import Footer from '../components/Footer'

function Home() {
  return (
    <>
      <Container
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
        <Typography
          variant="h4"
          component="h1"
          gutterBottom
          sx={{ color: '#002855', fontFamily: 'Poppins, Inter, sans-serif' }}
        >
          Plasma QR
        </Typography>
        <AnalysisForm />
      </Container>
      <Footer />
    </>
  )
}

export default Home
