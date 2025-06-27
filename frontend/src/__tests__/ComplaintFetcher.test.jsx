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
    json: async () => ({ msg: 'done' })
  })

  render(<ComplaintFetcher />)

  fireEvent.click(screen.getByRole('button', { name: /fetch complaints/i }))
  await waitFor(() => expect(fetch).toHaveBeenCalled())
  await screen.findByText(/done/)
})

test('shows error when api fails', async () => {
  fetch.mockResolvedValueOnce({ ok: false, status: 404 })

  render(<ComplaintFetcher />)

  fireEvent.click(screen.getByRole('button', { name: /fetch complaints/i }))
  await waitFor(() => expect(fetch).toHaveBeenCalled())
  await screen.findByText(/http error 404/i)
})
