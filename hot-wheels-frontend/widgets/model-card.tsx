import Link from "next/link"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import type { CarModel } from "@/shared/types"
import { ROUTES } from "@/shared/lib/constants"

interface ModelCardProps {
  model: CarModel
}

export function ModelCard({ model }: ModelCardProps) {
  const rarityColors = {
    common: "bg-secondary text-secondary-foreground",
    uncommon: "bg-chart-2/20 text-chart-2",
    rare: "bg-chart-3/20 text-chart-3",
    super_rare: "bg-chart-4/20 text-chart-4",
    chase: "bg-chart-5/20 text-chart-5",
  }

  return (
    <Link href={ROUTES.CATALOG_DETAIL(model.id)}>
      <Card className="group h-full overflow-hidden transition-all hover:shadow-md">
        <CardHeader className="p-0">
          <div className="aspect-video w-full overflow-hidden bg-muted">
            {model.images?.[0] ? (
              <img
                src={model.images[0] || "/placeholder.svg"}
                alt={model.name}
                className="h-full w-full object-cover transition-transform group-hover:scale-105"
              />
            ) : (
              <div className="flex h-full w-full items-center justify-center text-muted-foreground">No Image</div>
            )}
          </div>
        </CardHeader>
        <CardContent className="p-4">
          <div className="mb-2 flex items-start justify-between gap-2">
            <CardTitle className="line-clamp-1 text-base">{model.name}</CardTitle>
            <Badge variant="secondary" className={rarityColors[model.rarity] || rarityColors.common}>
              {(model.rarity || "common").replace(/_/g, " ")}
            </Badge>
          </div>
          <div className="space-y-1 text-sm text-muted-foreground">
            <p>Year: {model.year}</p>
            <p>Color: {model.color}</p>
            {model.series && <p className="line-clamp-1">Series: {model.series.name}</p>}
          </div>
        </CardContent>
        {model.estimatedValue && (
          <CardFooter className="border-t border-border bg-muted/50 p-4">
            <p className="text-sm font-medium">Est. Value: ${model.estimatedValue.toFixed(2)}</p>
          </CardFooter>
        )}
      </Card>
    </Link>
  )
}
