import { fetchBaseQuery } from "@reduxjs/toolkit/query/react"
import type { BaseQueryFn, FetchArgs, FetchBaseQueryError } from "@reduxjs/toolkit/query"
import { API_BASE_URL } from "@/shared/lib/constants"
import { setCredentials, clearCredentials } from "@/entities/auth/model/auth-slice"

const ACCESS_TOKEN_KEY = "hw_access_token"
const REFRESH_TOKEN_KEY = "hw_refresh_token"

export const setAccessToken = (token: string | null) => {
  if (typeof window !== "undefined") {
    if (token) {
      localStorage.setItem(ACCESS_TOKEN_KEY, token)
    } else {
      localStorage.removeItem(ACCESS_TOKEN_KEY)
    }
  }
}

export const getAccessToken = () => {
  if (typeof window !== "undefined") {
    return localStorage.getItem(ACCESS_TOKEN_KEY)
  }
  return null
}

export const setRefreshToken = (token: string | null) => {
  if (typeof window !== "undefined") {
    if (token) {
      localStorage.setItem(REFRESH_TOKEN_KEY, token)
    } else {
      localStorage.removeItem(REFRESH_TOKEN_KEY)
    }
  }
}

export const getRefreshToken = () => {
  if (typeof window !== "undefined") {
    return localStorage.getItem(REFRESH_TOKEN_KEY)
  }
  return null
}

const baseQuery = fetchBaseQuery({
  baseUrl: API_BASE_URL,
  prepareHeaders: (headers) => {
    const token = getAccessToken()
    if (token) {
      headers.set("Authorization", `Bearer ${token}`)
    }
    return headers
  },
})

// Create a separate baseQuery for refresh that uses the refresh token
const refreshBaseQuery = fetchBaseQuery({
  baseUrl: API_BASE_URL,
  prepareHeaders: (headers) => {
    const token = getRefreshToken()
    if (token) {
      headers.set("Authorization", `Bearer ${token}`)
    }
    return headers
  },
})

export const baseQueryWithReauth: BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError> = async (
  args,
  api,
  extraOptions,
) => {
  let result = await baseQuery(args, api, extraOptions)

  if (result.error && result.error.status === 401) {
    // Check if we have a refresh token
    const currentRefreshToken = getRefreshToken()
    if (!currentRefreshToken) {
      // No refresh token, redirect to login
      api.dispatch(clearCredentials())
      setAccessToken(null)
      setRefreshToken(null)
      if (typeof window !== "undefined") {
        window.location.href = "/auth/login"
      }
      return result
    }

    // Try to refresh token using the refresh token
    const refreshResult = await refreshBaseQuery({ url: "/auth/refresh", method: "POST" }, api, extraOptions)

    if (refreshResult.data) {
      const responseData = refreshResult.data as { data?: { accessToken: string }; accessToken?: string }
      // Handle both wrapped response (data.accessToken) and direct response
      const newToken = responseData.data?.accessToken || responseData.accessToken
      if (newToken) {
        setAccessToken(newToken)
        api.dispatch(setCredentials({ accessToken: newToken }))

        // Retry the original query
        result = await baseQuery(args, api, extraOptions)
      }
    } else {
      // Refresh failed, clear credentials and redirect to login
      api.dispatch(clearCredentials())
      setAccessToken(null)
      setRefreshToken(null)
      if (typeof window !== "undefined") {
        window.location.href = "/auth/login"
      }
    }
  }

  return result
}
