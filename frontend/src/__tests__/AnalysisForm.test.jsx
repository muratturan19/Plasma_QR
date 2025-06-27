import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import AnalysisForm from '../components/AnalysisForm'

vi.mock('@mui/x-date-pickers/DatePicker', () => {
  return {
    DatePicker: ({ onChange, ...props }) => (
      <input
        data-testid="date-input"
        onChange={(e) => onChange(new Date(e.target.value))}
        {...props}
      />
    )
  }
})

vi.mock('@mui/material/Autocomplete', () => ({
  __esModule: true,
  default: ({ value, onChange }) => (
    <input
      data-testid="guideline-input"
      value={value || ''}
      onChange={(e) => onChange(null, e.target.value)}
    />
  )
}))

beforeEach(() => {
  global.fetch = vi.fn()
})

afterEach(() => {
  vi.restoreAllMocks()
})

test('submits form and shows results', async () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({ result: 'ok' })
  })

  render(<AnalysisForm />)

  fireEvent.change(screen.getByLabelText(/complaint/i), {
    target: { value: 'issue' }
  })
  fireEvent.change(screen.getByTestId('guideline-input'), {
    target: { value: '8D' }
  })
  const dateInput = screen.getByTestId('date-input')
  fireEvent.change(dateInput, { target: { value: '2024-01-01' } })

  fireEvent.click(screen.getByRole('button', { name: /analyze/i }))

  await waitFor(() => expect(fetch).toHaveBeenCalled())
  await screen.findByText('result')
})

test('shows error on api failure', async () => {
  fetch.mockResolvedValueOnce({ ok: false, status: 500 })

  render(<AnalysisForm />)

  fireEvent.change(screen.getByLabelText(/complaint/i), {
    target: { value: 'issue' }
  })
  fireEvent.change(screen.getByTestId('guideline-input'), {
    target: { value: '8D' }
  })
  const dateInput = screen.getByTestId('date-input')
  fireEvent.change(dateInput, { target: { value: '2024-01-01' } })

  fireEvent.click(screen.getByRole('button', { name: /analyze/i }))

  await waitFor(() => expect(fetch).toHaveBeenCalled())
  await screen.findByText(/http 500/i)
})
