"use client"

import { AuthGuard } from "@/shared/components/auth-guard"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Card, CardContent } from "@/components/ui/card"
import { useGetWishlistQuery, useRemoveFromWishlistMutation } from "@/shared/api/collection-api"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Skeleton } from "@/components/ui/skeleton"
import { AlertCircle, Trash2, Heart } from "lucide-react"
import { toast } from "sonner"
import Link from "next/link"
import { ROUTES } from "@/shared/lib/constants"

export default function WishlistPage() {
  const { data: wishlist, isLoading, error } = useGetWishlistQuery()
  const [removeFromWishlist, { isLoading: isRemoving }] = useRemoveFromWishlistMutation()

  const handleRemove = async (id: string) => {
    if (confirm("Are you sure you want to remove this item from your wishlist?")) {
      try {
        await removeFromWishlist(id).unwrap()
        toast.success("Item removed from wishlist")
      } catch (err: unknown) {
        const error = err as { data?: { message?: string } }
        toast.error(error.data?.message || "Failed to remove item")
      }
    }
  }

  const priorityColors = {
    low: "bg-secondary text-secondary-foreground",
    medium: "bg-chart-4/20 text-chart-4",
    high: "bg-primary/20 text-primary",
  }

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="mb-2 text-3xl font-bold">My Wishlist</h1>
          <p className="text-muted-foreground">Track models you want to add to your collection</p>
        </div>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>Failed to load wishlist. Please try again later.</AlertDescription>
          </Alert>
        )}

            {isLoading ? (
              <Card>
                <CardContent className="p-6">
                  <div className="space-y-4">
                    {[1, 2, 3, 4, 5].map((i) => (
                      <Skeleton key={i} className="h-16 w-full" />
                    ))}
                  </div>
                </CardContent>
              </Card>
            ) : wishlist?.length === 0 ? (
              <Card>
                <CardContent className="flex min-h-64 items-center justify-center p-6">
                  <div className="text-center">
                    <Heart className="mx-auto mb-4 h-12 w-12 text-muted-foreground" />
                    <p className="text-lg font-medium">Your wishlist is empty</p>
                    <p className="text-sm text-muted-foreground">Start adding models from the catalog</p>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardContent className="p-0">
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Model</TableHead>
                          <TableHead>Year</TableHead>
                          <TableHead>Rarity</TableHead>
                          <TableHead>Priority</TableHead>
                          <TableHead>Max Price</TableHead>
                          <TableHead>Added</TableHead>
                          <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {wishlist?.map((item) => (
                          <TableRow key={item.id}>
                            <TableCell>
                              <Link
                                href={ROUTES.CATALOG_DETAIL(item.modelId)}
                                className="font-medium hover:text-primary hover:underline"
                              >
                                {item.model?.name || "Unknown"}
                              </Link>
                            </TableCell>
                            <TableCell>{item.model?.year}</TableCell>
                            <TableCell>
                              <Badge variant="secondary" className="capitalize">
                                {item.model?.rarity.replace("_", " ")}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <Badge variant="secondary" className={priorityColors[item.priority]}>
                                {item.priority}
                              </Badge>
                            </TableCell>
                            <TableCell>{item.maxPrice ? `$${item.maxPrice.toFixed(2)}` : "N/A"}</TableCell>
                            <TableCell>{new Date(item.createdAt).toLocaleDateString()}</TableCell>
                            <TableCell className="text-right">
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleRemove(item.id)}
                                disabled={isRemoving}
                                className="text-destructive hover:bg-destructive/10 hover:text-destructive"
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
    </AuthGuard>
  )
}
