vi.mock('@hophiphip/react-fishbone', () => ({
  default: ({ items }) => <div data-testid="fishbone">{items.label}</div>
}), { virtual: true })

import { render, screen } from '@testing-library/react'
import FishboneDiagram from '../components/FishboneDiagram'

it('renders items label', () => {
  const items = { label: 'Root' }
  render(<FishboneDiagram items={items} />)
  expect(screen.getByTestId('fishbone')).toHaveTextContent('Root')
})
