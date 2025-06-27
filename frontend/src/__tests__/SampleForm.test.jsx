import { render, screen } from '@testing-library/react'
import SampleForm from '../components/SampleForm'

it('renders analysis and query forms', () => {
  render(<SampleForm />)
  expect(screen.getByRole('button', { name: /analyze/i })).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /query/i })).toBeInTheDocument()
})
