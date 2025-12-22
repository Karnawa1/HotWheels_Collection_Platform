"use client"

import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { useAppSelector, useAppDispatch } from "@/shared/lib/hooks"
import { useLogoutMutation } from "@/shared/api/auth-api"
import { clearCredentials } from "@/entities/auth/model/auth-slice"
import { ROUTES, APP_NAME } from "@/shared/lib/constants"
import { toast } from "sonner"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { User, LogOut, Package, Heart, ShoppingBag, BarChart3 } from "lucide-react"
import { ThemeToggle } from "@/shared/ui/theme-toggle"

export function Header() {
  const pathname = usePathname()
  const router = useRouter()
  const dispatch = useAppDispatch()
  const { isAuthenticated, user } = useAppSelector((state) => state.auth)
  const [logout] = useLogoutMutation()

  const handleLogout = async () => {
    try {
      await logout().unwrap()
      dispatch(clearCredentials())
      toast.success("Logged out successfully")
      router.push(ROUTES.HOME)
    } catch (error) {
      dispatch(clearCredentials())
      router.push(ROUTES.HOME)
    }
  }

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link href={ROUTES.HOME} className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-lg bg-primary" />
          <span className="text-lg font-bold text-foreground">{APP_NAME}</span>
        </Link>

        <nav className="hidden items-center gap-6 md:flex">
          <Link
            href={ROUTES.CATALOG}
            className={`text-sm font-medium transition-colors hover:text-primary ${
              pathname?.startsWith("/catalog") ? "text-primary" : "text-foreground/70"
            }`}
          >
            Catalog
          </Link>
          <Link
            href={ROUTES.MARKETPLACE}
            className={`text-sm font-medium transition-colors hover:text-primary ${
              pathname?.startsWith("/marketplace") ? "text-primary" : "text-foreground/70"
            }`}
          >
            Marketplace
          </Link>
          {isAuthenticated && (
            <>
              <Link
                href={ROUTES.COLLECTION}
                className={`text-sm font-medium transition-colors hover:text-primary ${
                  pathname === ROUTES.COLLECTION ? "text-primary" : "text-foreground/70"
                }`}
              >
                Collection
              </Link>
              <Link
                href={ROUTES.WISHLIST}
                className={`text-sm font-medium transition-colors hover:text-primary ${
                  pathname === ROUTES.WISHLIST ? "text-primary" : "text-foreground/70"
                }`}
              >
                Wishlist
              </Link>
            </>
          )}
        </nav>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          {isAuthenticated ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm" className="gap-2">
                  <User className="h-4 w-4" />
                  <span className="hidden sm:inline">{user?.username}</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuItem asChild>
                  <Link href={ROUTES.PROFILE} className="flex items-center gap-2">
                    <User className="h-4 w-4" />
                    Profile
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href={ROUTES.COLLECTION} className="flex items-center gap-2">
                    <Package className="h-4 w-4" />
                    My Collection
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href={ROUTES.WISHLIST} className="flex items-center gap-2">
                    <Heart className="h-4 w-4" />
                    Wishlist
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href={ROUTES.TRANSACTIONS} className="flex items-center gap-2">
                    <ShoppingBag className="h-4 w-4" />
                    Transactions
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuItem asChild>
                  <Link href={ROUTES.ANALYTICS} className="flex items-center gap-2">
                    <BarChart3 className="h-4 w-4" />
                    Analytics
                  </Link>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout} className="flex items-center gap-2 text-destructive">
                  <LogOut className="h-4 w-4" />
                  Log Out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="sm" asChild>
                <Link href={ROUTES.LOGIN}>Sign In</Link>
              </Button>
              <Button size="sm" asChild>
                <Link href={ROUTES.REGISTER}>Sign Up</Link>
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
