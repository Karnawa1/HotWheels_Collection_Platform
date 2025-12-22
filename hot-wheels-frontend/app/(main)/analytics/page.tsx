"use client"

import { AuthGuard } from "@/shared/components/auth-guard"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useGetCollectionStatsQuery, useGetCollectionQuery } from "@/shared/api/collection-api"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AlertCircle, TrendingUp, Package, DollarSign } from "lucide-react"
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Pie,
  PieChart,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"

export default function AnalyticsPage() {
  const { data: stats, isLoading: statsLoading, error: statsError } = useGetCollectionStatsQuery()
  const { data: collection, isLoading: collectionLoading } = useGetCollectionQuery()

  const rarityColors = {
    common: "#94a3b8",
    uncommon: "#10b981",
    rare: "#3b82f6",
    super_rare: "#f59e0b",
    chase: "#ef4444",
  }

  const rarityData = stats?.rarityDistribution
    ? Object.entries(stats.rarityDistribution).map(([key, value]) => ({
        name: key.replace("_", " "),
        value,
      }))
    : []

  const yearData = stats?.yearDistribution
    ? Object.entries(stats.yearDistribution)
        .map(([key, value]) => ({
          year: key,
          count: value,
        }))
        .sort((a, b) => a.year.localeCompare(b.year))
    : []

  const conditionDistribution = collection?.reduce(
    (acc, item) => {
      acc[item.condition] = (acc[item.condition] || 0) + 1
      return acc
    },
    {} as Record<string, number>,
  )

  const conditionData = conditionDistribution
    ? Object.entries(conditionDistribution).map(([key, value]) => ({
        name: key.replace("_", " "),
        value,
      }))
    : []

  return (
    <AuthGuard>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="mb-2 text-3xl font-bold">Collection Analytics</h1>
          <p className="text-muted-foreground">Insights and statistics about your collection</p>
        </div>

        {statsError && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>Failed to load analytics. Please try again later.</AlertDescription>
              </Alert>
            )}

            {/* Summary Cards */}
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
                      <div className="text-2xl font-bold">${stats.totalValue.toFixed(2)}</div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium">Avg. Value</CardTitle>
                      <TrendingUp className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">
                        ${stats.totalItems > 0 ? (stats.totalValue / stats.totalItems).toFixed(2) : "0.00"}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )
            )}

            {/* Charts */}
            <div className="grid gap-6 lg:grid-cols-2">
              {/* Rarity Distribution */}
              <Card>
                <CardHeader>
                  <CardTitle>Rarity Distribution</CardTitle>
                  <CardDescription>Breakdown of items by rarity level</CardDescription>
                </CardHeader>
                <CardContent>
                  {statsLoading || collectionLoading ? (
                    <Skeleton className="h-80 w-full" />
                  ) : rarityData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={rarityData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {rarityData.map((entry, index) => (
                            <Cell
                              key={`cell-${index}`}
                              fill={
                                rarityColors[entry.name.replace(" ", "_") as keyof typeof rarityColors] || "#94a3b8"
                              }
                            />
                          ))}
                        </Pie>
                        <Tooltip />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="flex h-80 items-center justify-center text-muted-foreground">No data available</div>
                  )}
                </CardContent>
              </Card>

              {/* Condition Distribution */}
              <Card>
                <CardHeader>
                  <CardTitle>Condition Distribution</CardTitle>
                  <CardDescription>Breakdown of items by condition</CardDescription>
                </CardHeader>
                <CardContent>
                  {collectionLoading ? (
                    <Skeleton className="h-80 w-full" />
                  ) : conditionData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={conditionData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="value" fill="hsl(var(--primary))" name="Count" />
                      </BarChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="flex h-80 items-center justify-center text-muted-foreground">No data available</div>
                  )}
                </CardContent>
              </Card>

              {/* Year Distribution */}
              <Card className="lg:col-span-2">
                <CardHeader>
                  <CardTitle>Year Distribution</CardTitle>
                  <CardDescription>Number of items by year of production</CardDescription>
                </CardHeader>
                <CardContent>
                  {statsLoading ? (
                    <Skeleton className="h-80 w-full" />
                  ) : yearData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={yearData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="year" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="count" fill="hsl(var(--chart-1))" name="Count" />
                      </BarChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="flex h-80 items-center justify-center text-muted-foreground">No data available</div>
                  )}
                </CardContent>
              </Card>
            </div>
          </div>
    </AuthGuard>
  )
}
