import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import AnalysisForm from '../components/AnalysisForm'

vi.mock('@mui/material/Autocomplete', () => ({
  __esModule: true,
  default: ({ value, onChange, onInputChange, renderInput }) => {
    const params = { inputProps: {}, InputProps: {} }
    const { inputProps } = renderInput(params).props
    const handler = onChange || onInputChange || (() => {})
    return (
      <input
        data-testid={inputProps['data-testid']}
        value={value || ''}
        onChange={(e) => handler(null, e.target.value)}
      />
    )
  }
}))


beforeEach(() => {
  global.fetch = vi.fn()
})

afterEach(() => {
  vi.restoreAllMocks()
})

test('submits form and shows results', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ step: 'a' }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ result: 'done' }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ pdf: 'p', excel: 'e' }) })

  render(<AnalysisForm />)
  fetch.mockClear()

  fireEvent.change(screen.getByLabelText(/complaint/i), { target: { value: 'c' } })
  fireEvent.change(screen.getByTestId('customer-input'), { target: { value: 'cu' } })
  fireEvent.change(screen.getByTestId('subject-input'), { target: { value: 's' } })
  fireEvent.change(screen.getByTestId('partcode-input'), { target: { value: 'p' } })
  fireEvent.change(screen.getByTestId('method-input'), { target: { value: '8D' } })
  fireEvent.click(screen.getByRole('button', { name: /analyze/i }))

  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3))
  await screen.findByText(/done/)
  await screen.findByText(/created successfully/i)
  await screen.findByTestId('CheckCircleIcon')
  expect(screen.getByTestId('PictureAsPdfIcon')).toBeInTheDocument()
  expect(screen.getByTestId('FileDownloadIcon')).toBeInTheDocument()
})

test('shows error on api failure', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: false, status: 500 })

  render(<AnalysisForm />)
  fetch.mockClear()
  fireEvent.change(screen.getByLabelText(/complaint/i), { target: { value: 'c' } })
  fireEvent.change(screen.getByTestId('customer-input'), { target: { value: 'cu' } })
  fireEvent.change(screen.getByTestId('subject-input'), { target: { value: 's' } })
  fireEvent.change(screen.getByTestId('partcode-input'), { target: { value: 'p' } })
  fireEvent.change(screen.getByTestId('method-input'), { target: { value: '8D' } })
  fireEvent.click(screen.getByRole('button', { name: /analyze/i }))

  await waitFor(() => expect(fetch).toHaveBeenCalled())
  await screen.findByText(/http 500/i)
  expect(screen.getByText(/http 500/i)).toBeInTheDocument()
})
