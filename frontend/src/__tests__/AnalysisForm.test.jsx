import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import AnalysisForm from '../components/AnalysisForm'

vi.mock('@mui/material/Autocomplete', () => ({
  __esModule: true,
  default: ({ value, inputValue, onChange, onInputChange, renderInput }) => {
    const params = { inputProps: {}, InputProps: {} };
    const { inputProps } = renderInput(params).props;
    const handler = onChange || onInputChange || (() => {});
    return (
      <input
        data-testid={inputProps['data-testid'] || inputProps.id}
        value={inputValue || value || ''}
        onChange={(e) => handler(null, e.target.value)}
      />
    );
  }
}));

beforeEach(() => {
  global.fetch = vi.fn()
})

afterEach(() => {
  vi.restoreAllMocks()
})

test('shows error when options fetch fails', async () => {
  fetch.mockRejectedValueOnce(new Error('fail'))
  fetch.mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
  fetch.mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })

  render(<AnalysisForm />)

  await screen.findByText(/could not retrieve dropdown values/i)
})

test('shows guide text when method selected', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })

  render(<AnalysisForm />)
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3))

  fireEvent.change(screen.getByTestId('method-input'), {
    target: { value: '8D' }
  })
  expect(screen.getByText(/eight disciplines/i)).toBeInTheDocument()
})
