import Link from "next/link"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import type { Listing } from "@/shared/types"
import { ROUTES } from "@/shared/lib/constants"

interface ListingCardProps {
  listing: Listing
}

export function ListingCard({ listing }: ListingCardProps) {
  return (
    <Link href={ROUTES.MARKETPLACE_DETAIL(listing.id)}>
      <Card className="group h-full overflow-hidden transition-all hover:shadow-md">
        <CardHeader className="p-0">
          <div className="aspect-video w-full overflow-hidden bg-muted">
            {listing.photos?.[0] || listing.model?.images?.[0] ? (
              <img
                src={listing.photos?.[0] || listing.model?.images?.[0]}
                alt={listing.model?.name || "Listing"}
                className="h-full w-full object-cover transition-transform group-hover:scale-105"
              />
            ) : (
              <div className="flex h-full w-full items-center justify-center text-muted-foreground">No Image</div>
            )}
          </div>
        </CardHeader>
        <CardContent className="p-4">
          <div className="mb-2 flex items-start justify-between gap-2">
            <CardTitle className="line-clamp-1 text-base">{listing.model?.name || "Unknown Model"}</CardTitle>
            <Badge variant="secondary">{listing.condition}</Badge>
          </div>
          <div className="space-y-1 text-sm text-muted-foreground">
            {listing.seller && <p>Seller: {listing.seller.username}</p>}
            {listing.description && <p className="line-clamp-2">{listing.description}</p>}
          </div>
        </CardContent>
        <CardFooter className="border-t border-border bg-muted/50 p-4">
          <p className="text-lg font-bold text-primary">
            {listing.price != null ? `$${listing.price.toFixed(2)}` : "Price on request"}
          </p>
        </CardFooter>
      </Card>
    </Link>
  )
}
