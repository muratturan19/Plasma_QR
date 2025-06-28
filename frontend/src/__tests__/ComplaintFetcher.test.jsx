import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import ComplaintFetcher from '../components/ComplaintFetcher'

beforeEach(() => {
  global.fetch = vi.fn()
})

afterEach(() => {
  vi.restoreAllMocks()
})

test('fetches complaints and shows data', async () => {
  fetch
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ store: [{ complaint: 'a' }], excel: [] })
    })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ store: [], excel: [{ complaint: 'b' }] })
    })

  render(<ComplaintFetcher />)

  const checkboxes = screen.getAllByRole('checkbox')
  fireEvent.click(checkboxes[0])
  fireEvent.click(checkboxes[1])
  fireEvent.click(screen.getByRole('button', { name: /fetch complaints/i }))

  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(2))
  await screen.findByText(/"a"/)
  await screen.findByText(/"b"/)
})

test('shows error when api fails', async () => {
  fetch.mockResolvedValueOnce({ ok: false, status: 404 })

  render(<ComplaintFetcher />)

  fireEvent.click(screen.getAllByRole('checkbox')[0])
  fireEvent.click(screen.getByRole('button', { name: /fetch complaints/i }))
  await waitFor(() => expect(fetch).toHaveBeenCalled())
  await screen.findByText(/http error 404/i)
})
