import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import AnalysisForm from '../components/AnalysisForm';

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
  global.fetch = vi.fn();
});

afterEach(() => {
  vi.restoreAllMocks();
});

test('fetches options and logs analysis data', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) });

  const logSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

  render(<AnalysisForm />);
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3));

  fireEvent.change(screen.getByLabelText(/şikayet/i), { target: { value: 'c' } });
  fireEvent.change(screen.getByLabelText(/müşteri/i), { target: { value: 'cu' } });
  fireEvent.change(screen.getByLabelText(/konu/i), { target: { value: 's' } });
  fireEvent.change(screen.getByLabelText(/parça kodu/i), { target: { value: 'p' } });
  fireEvent.change(screen.getByLabelText(/metot/i), { target: { value: '8D' } });
  fireEvent.click(screen.getByRole('button', { name: /analiz et/i }));

  expect(logSpy).toHaveBeenCalledWith({
    complaint: 'c',
    customer: 'cu',
    subject: 's',
    partCode: 'p',
    method: '8D',
    directives: ''
  });
});

test('shows guide text when method selected', async () => {
  fetch
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ values: [] }) });

  render(<AnalysisForm />);
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(3));

  fireEvent.change(screen.getByLabelText(/metot/i), { target: { value: '8D' } });
  expect(screen.getByText(/eight disciplines/i)).toBeInTheDocument();
});
