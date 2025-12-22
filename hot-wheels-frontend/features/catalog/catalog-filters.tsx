"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { RARITY_OPTIONS } from "@/shared/lib/constants"
import { Search, X } from "lucide-react"

interface CatalogFiltersProps {
  onFiltersChange: (filters: {
    q?: string
    year_min?: number
    year_max?: number
    rarity?: string
    color?: string
  }) => void
}

export function CatalogFilters({ onFiltersChange }: CatalogFiltersProps) {
  const [search, setSearch] = useState("")
  const [yearMin, setYearMin] = useState("")
  const [yearMax, setYearMax] = useState("")
  const [rarity, setRarity] = useState("all")
  const [color, setColor] = useState("")

  const handleApplyFilters = () => {
    onFiltersChange({
      q: search || undefined,
      year_min: yearMin ? Number.parseInt(yearMin) : undefined,
      year_max: yearMax ? Number.parseInt(yearMax) : undefined,
      rarity: rarity || undefined,
      color: color || undefined,
    })
  }

  const handleReset = () => {
    setSearch("")
    setYearMin("")
    setYearMax("")
    setRarity("all")
    setColor("")
    onFiltersChange({})
  }

  return (
    <div className="space-y-4 rounded-lg border border-border bg-card p-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold">Filters</h3>
        <Button variant="ghost" size="sm" onClick={handleReset} className="h-8 gap-2">
          <X className="h-4 w-4" />
          Reset
        </Button>
      </div>

      <div className="space-y-4">
        <div className="space-y-2">
          <Label>Search</Label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search models..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9"
              onKeyDown={(e) => e.key === "Enter" && handleApplyFilters()}
            />
          </div>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label>Year From</Label>
            <Input
              type="number"
              placeholder="1968"
              value={yearMin}
              onChange={(e) => setYearMin(e.target.value)}
              min="1968"
            />
          </div>

          <div className="space-y-2">
            <Label>Year To</Label>
            <Input
              type="number"
              placeholder={new Date().getFullYear().toString()}
              value={yearMax}
              onChange={(e) => setYearMax(e.target.value)}
              max={new Date().getFullYear()}
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label>Rarity</Label>
          <Select value={rarity} onValueChange={setRarity}>
            <SelectTrigger>
              <SelectValue placeholder="All rarities" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All rarities</SelectItem>
              {RARITY_OPTIONS.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label>Color</Label>
          <Input placeholder="e.g., Red, Blue" value={color} onChange={(e) => setColor(e.target.value)} />
        </div>

        <Button onClick={handleApplyFilters} className="w-full">
          Apply Filters
        </Button>
      </div>
    </div>
  )
}
