import Box from '@mui/material/Box'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'

function SampleForm() {
  const handleSubmit = (event) => {
    event.preventDefault()
    // TODO: handle form submission
  }

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 2 }}>
      <TextField
        label="Sample Input"
        name="sample"
        fullWidth
        margin="normal"
      />
      <Button type="submit" variant="contained">Submit</Button>
    </Box>
  )
}

export default SampleForm
