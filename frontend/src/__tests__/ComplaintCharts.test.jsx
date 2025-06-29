import { render, screen } from '@testing-library/react'
import ComplaintCharts from '../components/ComplaintCharts'

beforeAll(() => {
  global.ResizeObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  }
})

test('renders form and chart titles', () => {
  render(<ComplaintCharts form={<div>FORM</div>} />)
  expect(screen.getByText('FORM')).toBeInTheDocument()
  expect(screen.getByText(/2025 Aylık Şikayet/i)).toBeInTheDocument()
  expect(screen.getByText(/Son 10 Yıl Şikayet/i)).toBeInTheDocument()
})
