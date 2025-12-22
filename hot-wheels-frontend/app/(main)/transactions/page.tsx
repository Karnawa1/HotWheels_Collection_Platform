"use client"

import { useState } from "react"
import { AuthGuard } from "@/shared/components/auth-guard"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { useGetPurchasesQuery, useGetSalesQuery } from "@/shared/api/marketplace-api"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Skeleton } from "@/components/ui/skeleton"
import { AlertCircle, ShoppingBag } from "lucide-react"

export default function TransactionsPage() {
  const [activeTab, setActiveTab] = useState("purchases")
  const { data: purchases, isLoading: purchasesLoading, error: purchasesError } = useGetPurchasesQuery()
  const { data: sales, isLoading: salesLoading, error: salesError } = useGetSalesQuery()

  const statusColors = {
    pending: "bg-chart-4/20 text-chart-4",
    completed: "bg-chart-2/20 text-chart-2",
    cancelled: "bg-secondary text-secondary-foreground",
  }

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="mb-2 text-3xl font-bold">Transactions</h1>
          <p className="text-muted-foreground">View your purchase and sales history</p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="mb-6">
            <TabsTrigger value="purchases">Purchases</TabsTrigger>
            <TabsTrigger value="sales">Sales</TabsTrigger>
              </TabsList>

              <TabsContent value="purchases">
                {purchasesError && (
                  <Alert variant="destructive" className="mb-6">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>Failed to load purchases. Please try again later.</AlertDescription>
                  </Alert>
                )}

                {purchasesLoading ? (
                  <Card>
                    <CardContent className="p-6">
                      <div className="space-y-4">
                        {[1, 2, 3, 4, 5].map((i) => (
                          <Skeleton key={i} className="h-16 w-full" />
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                ) : purchases?.length === 0 ? (
                  <Card>
                    <CardContent className="flex min-h-64 items-center justify-center p-6">
                      <div className="text-center">
                        <ShoppingBag className="mx-auto mb-4 h-12 w-12 text-muted-foreground" />
                        <p className="text-lg font-medium">No purchases yet</p>
                        <p className="text-sm text-muted-foreground">Browse the marketplace to start shopping</p>
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
                              <TableHead>Item</TableHead>
                              <TableHead>Seller</TableHead>
                              <TableHead>Amount</TableHead>
                              <TableHead>Status</TableHead>
                              <TableHead>Date</TableHead>
                            </TableRow>
                          </TableHeader>
                          <TableBody>
                            {purchases?.map((transaction) => (
                              <TableRow key={transaction.id}>
                                <TableCell className="font-medium">
                                  {transaction.listing?.model?.name || "Unknown"}
                                </TableCell>
                                <TableCell>{transaction.seller?.username || "Unknown"}</TableCell>
                                <TableCell>${transaction.amount.toFixed(2)}</TableCell>
                                <TableCell>
                                  <Badge variant="secondary" className={statusColors[transaction.status]}>
                                    {transaction.status}
                                  </Badge>
                                </TableCell>
                                <TableCell>{new Date(transaction.createdAt).toLocaleDateString()}</TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </TabsContent>

              <TabsContent value="sales">
                {salesError && (
                  <Alert variant="destructive" className="mb-6">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>Failed to load sales. Please try again later.</AlertDescription>
                  </Alert>
                )}

                {salesLoading ? (
                  <Card>
                    <CardContent className="p-6">
                      <div className="space-y-4">
                        {[1, 2, 3, 4, 5].map((i) => (
                          <Skeleton key={i} className="h-16 w-full" />
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                ) : sales?.length === 0 ? (
                  <Card>
                    <CardContent className="flex min-h-64 items-center justify-center p-6">
                      <div className="text-center">
                        <ShoppingBag className="mx-auto mb-4 h-12 w-12 text-muted-foreground" />
                        <p className="text-lg font-medium">No sales yet</p>
                        <p className="text-sm text-muted-foreground">Create a listing to start selling</p>
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
                              <TableHead>Item</TableHead>
                              <TableHead>Buyer</TableHead>
                              <TableHead>Amount</TableHead>
                              <TableHead>Status</TableHead>
                              <TableHead>Date</TableHead>
                            </TableRow>
                          </TableHeader>
                          <TableBody>
                            {sales?.map((transaction) => (
                              <TableRow key={transaction.id}>
                                <TableCell className="font-medium">
                                  {transaction.listing?.model?.name || "Unknown"}
                                </TableCell>
                                <TableCell>{transaction.buyer?.username || "Unknown"}</TableCell>
                                <TableCell>${transaction.amount.toFixed(2)}</TableCell>
                                <TableCell>
                                  <Badge variant="secondary" className={statusColors[transaction.status]}>
                                    {transaction.status}
                                  </Badge>
                                </TableCell>
                                <TableCell>{new Date(transaction.createdAt).toLocaleDateString()}</TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </TabsContent>
            </Tabs>
          </div>
    </AuthGuard>
  )
}
