import { render, screen } from '@testing-library/react'
import SampleForm from '../components/SampleForm'

beforeAll(() => {
  global.ResizeObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  }
})

it('renders analysis and query forms', () => {
  render(<SampleForm />)
  const buttons = screen.getAllByRole('button')
  expect(buttons.length).toBeGreaterThanOrEqual(2)
})
