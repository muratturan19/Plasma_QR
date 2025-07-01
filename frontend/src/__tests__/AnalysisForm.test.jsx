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
vi.mock('fishbone-chart', () => ({
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

test('runs analyze workflow', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ fields: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ full_text: 'a' }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ result: 'r' }) })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ pdf: '/p', excel: '/e' })
    })

  render(<AnalysisForm initialMethod="8D" />)
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3))

  fireEvent.change(screen.getByLabelText('Şikayet (Complaint)'), {
    target: { value: 'c' }
  })
  fireEvent.click(screen.getByRole('button', { name: 'ANALİZ ET' }))

  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(7))
  expect(fetch.mock.calls[3][0]).toMatch(/\/guide\/8D/)
  expect(fetch.mock.calls[4][0]).toMatch(/\/analyze$/)
  expect(fetch.mock.calls[5][0]).toMatch(/\/review$/)
  expect(fetch.mock.calls[6][0]).toMatch(/\/report$/)
  await screen.findByTestId('analysis-text')
  await screen.findByTestId('review-text')
  await screen.findByTestId('pdf-link')
  await screen.findByTestId('excel-link')
})

test('shows error alert on analyze failure', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ fields: [] }) })
    .mockResolvedValueOnce({ ok: false, text: async () => 'fail' })

  render(<AnalysisForm initialMethod="8D" />)
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3))

  fireEvent.change(screen.getByLabelText('Şikayet (Complaint)'), {
    target: { value: 'c' }
  })
  fireEvent.click(screen.getByRole('button', { name: 'ANALİZ ET' }))

  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(5))
  expect(screen.getAllByRole('alert')[1]).toHaveTextContent('fail')
})

test('shows error alert on empty report response', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ fields: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ full_text: 'a' }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ result: 'r' }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({}) })

  render(<AnalysisForm initialMethod="8D" />)
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3))

  fireEvent.change(screen.getByLabelText('Şikayet (Complaint)'), {
    target: { value: 'c' }
  })
  fireEvent.click(screen.getByRole('button', { name: 'ANALİZ ET' }))

  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(7))
  const alert = await screen.findAllByRole('alert')
  expect(alert[1]).toHaveTextContent('Sunucudan beklenmeyen boş yanıt alındı')
  await screen.findByTestId('analysis-text')
  expect(await screen.findByTestId('review-text')).toHaveTextContent('r')
})

test('shows alert when analyze request rejects', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ fields: [] }) })
    .mockRejectedValueOnce(new Error('server error'))

  render(<AnalysisForm initialMethod="8D" />)
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3))

  fireEvent.change(screen.getByLabelText('Şikayet (Complaint)'), {
    target: { value: 'c' }
  })
  fireEvent.click(screen.getByRole('button', { name: 'ANALİZ ET' }))

  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(5))
  const alert = await screen.findAllByRole('alert')
  expect(alert[1]).toHaveTextContent('server error')
})

test('shows loading indicator during analyze', async () => {
  let resolveGuide
  const guidePromise = new Promise((res) => {
    resolveGuide = res
  })

  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockReturnValueOnce(guidePromise)
    .mockResolvedValueOnce({ ok: true, json: async () => ({ full_text: 't' }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ result: 'r' }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ pdf: '/p', excel: '/e' }) })

  render(<AnalysisForm initialMethod="8D" />)
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3))

  fireEvent.change(screen.getByLabelText('Şikayet (Complaint)'), {
    target: { value: 'c' }
  })
  fireEvent.click(screen.getByRole('button', { name: 'ANALİZ ET' }))

  await screen.findByTestId('loading-indicator')
  resolveGuide({ ok: true, json: async () => ({ fields: [] }) })

  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(7))
  expect(screen.queryByTestId('loading-indicator')).toBeNull()
})
