import { createApi } from "@reduxjs/toolkit/query/react"
import { baseQueryWithReauth } from "./base-query"
import type { CarModel, PaginatedResponse } from "@/shared/types"

export interface CatalogFilters {
  q?: string
  page?: number
  per_page?: number
  year_min?: number
  year_max?: number
  rarity?: string
  color?: string
  series?: string
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

// Backend car model format (snake_case)
interface BackendCarModel {
  model_id: number
  casting_id: number
  series_id?: number
  release_year: number
  color: string
  tampo_design?: string
  wheel_type?: string
  base_color?: string
  window_color?: string
  interior_color?: string
  production_code?: string
  sku?: string
  rarity_level?: string
  estimated_production_quantity?: number
  msrp?: number
  created_at?: string
  updated_at?: string
  casting_name?: string
  series_name?: string
}

// Transform backend model to frontend format
function transformCarModel(backend: BackendCarModel): CarModel {
  return {
    id: String(backend.model_id),
    name: backend.casting_name || `Model ${backend.model_id}`,
    year: backend.release_year,
    color: backend.color,
    rarity: (backend.rarity_level?.toLowerCase().replace(/ /g, "_") || "common") as CarModel["rarity"],
    images: [],
    series: backend.series_name ? { id: String(backend.series_id), name: backend.series_name } : undefined,
    description: backend.tampo_design,
    estimatedValue: backend.msrp,
    createdAt: backend.created_at || new Date().toISOString(),
    updatedAt: backend.updated_at || new Date().toISOString(),
  }
}

export const catalogApi = createApi({
  reducerPath: "catalogApi",
  baseQuery: baseQueryWithReauth,
  tagTypes: ["Catalog"],
  endpoints: (builder) => ({
    getModels: builder.query<PaginatedResponse<CarModel>, CatalogFilters>({
      query: (filters) => {
        const params = new URLSearchParams()
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null && value !== "") {
            params.append(key, String(value))
          }
        })
        return `/catalog/models?${params.toString()}`
      },
      transformResponse: (response: ApiResponse<BackendPaginatedData<BackendCarModel>>): PaginatedResponse<CarModel> => ({
        data: response.data.items.map(transformCarModel),
        page: response.data.pagination.page,
        perPage: response.data.pagination.per_page,
        total: response.data.pagination.total_items,
        totalPages: response.data.pagination.total_pages,
      }),
      providesTags: (result) =>
        result?.data
          ? [...result.data.map(({ id }) => ({ type: "Catalog" as const, id })), { type: "Catalog", id: "LIST" }]
          : [{ type: "Catalog", id: "LIST" }],
    }),
    getModelById: builder.query<CarModel, string>({
      query: (id) => `/catalog/models/${id}`,
      transformResponse: (response: ApiResponse<{ model: BackendCarModel }>) => transformCarModel(response.data.model),
      providesTags: (_result, _error, id) => [{ type: "Catalog", id }],
    }),
  }),
})

export const { useGetModelsQuery, useGetModelByIdQuery } = catalogApi
