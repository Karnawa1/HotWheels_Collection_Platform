export interface User {
  id: string
  username: string
  email: string
  role: "collector" | "trader" | "admin" | "moderator"
  avatar?: string
  createdAt: string
  updatedAt: string
}

export interface Manufacturer {
  id: string
  name: string
  country?: string
}

export interface Series {
  id: string
  name: string
  year?: number
  description?: string
}

export interface Casting {
  id: string
  name: string
  designer?: string
  firstAppearance?: number
}

export interface CarModel {
  id: string
  name: string
  year: number
  color: string
  rarity: "common" | "uncommon" | "rare" | "super_rare" | "chase"
  images: string[]
  manufacturer?: Manufacturer
  series?: Series
  casting?: Casting
  description?: string
  estimatedValue?: number
  createdAt: string
  updatedAt: string
}

export interface CollectionItem {
  id: string
  userId: string
  modelId: string
  model?: CarModel
  condition: "mint" | "near_mint" | "excellent" | "good" | "fair"
  purchasePrice?: number
  purchaseDate?: string
  notes?: string
  customPhotos?: string[]
  createdAt: string
  updatedAt: string
}

export interface WishlistItem {
  id: string
  userId: string
  modelId: string
  model?: CarModel
  priority: "low" | "medium" | "high"
  maxPrice?: number
  notes?: string
  createdAt: string
}

export interface Listing {
  id: string
  sellerId: string
  seller?: User
  modelId: string
  model?: CarModel
  collectionItemId?: string
  condition: "mint" | "near_mint" | "excellent" | "good" | "fair"
  price: number
  description?: string
  photos?: string[]
  status: "active" | "sold" | "cancelled" | "expired"
  expiresAt?: string
  createdAt: string
  updatedAt: string
}

export interface Transaction {
  id: string
  listingId: string
  listing?: Listing
  buyerId: string
  buyer?: User
  sellerId: string
  seller?: User
  amount: number
  status: "pending" | "completed" | "cancelled"
  createdAt: string
  completedAt?: string
}

export interface Review {
  id: string
  transactionId: string
  transaction?: Transaction
  reviewerId: string
  reviewer?: User
  revieweeId: string
  reviewee?: User
  rating: number
  comment?: string
  createdAt: string
}

export interface PaginatedResponse<T> {
  data: T[]
  page: number
  perPage: number
  total: number
  totalPages: number
}

export interface ApiError {
  message: string
  statusCode: number
  errors?: Record<string, string[]>
}
