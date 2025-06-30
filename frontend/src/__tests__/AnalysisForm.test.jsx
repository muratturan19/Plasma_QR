import { render, screen, fireEvent, waitFor } from '@testing-library/react'

vi.mock('@mui/material/Autocomplete', () => ({
  __esModule: true,
  default: ({ value, inputValue, onChange, onInputChange, renderInput }) => {
    const params = { inputProps: {}, InputProps: {} }
    const { inputProps, label } = renderInput(params).props
    const handler = onChange || onInputChange || (() => {})
    return (
      <input
        aria-label={label}
        data-testid={inputProps['data-testid'] || inputProps.id}
        value={inputValue || value || ''}
        onChange={(e) => handler(null, e.target.value)}
      />
    )
  }
}))
vi.mock('@hophiphip/react-fishbone', () => ({
  default: () => <div data-testid="fishbone">diagram</div>
}), { virtual: true })

import AnalysisForm from '../components/AnalysisForm'
beforeAll(() => {
  global.ResizeObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  }
})


beforeEach(() => {
  global.fetch = vi.fn()
})

afterEach(() => {
  vi.restoreAllMocks()
})

test('renders when options fetch fails', async () => {
  fetch.mockRejectedValueOnce(new Error('fail'))
  fetch.mockResolvedValueOnce({ ok: true, json: async () => ({}) })
  fetch.mockResolvedValueOnce({ ok: true, json: async () => ({}) })

  render(<AnalysisForm />)
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3))

  expect(screen.getByText(/özel talimatlar/i)).toBeInTheDocument()
})

test('shows guide text when method selected', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })

  render(<AnalysisForm />)
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3))

  const methodInput = screen.getByLabelText('Metot')
  fireEvent.change(methodInput, {
    target: { value: '8D' }
  })
})

test('fetches filtered claims', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ excel: [{ complaint: 'x' }], store: [] })
    })

  render(<AnalysisForm />)
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3))

  fireEvent.change(screen.getByTestId('customer-input'), {
    target: { value: 'acme' }
  })
  fireEvent.click(screen.getByLabelText('Müşteri'))
  fireEvent.click(screen.getByRole('button', { name: /şikayetleri getir/i }))

  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(4))
  const url = fetch.mock.calls[3][0]
  expect(url).toContain('customer=acme')
  await screen.findByText(/"x"/)
})

test('applies instructionsBoxProps margin', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })

  render(<AnalysisForm instructionsBoxProps={{ mt: 5 }} />)
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3))

  const box = screen.getByText(/özel talimatlar/i).parentElement
  expect(box).toHaveStyle('margin-top: 40px')
})

test('shows fishbone diagram on Ishikawa method', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })

  render(<AnalysisForm initialMethod="Ishikawa" />)
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3))
  expect(screen.getByTestId('fishbone')).toBeInTheDocument()
})
