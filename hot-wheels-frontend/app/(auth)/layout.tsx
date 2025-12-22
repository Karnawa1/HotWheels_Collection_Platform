import type React from "react"
import Link from "next/link"
import { Car } from "lucide-react"

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex min-h-screen">
      {/* Left Side - Logo/Brand (50%) */}
      <Link
        href="/"
        className="hidden lg:flex lg:w-1/2 items-center justify-center bg-gradient-to-br from-primary via-primary/90 to-primary/80 p-12"
      >
        <div className="text-center">
          <div className="mb-6 flex justify-center">
            <div className="flex size-24 items-center justify-center rounded-full bg-white/10 backdrop-blur-sm">
              <Car className="size-12 text-white" />
            </div>
          </div>
          <h1 className="mb-4 text-balance text-4xl font-bold text-white">Hot Wheels Collector</h1>
          <p className="text-pretty text-lg text-white/90">The ultimate platform for collectors</p>
        </div>
      </Link>

      {/* Right Side - Form (50%) */}
      <div className="flex w-full items-center justify-center p-4 lg:w-1/2">
        <div className="w-full max-w-md">
          {/* Mobile Logo */}
          <Link href="/" className="mb-8 flex justify-center lg:hidden">
            <div className="flex items-center gap-3">
              <div className="flex size-12 items-center justify-center rounded-full bg-primary/10">
                <Car className="size-6 text-primary" />
              </div>
              <span className="text-xl font-bold">Hot Wheels Collector</span>
            </div>
          </Link>

          {children}
        </div>
      </div>
    </div>
  )
}
