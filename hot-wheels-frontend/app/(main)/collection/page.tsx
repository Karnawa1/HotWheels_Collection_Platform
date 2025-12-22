"use client"
import { AuthGuard } from "@/shared/components/auth-guard"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  useGetCollectionQuery,
  useRemoveFromCollectionMutation,
  useGetCollectionStatsQuery,
} from "@/shared/api/collection-api"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Skeleton } from "@/components/ui/skeleton"
import { AlertCircle, Trash2, Package, DollarSign, TrendingUp } from "lucide-react"
import { toast } from "sonner"

export default function CollectionPage() {
  const { data: collection, isLoading, error } = useGetCollectionQuery()
  const { data: stats, isLoading: statsLoading } = useGetCollectionStatsQuery()
  const [removeFromCollection, { isLoading: isRemoving }] = useRemoveFromCollectionMutation()

  const handleRemove = async (id: string) => {
    if (confirm("Are you sure you want to remove this item from your collection?")) {
      try {
        await removeFromCollection(id).unwrap()
        toast.success("Item removed from collection")
      } catch (err: unknown) {
        const error = err as { data?: { message?: string } }
        toast.error(error.data?.message || "Failed to remove item")
      }
    }
  }

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
            <div className="mb-8">
              <h1 className="mb-2 text-3xl font-bold">My Collection</h1>
              <p className="text-muted-foreground">Manage your Hot Wheels collection</p>
            </div>

            {/* Stats Cards */}
            {statsLoading ? (
              <div className="mb-8 grid gap-6 md:grid-cols-3">
                {[1, 2, 3].map((i) => (
                  <Card key={i}>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <Skeleton className="h-4 w-24" />
                      <Skeleton className="h-4 w-4" />
                    </CardHeader>
                    <CardContent>
                      <Skeleton className="h-8 w-20" />
                    </CardContent>
                  </Card>
                ))}
              </div>
            ) : (
              stats && (
                <div className="mb-8 grid gap-6 md:grid-cols-3">
                  <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium">Total Items</CardTitle>
                      <Package className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">{stats.totalItems}</div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium">Total Value</CardTitle>
                      <DollarSign className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">${(stats.totalValue ?? 0).toFixed(2)}</div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium">Avg. Value</CardTitle>
                      <TrendingUp className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">
                        ${stats.totalItems > 0 ? ((stats.totalValue ?? 0) / stats.totalItems).toFixed(2) : "0.00"}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )
            )}

            {error && (
              <Alert variant="destructive" className="mb-6">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>Failed to load collection. Please try again later.</AlertDescription>
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
            ) : collection?.length === 0 ? (
              <Card>
                <CardContent className="flex min-h-64 items-center justify-center p-6">
                  <div className="text-center">
                    <Package className="mx-auto mb-4 h-12 w-12 text-muted-foreground" />
                    <p className="text-lg font-medium">Your collection is empty</p>
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
                          <TableHead>Condition</TableHead>
                          <TableHead>Purchase Price</TableHead>
                          <TableHead>Est. Value</TableHead>
                          <TableHead>Added</TableHead>
                          <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {collection?.map((item) => (
                          <TableRow key={item.id}>
                            <TableCell className="font-medium">{item.model?.name || "Unknown"}</TableCell>
                            <TableCell>{item.model?.year}</TableCell>
                            <TableCell>
                              <Badge variant="secondary" className="capitalize">
                                {item.condition.replace("_", " ")}
                              </Badge>
                            </TableCell>
                            <TableCell>{item.purchasePrice ? `$${item.purchasePrice.toFixed(2)}` : "N/A"}</TableCell>
                            <TableCell>
                              {item.model?.estimatedValue ? `$${item.model.estimatedValue.toFixed(2)}` : "N/A"}
                            </TableCell>
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
