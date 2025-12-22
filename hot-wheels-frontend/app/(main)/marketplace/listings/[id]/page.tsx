"use client"

import Link from "next/link"

import { use } from "react"
import { useRouter } from "next/navigation"
import { Header } from "@/widgets/header"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { useGetListingByIdQuery, useCreateTransactionMutation } from "@/shared/api/marketplace-api"
import { useAppSelector } from "@/shared/lib/hooks"
import { ROUTES } from "@/shared/lib/constants"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AlertCircle, ArrowLeft, ShoppingCart, User } from "lucide-react"
import { toast } from "sonner"

export default function ListingDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params)
  const router = useRouter()
  const { isAuthenticated, user } = useAppSelector((state) => state.auth)
  const { data: listing, isLoading, error } = useGetListingByIdQuery(id)
  const [createTransaction, { isLoading: isPurchasing }] = useCreateTransactionMutation()

  const handlePurchase = async () => {
    if (!isAuthenticated) {
      router.push(ROUTES.LOGIN)
      return
    }

    try {
      await createTransaction({ listingId: id }).unwrap()
      toast.success("Purchase successful!")
      router.push(ROUTES.TRANSACTIONS)
    } catch (err: unknown) {
      const error = err as { data?: { message?: string } }
      toast.error(error.data?.message || "Purchase failed. Please try again.")
    }
  }

  if (error) {
    return (
      <div className="flex min-h-screen flex-col">
        <Header />
        <main className="flex flex-1 items-center justify-center">
          <Alert variant="destructive" className="max-w-md">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>Failed to load listing details. Please try again later.</AlertDescription>
          </Alert>
        </main>
      </div>
    )
  }

  const isOwnListing = user?.id === listing?.sellerId
  const canPurchase = isAuthenticated && !isOwnListing && listing?.status === "active"

  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1">
        <div className="container mx-auto px-4 py-8">
          <Button variant="ghost" onClick={() => router.back()} className="mb-6 gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to Marketplace
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
          ) : listing ? (
            <div className="grid gap-8 lg:grid-cols-2">
              {/* Images */}
              <div className="space-y-4">
                <div className="aspect-square overflow-hidden rounded-lg border border-border bg-muted">
                  {listing.photos?.[0] || listing.model?.images?.[0] ? (
                    <img
                      src={listing.photos?.[0] || listing.model?.images?.[0]}
                      alt={listing.model?.name || "Listing"}
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
                  <div className="mb-2 flex items-start justify-between gap-4">
                    <h1 className="text-3xl font-bold text-balance">{listing.model?.name || "Unknown Model"}</h1>
                    <Badge variant={listing.status === "active" ? "default" : "secondary"} className="shrink-0">
                      {listing.status}
                    </Badge>
                  </div>
                  <p className="text-3xl font-bold text-primary">${listing.price.toFixed(2)}</p>
                </div>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">Listing Details</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid gap-4 sm:grid-cols-2">
                      <div>
                        <p className="text-sm text-muted-foreground">Condition</p>
                        <p className="font-medium capitalize">{listing.condition.replace("_", " ")}</p>
                      </div>
                      {listing.seller && (
                        <div>
                          <p className="text-sm text-muted-foreground">Seller</p>
                          <p className="flex items-center gap-2 font-medium">
                            <User className="h-4 w-4" />
                            {listing.seller.username}
                          </p>
                        </div>
                      )}
                    </div>
                    {listing.description && (
                      <div>
                        <p className="text-sm text-muted-foreground">Description</p>
                        <p className="text-pretty">{listing.description}</p>
                      </div>
                    )}
                  </CardContent>
                </Card>

                {canPurchase && (
                  <Button onClick={handlePurchase} disabled={isPurchasing} size="lg" className="w-full gap-2">
                    <ShoppingCart className="h-5 w-5" />
                    {isPurchasing ? "Processing..." : "Purchase Now"}
                  </Button>
                )}

                {!isAuthenticated && (
                  <Alert>
                    <AlertDescription>
                      <Link href={ROUTES.LOGIN} className="font-medium text-primary hover:underline">
                        Sign in
                      </Link>{" "}
                      to purchase this item
                    </AlertDescription>
                  </Alert>
                )}
              </div>
            </div>
          ) : null}
        </div>
      </main>
    </div>
  )
}
