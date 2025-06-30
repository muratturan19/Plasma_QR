vi.mock('fishbone-chart', () => ({
  default: ({ data }) => (
    <div data-testid="fishbone">{Object.keys(data)[0]}</div>
  )
}), { virtual: true })

import { render, screen } from '@testing-library/react'
import FishboneDiagram from '../components/FishboneDiagram'

it('renders items label', () => {
  const data = { Root: {} }
  render(<FishboneDiagram data={data} />)
  expect(screen.getByTestId('fishbone')).toHaveTextContent('Root')
})
