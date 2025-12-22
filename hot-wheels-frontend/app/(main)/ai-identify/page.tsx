"use client"

import { useState } from "react"
import { Header } from "@/widgets/header"
import { AuthGuard } from "@/shared/components/auth-guard"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Spinner } from "@/shared/ui/spinner"
import { AlertCircle, Camera, Search } from "lucide-react"
import { AI_API_BASE_URL, ROUTES } from "@/shared/lib/constants"
import { toast } from "sonner"
import Link from "next/link"

interface IdentificationResult {
  modelId: string
  modelName: string
  confidence: number
  year?: number
  series?: string
}

export default function AIIdentifyPage() {
  const [imageUrl, setImageUrl] = useState("")
  const [isIdentifying, setIsIdentifying] = useState(false)
  const [results, setResults] = useState<IdentificationResult[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleIdentify = async () => {
    if (!imageUrl.trim()) {
      toast.error("Please enter an image URL")
      return
    }

    setIsIdentifying(true)
    setError(null)
    setResults(null)

    try {
      const response = await fetch(`${AI_API_BASE_URL}/identify`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          imageUrl,
        }),
      })

      if (!response.ok) {
        throw new Error("Failed to identify model")
      }

      const data = await response.json()
      setResults(data.results || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to identify model")
      toast.error("Failed to identify model. Please try again.")
    } finally {
      setIsIdentifying(false)
    }
  }

  return (
    <AuthGuard>
      <div className="flex min-h-screen flex-col">
        <Header />
        <main className="flex-1">
          <div className="container mx-auto max-w-4xl px-4 py-8">
            <div className="mb-8 text-center">
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
                <Camera className="h-8 w-8 text-primary" />
              </div>
              <h1 className="mb-2 text-3xl font-bold">AI Model Identification</h1>
              <p className="text-muted-foreground">Upload a photo to identify Hot Wheels models using AI</p>
            </div>

            <Card className="mb-6">
              <CardHeader>
                <CardTitle>Upload Image</CardTitle>
                <CardDescription>Enter the URL of a Hot Wheels image to identify</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="imageUrl">Image URL</Label>
                  <Input
                    id="imageUrl"
                    type="url"
                    placeholder="https://example.com/hotwheels.jpg"
                    value={imageUrl}
                    onChange={(e) => setImageUrl(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleIdentify()}
                  />
                </div>

                {imageUrl && (
                  <div className="overflow-hidden rounded-lg border border-border">
                    <img
                      src={imageUrl || "/placeholder.svg"}
                      alt="Preview"
                      className="h-64 w-full object-contain bg-muted"
                      onError={(e) => {
                        e.currentTarget.src = "/placeholder.svg"
                        toast.error("Failed to load image")
                      }}
                    />
                  </div>
                )}

                <Button onClick={handleIdentify} disabled={isIdentifying} className="w-full">
                  {isIdentifying ? <Spinner size="sm" className="mr-2" /> : <Camera className="mr-2 h-4 w-4" />}
                  {isIdentifying ? "Identifying..." : "Identify Model"}
                </Button>
              </CardContent>
            </Card>

            {error && (
              <Alert variant="destructive" className="mb-6">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {results && results.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Identification Results</CardTitle>
                  <CardDescription>Top matches based on AI analysis</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {results.map((result, index) => (
                    <div key={index} className="flex items-center justify-between rounded-lg border border-border p-4">
                      <div className="flex-1">
                        <h3 className="font-semibold">{result.modelName}</h3>
                        <div className="mt-1 flex flex-wrap gap-2 text-sm text-muted-foreground">
                          {result.year && <span>Year: {result.year}</span>}
                          {result.series && <span>Series: {result.series}</span>}
                        </div>
                        <div className="mt-2">
                          <div className="text-sm text-muted-foreground">
                            Confidence: {(result.confidence * 100).toFixed(1)}%
                          </div>
                          <div className="mt-1 h-2 w-full overflow-hidden rounded-full bg-secondary">
                            <div className="h-full bg-primary" style={{ width: `${result.confidence * 100}%` }} />
                          </div>
                        </div>
                      </div>
                      <Button asChild variant="outline" className="ml-4 gap-2 bg-transparent">
                        <Link href={ROUTES.CATALOG_DETAIL(result.modelId)}>
                          <Search className="h-4 w-4" />
                          View
                        </Link>
                      </Button>
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}

            {results && results.length === 0 && (
              <Alert>
                <AlertDescription>No models were identified. Try a different image.</AlertDescription>
              </Alert>
            )}
          </div>
        </main>
      </div>
    </AuthGuard>
  )
}
