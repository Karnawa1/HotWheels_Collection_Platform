"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Header } from "@/widgets/header"
import { AuthGuard } from "@/shared/components/auth-guard"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Spinner } from "@/shared/ui/spinner"
import { useCreateListingMutation } from "@/shared/api/marketplace-api"
import { useGetCollectionQuery } from "@/shared/api/collection-api"
import { listingSchema, type ListingInput } from "@/shared/lib/validations"
import { CONDITION_OPTIONS, ROUTES } from "@/shared/lib/constants"
import { toast } from "sonner"
import { ArrowLeft } from "lucide-react"

export default function CreateListingPage() {
  const router = useRouter()
  const [createListing, { isLoading }] = useCreateListingMutation()
  const { data: collection } = useGetCollectionQuery()
  const [useCollectionItem, setUseCollectionItem] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
  } = useForm<ListingInput>({
    resolver: zodResolver(listingSchema),
    defaultValues: {
      condition: "mint",
    },
  })

  const selectedCollectionItemId = watch("collectionItemId")

  const onSubmit = async (data: ListingInput) => {
    try {
      await createListing(data).unwrap()
      toast.success("Listing created successfully!")
      router.push(ROUTES.MARKETPLACE)
    } catch (err: unknown) {
      const error = err as { data?: { message?: string } }
      toast.error(error.data?.message || "Failed to create listing. Please try again.")
    }
  }

  return (
    <AuthGuard>
      <div className="flex min-h-screen flex-col">
        <Header />
        <main className="flex-1">
          <div className="container mx-auto max-w-2xl px-4 py-8">
            <Button variant="ghost" onClick={() => router.back()} className="mb-6 gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back
            </Button>

            <Card>
              <CardHeader>
                <CardTitle>Create Marketplace Listing</CardTitle>
                <CardDescription>List a Hot Wheels model for sale in the marketplace</CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                  {/* Source Selection */}
                  <div className="space-y-2">
                    <Label>Source</Label>
                    <div className="flex gap-4">
                      <Button
                        type="button"
                        variant={!useCollectionItem ? "default" : "outline"}
                        onClick={() => {
                          setUseCollectionItem(false)
                          setValue("collectionItemId", undefined)
                        }}
                        className="flex-1"
                      >
                        Direct Model ID
                      </Button>
                      <Button
                        type="button"
                        variant={useCollectionItem ? "default" : "outline"}
                        onClick={() => setUseCollectionItem(true)}
                        className="flex-1"
                      >
                        From Collection
                      </Button>
                    </div>
                  </div>

                  {/* Model Selection */}
                  {useCollectionItem ? (
                    <div className="space-y-2">
                      <Label htmlFor="collectionItemId">Collection Item</Label>
                      <Select
                        value={selectedCollectionItemId}
                        onValueChange={(value) => {
                          setValue("collectionItemId", value)
                          const item = collection?.find((c) => c.id === value)
                          if (item) {
                            setValue("modelId", item.modelId)
                            setValue("condition", item.condition)
                          }
                        }}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select from your collection" />
                        </SelectTrigger>
                        <SelectContent>
                          {collection?.map((item) => (
                            <SelectItem key={item.id} value={item.id}>
                              {item.model?.name} ({item.condition})
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      {errors.collectionItemId && (
                        <p className="text-sm text-destructive">{errors.collectionItemId.message}</p>
                      )}
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <Label htmlFor="modelId">Model ID</Label>
                      <Input
                        id="modelId"
                        placeholder="Enter model ID from catalog"
                        {...register("modelId")}
                        className={errors.modelId ? "border-destructive" : ""}
                      />
                      {errors.modelId && <p className="text-sm text-destructive">{errors.modelId.message}</p>}
                    </div>
                  )}

                  {/* Condition */}
                  <div className="space-y-2">
                    <Label htmlFor="condition">Condition</Label>
                    <Select
                      value={watch("condition")}
                      onValueChange={(value: "mint" | "near_mint" | "excellent" | "good" | "fair") =>
                        setValue("condition", value)
                      }
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {CONDITION_OPTIONS.map((option) => (
                          <SelectItem key={option.value} value={option.value}>
                            {option.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    {errors.condition && <p className="text-sm text-destructive">{errors.condition.message}</p>}
                  </div>

                  {/* Price */}
                  <div className="space-y-2">
                    <Label htmlFor="price">Price ($)</Label>
                    <Input
                      id="price"
                      type="number"
                      step="0.01"
                      placeholder="0.00"
                      {...register("price", { valueAsNumber: true })}
                      className={errors.price ? "border-destructive" : ""}
                    />
                    {errors.price && <p className="text-sm text-destructive">{errors.price.message}</p>}
                  </div>

                  {/* Description */}
                  <div className="space-y-2">
                    <Label htmlFor="description">Description (Optional)</Label>
                    <Textarea
                      id="description"
                      placeholder="Describe the item condition, packaging, or other details..."
                      rows={4}
                      {...register("description")}
                    />
                    {errors.description && <p className="text-sm text-destructive">{errors.description.message}</p>}
                  </div>

                  <div className="flex gap-4">
                    <Button type="submit" disabled={isLoading} className="flex-1">
                      {isLoading ? <Spinner size="sm" className="mr-2" /> : null}
                      Create Listing
                    </Button>
                    <Button type="button" variant="outline" onClick={() => router.back()} className="flex-1">
                      Cancel
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </AuthGuard>
  )
}
