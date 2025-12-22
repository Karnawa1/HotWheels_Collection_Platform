"use client"

import type React from "react"
import { useEffect } from "react"

import { Provider, useDispatch } from "react-redux"
import { ThemeProvider as NextThemesProvider } from "next-themes"
import { store, type AppDispatch } from "@/shared/store"
import { getAccessToken } from "@/shared/api/base-query"
import { hydrateAuth, setUser, clearCredentials } from "@/entities/auth/model/auth-slice"
import { authApi } from "@/shared/api/auth-api"

function AuthInitializer({ children }: { children: React.ReactNode }) {
  const dispatch = useDispatch<AppDispatch>()

  useEffect(() => {
    // Check if we have a stored token and hydrate auth state
    const token = getAccessToken()
    if (token) {
      dispatch(hydrateAuth())
      // Fetch user data
      dispatch(authApi.endpoints.getMe.initiate())
        .unwrap()
        .then((user) => {
          dispatch(setUser(user))
        })
        .catch(() => {
          // Token is invalid, clear credentials
          dispatch(clearCredentials())
        })
    }
  }, [dispatch])

  return <>{children}</>
}

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <Provider store={store}>
      <NextThemesProvider attribute="class" defaultTheme="system" enableSystem>
        <AuthInitializer>{children}</AuthInitializer>
      </NextThemesProvider>
    </Provider>
  )
}
