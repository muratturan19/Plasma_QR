import { render, screen } from '@testing-library/react'
import Footer from '../components/Footer'

it('renders company info and links', () => {
  render(<Footer />)
  const year = new Date().getFullYear().toString()
  expect(screen.getByText(new RegExp(year))).toBeInTheDocument()
  expect(screen.getByRole('link', { name: /about/i })).toBeInTheDocument()
  expect(screen.getByRole('link', { name: /privacy/i })).toBeInTheDocument()
})
