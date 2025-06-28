import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import AnalysisForm from '../components/AnalysisForm'
import ComplaintFetcher from '../components/ComplaintFetcher'
import Footer from '../components/Footer'

function Home() {
  return (
    <>
      <Container
        sx={{
          width: '100%',
          maxWidth: 'none',
          margin: '0 auto',
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
        <ComplaintFetcher />
      </Container>
      <Footer />
    </>
  )
}

export default Home
