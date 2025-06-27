import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import SampleForm from '../components/SampleForm'
import ComplaintFetcher from '../components/ComplaintFetcher'

function Home() {
  return (
    <Container maxWidth="sm">
      <Typography variant="h4" component="h1" gutterBottom>
        Plasma QR Home
      </Typography>
      <SampleForm />
      <ComplaintFetcher />
    </Container>
  )
}

export default Home
