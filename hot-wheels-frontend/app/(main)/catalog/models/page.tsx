"use client"

import { useState } from "react"
import { ModelCard } from "@/widgets/model-card"
import { CatalogFilters } from "@/features/catalog/catalog-filters"
import { Pagination } from "@/shared/ui/pagination"
import { SkeletonCard } from "@/shared/ui/skeleton-card"
import { useGetModelsQuery } from "@/shared/api/catalog-api"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AlertCircle } from "lucide-react"

export default function CatalogPage() {
  const [filters, setFilters] = useState({
    page: 1,
    per_page: 12,
  })

  const { data, isLoading, error } = useGetModelsQuery(filters)

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">Hot Wheels Catalog</h1>
        <p className="text-muted-foreground">Browse our complete collection of Hot Wheels models</p>
      </div>

          <div className="flex flex-col gap-6 lg:flex-row">
            {/* Filters Sidebar */}
            <aside className="w-full lg:w-64 lg:shrink-0">
              <CatalogFilters
                onFiltersChange={(newFilters) => {
                  setFilters({ ...filters, ...newFilters, page: 1 })
                }}
              />
            </aside>

            {/* Main Content */}
            <div className="flex-1">
              {error && (
                <Alert variant="destructive" className="mb-6">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>Failed to load models. Please try again later.</AlertDescription>
                </Alert>
              )}

              {isLoading ? (
                <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                  {Array.from({ length: 12 }).map((_, i) => (
                    <SkeletonCard key={i} />
                  ))}
                </div>
              ) : data?.data.length === 0 ? (
                <div className="flex min-h-96 items-center justify-center">
                  <div className="text-center">
                    <p className="text-lg font-medium">No models found</p>
                    <p className="text-sm text-muted-foreground">Try adjusting your filters</p>
                  </div>
                </div>
              ) : (
                <>
                  <div className="mb-4 text-sm text-muted-foreground">
                    Showing {data?.data.length || 0} of {data?.total || 0} models
                  </div>
                  <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                    {data?.data.map((model) => (
                      <ModelCard key={model.id} model={model} />
                    ))}
                  </div>

                  {data && data.totalPages > 1 && (
                    <div className="mt-8">
                      <Pagination
                        currentPage={data.page}
                        totalPages={data.totalPages}
                        onPageChange={(page) => setFilters({ ...filters, page })}
                      />
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
  )
}
