import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import ComplaintFetcher from '../components/ComplaintFetcher'

beforeEach(() => {
  global.fetch = vi.fn()
})

afterEach(() => {
  vi.restoreAllMocks()
})

test('fetches complaints and shows data', async () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({ store: [{ complaint: 'a' }], excel: [{ complaint: 'b' }] })
  })

  render(<ComplaintFetcher />)

  fireEvent.click(screen.getByLabelText('Müşteri'))
  fireEvent.click(screen.getByLabelText('Konu'))
  fireEvent.click(screen.getByRole('button', { name: /fetch complaints/i }))

  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1))
  const url = fetch.mock.calls[0][0]
  expect(url).toContain('customer=1')
  expect(url).toContain('subject=1')
  await screen.findByText(/"a"/)
  await screen.findByText(/"b"/)
})

test('shows error when api fails', async () => {
  fetch.mockResolvedValueOnce({ ok: false, status: 404 })

  render(<ComplaintFetcher />)

  fireEvent.click(screen.getByLabelText('Müşteri'))
  fireEvent.click(screen.getByRole('button', { name: /fetch complaints/i }))
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1))
  await screen.findByText(/http error 404/i)
})
