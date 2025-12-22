import { createApi } from "@reduxjs/toolkit/query/react"
import { baseQueryWithReauth } from "./base-query"
import type { User } from "@/shared/types"

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
}

export interface AuthResponse {
  user: User
  accessToken: string
  refreshToken: string
}

// Backend response wrapper type
interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
  timestamp?: string
}

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: baseQueryWithReauth,
  tagTypes: ["Auth"],
  endpoints: (builder) => ({
    login: builder.mutation<AuthResponse, LoginRequest>({
      query: (credentials) => ({
        url: "/auth/login",
        method: "POST",
        body: credentials,
      }),
      transformResponse: (response: ApiResponse<AuthResponse>) => response.data,
    }),
    register: builder.mutation<AuthResponse, RegisterRequest>({
      query: (data) => ({
        url: "/auth/register",
        method: "POST",
        body: data,
      }),
      transformResponse: (response: ApiResponse<AuthResponse>) => response.data,
    }),
    logout: builder.mutation<void, void>({
      query: () => ({
        url: "/auth/logout",
        method: "POST",
      }),
    }),
    getMe: builder.query<User, void>({
      query: () => "/auth/me",
      providesTags: ["Auth"],
      transformResponse: (response: ApiResponse<{ user: User }>) => response.data.user,
    }),
    updateProfile: builder.mutation<User, Partial<User>>({
      query: (data) => ({
        url: "/auth/me",
        method: "PUT",
        body: data,
      }),
      invalidatesTags: ["Auth"],
      transformResponse: (response: ApiResponse<{ user: User }>) => response.data.user,
    }),
  }),
})

export const { useLoginMutation, useRegisterMutation, useLogoutMutation, useGetMeQuery, useUpdateProfileMutation } =
  authApi
