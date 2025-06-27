import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import ComplaintQuery from '../components/ComplaintQuery'

beforeEach(() => {
  global.fetch = vi.fn()
})

afterEach(() => {
  vi.restoreAllMocks()
})

test('queries with selected filters', async () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({ store: [{ complaint: 'c', customer: 'x' }], excel: [] })
  })

  render(<ComplaintQuery />)

  fireEvent.change(screen.getAllByRole('textbox')[1], { target: { value: 'x' } })
  fireEvent.click(screen.getAllByRole('checkbox')[1])
  fireEvent.click(screen.getByRole('button', { name: /query/i }))

  await waitFor(() => expect(fetch).toHaveBeenCalled())
  const cells = await screen.findAllByText('c')
  expect(cells.length).toBeGreaterThan(0)
})

