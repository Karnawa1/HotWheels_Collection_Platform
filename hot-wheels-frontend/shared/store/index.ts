import { configureStore } from "@reduxjs/toolkit"
import { authApi } from "@/shared/api/auth-api"
import { catalogApi } from "@/shared/api/catalog-api"
import { collectionApi } from "@/shared/api/collection-api"
import { marketplaceApi } from "@/shared/api/marketplace-api"
import authReducer from "@/entities/auth/model/auth-slice"

export const store = configureStore({
  reducer: {
    auth: authReducer,
    [authApi.reducerPath]: authApi.reducer,
    [catalogApi.reducerPath]: catalogApi.reducer,
    [collectionApi.reducerPath]: collectionApi.reducer,
    [marketplaceApi.reducerPath]: marketplaceApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(
      authApi.middleware,
      catalogApi.middleware,
      collectionApi.middleware,
      marketplaceApi.middleware,
    ),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
