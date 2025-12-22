import { createApi } from "@reduxjs/toolkit/query/react"
import { baseQueryWithReauth } from "./base-query"
import type { CollectionItem, WishlistItem } from "@/shared/types"

export interface CollectionStats {
  totalItems: number
  totalValue: number
  rarityDistribution: Record<string, number>
  yearDistribution: Record<string, number>
}

// Backend response wrapper type
interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
  timestamp?: string
}

export const collectionApi = createApi({
  reducerPath: "collectionApi",
  baseQuery: baseQueryWithReauth,
  tagTypes: ["Collection", "Wishlist", "Stats"],
  endpoints: (builder) => ({
    getCollection: builder.query<CollectionItem[], void>({
      query: () => "/collections",
      transformResponse: (response: ApiResponse<{ items: CollectionItem[] }>) => response.data.items,
      providesTags: (result) =>
        result
          ? [...result.map(({ id }) => ({ type: "Collection" as const, id })), { type: "Collection", id: "LIST" }]
          : [{ type: "Collection", id: "LIST" }],
    }),
    addToCollection: builder.mutation<CollectionItem, Partial<CollectionItem>>({
      query: (data) => ({
        url: "/collections",
        method: "POST",
        body: data,
      }),
      transformResponse: (response: ApiResponse<{ collection_item: CollectionItem }>) => response.data.collection_item,
      invalidatesTags: [{ type: "Collection", id: "LIST" }, "Stats"],
    }),
    updateCollectionItem: builder.mutation<CollectionItem, { id: string; data: Partial<CollectionItem> }>({
      query: ({ id, data }) => ({
        url: `/collections/${id}`,
        method: "PUT",
        body: data,
      }),
      transformResponse: (response: ApiResponse<{ collection_item: CollectionItem }>) => response.data.collection_item,
      invalidatesTags: (_result, _error, { id }) => [
        { type: "Collection", id },
        { type: "Collection", id: "LIST" },
        "Stats",
      ],
    }),
    removeFromCollection: builder.mutation<void, string>({
      query: (id) => ({
        url: `/collections/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: [{ type: "Collection", id: "LIST" }, "Stats"],
    }),
    getCollectionStats: builder.query<CollectionStats, void>({
      query: () => "/collections/stats",
      transformResponse: (response: ApiResponse<{ stats: CollectionStats }>) => response.data.stats,
      providesTags: ["Stats"],
    }),
    getWishlist: builder.query<WishlistItem[], void>({
      query: () => "/collections/wishlist",
      transformResponse: (response: ApiResponse<{ items: WishlistItem[] }>) => response.data.items,
      providesTags: (result) =>
        result
          ? [...result.map(({ id }) => ({ type: "Wishlist" as const, id })), { type: "Wishlist", id: "LIST" }]
          : [{ type: "Wishlist", id: "LIST" }],
    }),
    addToWishlist: builder.mutation<WishlistItem, Partial<WishlistItem>>({
      query: (data) => ({
        url: "/collections/wishlist",
        method: "POST",
        body: data,
      }),
      transformResponse: (response: ApiResponse<{ wishlist_item: WishlistItem }>) => response.data.wishlist_item,
      invalidatesTags: [{ type: "Wishlist", id: "LIST" }],
    }),
    removeFromWishlist: builder.mutation<void, string>({
      query: (id) => ({
        url: `/collections/wishlist/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: [{ type: "Wishlist", id: "LIST" }],
    }),
  }),
})

export const {
  useGetCollectionQuery,
  useAddToCollectionMutation,
  useUpdateCollectionItemMutation,
  useRemoveFromCollectionMutation,
  useGetCollectionStatsQuery,
  useGetWishlistQuery,
  useAddToWishlistMutation,
  useRemoveFromWishlistMutation,
} = collectionApi
