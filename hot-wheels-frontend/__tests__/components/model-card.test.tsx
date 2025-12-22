import { render, screen } from "@testing-library/react"
import { ModelCard } from "@/widgets/model-card"
import type { CarModel } from "@/shared/types"

const mockModel: CarModel = {
  id: "1",
  name: "Custom '67 Pontiac Firebird",
  year: 2020,
  color: "Red",
  rarity: "rare",
  images: ["https://example.com/image.jpg"],
  estimatedValue: 25.99,
  createdAt: "2023-01-01T00:00:00Z",
  updatedAt: "2023-01-01T00:00:00Z",
}

describe("ModelCard", () => {
  it("renders model information correctly", () => {
    render(<ModelCard model={mockModel} />)

    expect(screen.getByText("Custom '67 Pontiac Firebird")).toBeInTheDocument()
    expect(screen.getByText("Year: 2020")).toBeInTheDocument()
    expect(screen.getByText("Color: Red")).toBeInTheDocument()
    expect(screen.getByText("Est. Value: $25.99")).toBeInTheDocument()
  })

  it("displays rarity badge", () => {
    render(<ModelCard model={mockModel} />)

    expect(screen.getByText("rare")).toBeInTheDocument()
  })

  it("shows 'No Image' when no image is provided", () => {
    const modelWithoutImage = { ...mockModel, images: [] }
    render(<ModelCard model={modelWithoutImage} />)

    expect(screen.getByText("No Image")).toBeInTheDocument()
  })
})
