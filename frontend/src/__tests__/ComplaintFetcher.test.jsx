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
    json: async () => ({
      store: [{ complaint: 'a', customer: 'one' }],
      excel: [{ complaint: 'b', customer: 'two' }]
    })
  })

  render(<ComplaintFetcher />)

  const inputs = screen.getAllByRole('textbox')
  const checks = screen.getAllByRole('checkbox')
  fireEvent.change(inputs[0], { target: { value: 'cust' } })
  fireEvent.click(checks[0])
  fireEvent.change(inputs[1], { target: { value: 'subj' } })
  fireEvent.click(checks[1])
  fireEvent.change(inputs[2], { target: { value: 'part' } })
  fireEvent.click(checks[2])
  fireEvent.click(screen.getByRole('button', { name: /fetch complaints/i }))

  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1))
  const url = fetch.mock.calls[0][0]
  expect(url).toContain('customer=cust')
  expect(url).toContain('subject=subj')
  expect(url).toContain('part_code=part')
  await screen.findByText('a')
  await screen.findByText('b')
  const headers = screen.getAllByRole('columnheader').map((h) => h.textContent)
  expect(headers).toEqual(expect.arrayContaining(['complaint', 'customer']))
  const rows = await screen.findAllByRole('row')
  expect(rows.length).toBeGreaterThan(1)
})

test('shows error when api fails', async () => {
  fetch.mockResolvedValueOnce({ ok: false, status: 404 })

  render(<ComplaintFetcher />)

  fireEvent.change(screen.getAllByRole('textbox')[0], { target: { value: 'x' } })
  fireEvent.click(screen.getAllByRole('checkbox')[0])
  fireEvent.click(screen.getByRole('button', { name: /fetch complaints/i }))
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1))
  await screen.findByText(/http error 404/i)
})
