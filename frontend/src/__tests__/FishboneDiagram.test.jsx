import { render, screen } from '@testing-library/react'
import FishboneDiagram from '../components/FishboneDiagram'

test.skip('renders items label', () => {
  const data = { Root: {} }
  render(<FishboneDiagram data={data} />)
  expect(screen.getByTestId('fishbone')).toHaveTextContent('Root')
})
