import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import AnalysisForm from '../components/AnalysisForm'
import ComplaintFetcher from '../components/ComplaintFetcher'

function Home() {
  return (
    <Container maxWidth="sm">
      <Typography variant="h4" component="h1" gutterBottom>
        Plasma QR Home
      </Typography>
      <AnalysisForm />
      <ComplaintFetcher />
    </Container>
  )
}

export default Home
