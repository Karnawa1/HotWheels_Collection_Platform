"use client"

import { use } from "react"
import { useRouter } from "next/navigation"
import { Header } from "@/widgets/header"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { useGetModelByIdQuery } from "@/shared/api/catalog-api"
import { useAppSelector } from "@/shared/lib/hooks"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AlertCircle, Heart, Package, ArrowLeft } from "lucide-react"

export default function ModelDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params)
  const router = useRouter()
  const { isAuthenticated } = useAppSelector((state) => state.auth)
  const { data: model, isLoading, error } = useGetModelByIdQuery(id)

  if (error) {
    return (
      <div className="flex min-h-screen flex-col">
        <Header />
        <main className="flex flex-1 items-center justify-center">
          <Alert variant="destructive" className="max-w-md">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>Failed to load model details. Please try again later.</AlertDescription>
          </Alert>
        </main>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1">
        <div className="container mx-auto px-4 py-8">
          <Button variant="ghost" onClick={() => router.back()} className="mb-6 gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to Catalog
          </Button>

          {isLoading ? (
            <div className="grid gap-8 lg:grid-cols-2">
              <Skeleton className="aspect-square w-full rounded-lg" />
              <div className="space-y-4">
                <Skeleton className="h-10 w-3/4" />
                <Skeleton className="h-6 w-1/4" />
                <Skeleton className="h-24 w-full" />
                <Skeleton className="h-32 w-full" />
              </div>
            </div>
          ) : model ? (
            <div className="grid gap-8 lg:grid-cols-2">
              {/* Images */}
              <div className="space-y-4">
                <div className="aspect-square overflow-hidden rounded-lg border border-border bg-muted">
                  {model.images?.[0] ? (
                    <img
                      src={model.images[0] || "/placeholder.svg"}
                      alt={model.name}
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <div className="flex h-full w-full items-center justify-center text-muted-foreground">
                      No Image Available
                    </div>
                  )}
                </div>
              </div>

              {/* Details */}
              <div className="space-y-6">
                <div>
                  <h1 className="mb-2 text-3xl font-bold text-balance">{model.name}</h1>
                  <Badge variant="secondary" className="text-sm">
                    {model.rarity.replace("_", " ").toUpperCase()}
                  </Badge>
                </div>

                {model.description && <p className="text-muted-foreground text-pretty">{model.description}</p>}

                <Card>
                  <CardContent className="grid gap-4 p-6 sm:grid-cols-2">
                    <div>
                      <p className="text-sm text-muted-foreground">Year</p>
                      <p className="font-medium">{model.year}</p>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground">Color</p>
                      <p className="font-medium">{model.color}</p>
                    </div>
                    {model.series && (
                      <div>
                        <p className="text-sm text-muted-foreground">Series</p>
                        <p className="font-medium">{model.series.name}</p>
                      </div>
                    )}
                    {model.casting && (
                      <div>
                        <p className="text-sm text-muted-foreground">Casting</p>
                        <p className="font-medium">{model.casting.name}</p>
                      </div>
                    )}
                    {model.manufacturer && (
                      <div>
                        <p className="text-sm text-muted-foreground">Manufacturer</p>
                        <p className="font-medium">{model.manufacturer.name}</p>
                      </div>
                    )}
                    {model.estimatedValue && (
                      <div>
                        <p className="text-sm text-muted-foreground">Est. Value</p>
                        <p className="font-medium">${model.estimatedValue.toFixed(2)}</p>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {isAuthenticated && (
                  <div className="flex flex-wrap gap-4">
                    <Button className="gap-2">
                      <Package className="h-4 w-4" />
                      Add to Collection
                    </Button>
                    <Button variant="outline" className="gap-2 bg-transparent">
                      <Heart className="h-4 w-4" />
                      Add to Wishlist
                    </Button>
                  </div>
                )}
              </div>
            </div>
          ) : null}
        </div>
      </main>
    </div>
  )
}
