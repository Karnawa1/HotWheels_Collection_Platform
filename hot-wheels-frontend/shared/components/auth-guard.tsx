"use client"

import type React from "react"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAppSelector } from "@/shared/lib/hooks"
import { useGetMeQuery } from "@/shared/api/auth-api"
import { ROUTES } from "@/shared/lib/constants"
import { Spinner } from "@/shared/ui/spinner"

interface AuthGuardProps {
  children: React.ReactNode
  requireAuth?: boolean
  allowedRoles?: Array<"collector" | "trader" | "admin" | "moderator">
}

export function AuthGuard({ children, requireAuth = true, allowedRoles }: AuthGuardProps) {
  const router = useRouter()
  const { isAuthenticated } = useAppSelector((state) => state.auth)
  const {
    data: user,
    isLoading,
    error,
  } = useGetMeQuery(undefined, {
    skip: !isAuthenticated,
  })

  useEffect(() => {
    if (!isLoading && requireAuth) {
      if (!isAuthenticated || error) {
        router.push(ROUTES.LOGIN)
        return
      }

      if (allowedRoles && user && !allowedRoles.includes(user.role)) {
        router.push(ROUTES.HOME)
      }
    }
  }, [isAuthenticated, isLoading, error, requireAuth, allowedRoles, user, router])

  if (requireAuth && (isLoading || !isAuthenticated)) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Spinner size="lg" />
      </div>
    )
  }

  return <>{children}</>
}
