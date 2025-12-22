"use client"

import { useState } from "react"
import { ListingCard } from "@/widgets/listing-card"
import { Pagination } from "@/shared/ui/pagination"
import { SkeletonCard } from "@/shared/ui/skeleton-card"
import { useGetListingsQuery } from "@/shared/api/marketplace-api"
import { useAppSelector } from "@/shared/lib/hooks"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AlertCircle, Plus } from "lucide-react"
import Link from "next/link"
import { ROUTES } from "@/shared/lib/constants"

export default function MarketplacePage() {
  const [filters, setFilters] = useState({
    page: 1,
    per_page: 12,
  })

  const { isAuthenticated } = useAppSelector((state) => state.auth)
  const { data, isLoading, error } = useGetListingsQuery(filters)

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8 flex items-start justify-between gap-4">
        <div>
          <h1 className="mb-2 text-3xl font-bold">Marketplace</h1>
          <p className="text-muted-foreground">Buy and sell Hot Wheels with collectors worldwide</p>
        </div>
        {isAuthenticated && (
          <Button asChild>
            <Link href={ROUTES.MARKETPLACE_CREATE} className="gap-2">
              <Plus className="h-4 w-4" />
              Create Listing
            </Link>
              </Button>
            )}
          </div>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>Failed to load listings. Please try again later.</AlertDescription>
          </Alert>
        )}

        {isLoading ? (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {Array.from({ length: 12 }).map((_, i) => (
              <SkeletonCard key={i} />
            ))}
          </div>
        ) : data?.data.length === 0 ? (
          <div className="flex min-h-96 items-center justify-center">
            <div className="text-center">
              <p className="text-lg font-medium">No listings found</p>
              <p className="text-sm text-muted-foreground">Check back later for new items</p>
            </div>
          </div>
        ) : (
          <>
            <div className="mb-4 text-sm text-muted-foreground">
              Showing {data?.data.length || 0} of {data?.total || 0} listings
            </div>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {data?.data.map((listing) => (
                <ListingCard key={listing.id} listing={listing} />
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
  )
}
