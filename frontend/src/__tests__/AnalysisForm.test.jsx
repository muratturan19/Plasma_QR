import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import AnalysisForm from '../components/AnalysisForm'

vi.mock('@mui/material/Autocomplete', () => ({
  __esModule: true,
  default: ({ value, onChange }) => (
    <input data-testid="method-input" value={value || ''} onChange={(e) => onChange(null, e.target.value)} />
  )
}))

beforeEach(() => {
  global.fetch = vi.fn()
})

afterEach(() => {
  vi.restoreAllMocks()
})

test('submits form and shows results', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ step: 'a' }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ result: 'done' }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ pdf: 'p', excel: 'e' }) })

  render(<AnalysisForm />)

  fireEvent.change(screen.getByLabelText(/complaint/i), { target: { value: 'c' } })
  fireEvent.change(screen.getByLabelText(/customer/i), { target: { value: 'cu' } })
  fireEvent.change(screen.getByLabelText(/subject/i), { target: { value: 's' } })
  fireEvent.change(screen.getByLabelText(/part code/i), { target: { value: 'p' } })
  fireEvent.change(screen.getByTestId('method-input'), { target: { value: '8D' } })
  fireEvent.click(screen.getByRole('button', { name: /analyze/i }))

  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3))
  await screen.findByText(/done/)
  await screen.findByText(/created successfully/i)
})

test('shows error on api failure', async () => {
  fetch.mockResolvedValueOnce({ ok: false, status: 500 })

  render(<AnalysisForm />)
  fireEvent.change(screen.getByLabelText(/complaint/i), { target: { value: 'c' } })
  fireEvent.change(screen.getByLabelText(/customer/i), { target: { value: 'cu' } })
  fireEvent.change(screen.getByLabelText(/subject/i), { target: { value: 's' } })
  fireEvent.change(screen.getByLabelText(/part code/i), { target: { value: 'p' } })
  fireEvent.change(screen.getByTestId('method-input'), { target: { value: '8D' } })
  fireEvent.click(screen.getByRole('button', { name: /analyze/i }))

  await waitFor(() => expect(fetch).toHaveBeenCalled())
  await screen.findByText(/http 500/i)
  expect(screen.getByText(/http 500/i)).toBeInTheDocument()
})
