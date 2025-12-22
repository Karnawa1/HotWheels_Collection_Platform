import { createApi } from "@reduxjs/toolkit/query/react"
import { baseQueryWithReauth } from "./base-query"
import type { Listing, Transaction, Review, PaginatedResponse } from "@/shared/types"

export interface ListingFilters {
  page?: number
  per_page?: number
  modelId?: string
  condition?: string
  priceMin?: number
  priceMax?: number
}

// Backend response wrapper type
interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
  timestamp?: string
}

// Backend paginated data format
interface BackendPaginatedData<T> {
  items: T[]
  pagination: {
    page: number
    per_page: number
    total_items: number
    total_pages: number
    has_next: boolean
    has_prev: boolean
  }
}

// Backend listing format (snake_case fields)
interface BackendListing {
  listing_id: number
  seller_id: number
  collection_item_id?: number
  model_id: number
  listing_type: string
  price: number | null
  condition: string
  description?: string
  status: string
  views_count: number
  created_at: string
  expires_at?: string
  sold_at?: string
  seller?: {
    username: string
    is_verified: boolean
  }
  car_model?: {
    model_id: number
    name: string
    year: number
    color: string
    rarity: string
    images?: string[]
  }
  photos?: string[]
}

// Transform backend listing to frontend Listing type
function transformListing(item: BackendListing): Listing {
  return {
    id: String(item.listing_id),
    sellerId: String(item.seller_id),
    modelId: String(item.model_id),
    collectionItemId: item.collection_item_id ? String(item.collection_item_id) : undefined,
    condition: item.condition.toLowerCase().replace(" ", "_") as Listing["condition"],
    price: item.price ?? 0,
    description: item.description,
    photos: item.photos,
    status: item.status as Listing["status"],
    createdAt: item.created_at,
    updatedAt: item.created_at,
    expiresAt: item.expires_at,
    seller: item.seller
      ? {
          id: String(item.seller_id),
          username: item.seller.username,
          email: "",
          role: "collector",
          createdAt: "",
          updatedAt: "",
        }
      : undefined,
    model: item.car_model
      ? {
          id: String(item.car_model.model_id),
          name: item.car_model.name,
          year: item.car_model.year,
          color: item.car_model.color,
          rarity: item.car_model.rarity.toLowerCase().replace(" ", "_") as "common" | "uncommon" | "rare" | "super_rare" | "chase",
          images: item.car_model.images || [],
          createdAt: "",
          updatedAt: "",
        }
      : undefined,
  }
}

export const marketplaceApi = createApi({
  reducerPath: "marketplaceApi",
  baseQuery: baseQueryWithReauth,
  tagTypes: ["Listing", "Transaction", "Review"],
  endpoints: (builder) => ({
    getListings: builder.query<PaginatedResponse<Listing>, ListingFilters>({
      query: (filters) => {
        const params = new URLSearchParams()
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null && value !== "") {
            params.append(key, String(value))
          }
        })
        return `/marketplace/listings?${params.toString()}`
      },
      transformResponse: (response: ApiResponse<BackendPaginatedData<BackendListing>>): PaginatedResponse<Listing> => ({
        data: response.data.items.map(transformListing),
        page: response.data.pagination.page,
        perPage: response.data.pagination.per_page,
        total: response.data.pagination.total_items,
        totalPages: response.data.pagination.total_pages,
      }),
      providesTags: (result) =>
        result?.data
          ? [...result.data.map(({ id }) => ({ type: "Listing" as const, id })), { type: "Listing", id: "LIST" }]
          : [{ type: "Listing", id: "LIST" }],
    }),
    getListingById: builder.query<Listing, string>({
      query: (id) => `/marketplace/listings/${id}`,
      transformResponse: (response: ApiResponse<{ listing: BackendListing }>) => transformListing(response.data.listing),
      providesTags: (_result, _error, id) => [{ type: "Listing", id }],
    }),
    createListing: builder.mutation<Listing, Partial<Listing>>({
      query: (data) => ({
        url: "/marketplace/listings",
        method: "POST",
        body: data,
      }),
      transformResponse: (response: ApiResponse<{ listing: Listing }>) => response.data.listing,
      invalidatesTags: [{ type: "Listing", id: "LIST" }],
    }),
    updateListing: builder.mutation<Listing, { id: string; data: Partial<Listing> }>({
      query: ({ id, data }) => ({
        url: `/marketplace/listings/${id}`,
        method: "PUT",
        body: data,
      }),
      transformResponse: (response: ApiResponse<{ listing: Listing }>) => response.data.listing,
      invalidatesTags: (_result, _error, { id }) => [
        { type: "Listing", id },
        { type: "Listing", id: "LIST" },
      ],
    }),
    cancelListing: builder.mutation<void, string>({
      query: (id) => ({
        url: `/marketplace/listings/${id}/cancel`,
        method: "POST",
      }),
      invalidatesTags: (_result, _error, id) => [
        { type: "Listing", id },
        { type: "Listing", id: "LIST" },
      ],
    }),
    createTransaction: builder.mutation<Transaction, { listingId: string }>({
      query: (data) => ({
        url: "/marketplace/transactions",
        method: "POST",
        body: data,
      }),
      transformResponse: (response: ApiResponse<{ transaction: Transaction }>) => response.data.transaction,
      invalidatesTags: [
        { type: "Transaction", id: "LIST" },
        { type: "Listing", id: "LIST" },
      ],
    }),
    getPurchases: builder.query<Transaction[], void>({
      query: () => "/marketplace/transactions/purchases",
      transformResponse: (response: ApiResponse<{ items: Transaction[] }>) => response.data.items,
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "Transaction" as const, id })),
              { type: "Transaction", id: "PURCHASES" },
            ]
          : [{ type: "Transaction", id: "PURCHASES" }],
    }),
    getSales: builder.query<Transaction[], void>({
      query: () => "/marketplace/transactions/sales",
      transformResponse: (response: ApiResponse<{ items: Transaction[] }>) => response.data.items,
      providesTags: (result) =>
        result
          ? [...result.map(({ id }) => ({ type: "Transaction" as const, id })), { type: "Transaction", id: "SALES" }]
          : [{ type: "Transaction", id: "SALES" }],
    }),
    createReview: builder.mutation<Review, Partial<Review>>({
      query: (data) => ({
        url: "/marketplace/reviews",
        method: "POST",
        body: data,
      }),
      transformResponse: (response: ApiResponse<{ review: Review }>) => response.data.review,
      invalidatesTags: [{ type: "Review", id: "LIST" }],
    }),
  }),
})

export const {
  useGetListingsQuery,
  useGetListingByIdQuery,
  useCreateListingMutation,
  useUpdateListingMutation,
  useCancelListingMutation,
  useCreateTransactionMutation,
  useGetPurchasesQuery,
  useGetSalesQuery,
  useCreateReviewMutation,
} = marketplaceApi
