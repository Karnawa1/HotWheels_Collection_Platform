import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ROUTES } from "@/shared/lib/constants"
import { Car, TrendingUp, Users, Search } from "lucide-react"

export default function HomePage() {
  return (
    <div className="flex min-h-[calc(100vh-4rem)] flex-col">
      {/* Hero Section */}
      <section className="flex flex-1 items-center justify-center bg-gradient-to-b from-primary/5 via-background to-background px-4 py-20">
        <div className="mx-auto max-w-5xl text-center">
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border bg-background/50 px-4 py-2 text-sm backdrop-blur-sm">
            <Car className="size-4 text-primary" />
            <span className="text-muted-foreground">The Ultimate Hot Wheels Platform</span>
          </div>

          <h1 className="mb-6 text-balance text-5xl font-bold leading-tight tracking-tight md:text-6xl lg:text-7xl">
            Collect, Trade & Connect with Hot Wheels Enthusiasts
          </h1>

          <p className="mb-10 text-pretty text-lg text-muted-foreground md:text-xl">
            Manage your collection, discover rare models, and trade with collectors worldwide. Join the most
            comprehensive Hot Wheels community today.
          </p>

          <div className="flex flex-col justify-center gap-4 sm:flex-row">
            <Button asChild size="lg" className="gap-2">
              <Link href={ROUTES.REGISTER}>
                Get Started
                <Car className="size-4" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline">
              <Link href={ROUTES.CATALOG}>Browse Catalog</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="border-t bg-secondary/30 px-4 py-20">
        <div className="mx-auto max-w-6xl">
          <div className="mb-12 text-center">
            <h2 className="mb-4 text-balance text-3xl font-bold md:text-4xl">Everything You Need</h2>
            <p className="text-pretty text-muted-foreground">Powerful tools for serious collectors</p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            <Card>
              <CardHeader>
                <div className="mb-2 flex size-12 items-center justify-center rounded-lg bg-primary/10">
                  <Search className="size-6 text-primary" />
                </div>
                <CardTitle>Complete Catalog</CardTitle>
                <CardDescription>
                  Browse thousands of Hot Wheels models with detailed specifications, images, and rarity information.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <div className="mb-2 flex size-12 items-center justify-center rounded-lg bg-primary/10">
                  <Car className="size-6 text-primary" />
                </div>
                <CardTitle>Collection Management</CardTitle>
                <CardDescription>
                  Track your collection with condition ratings, purchase history, and personal notes.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <div className="mb-2 flex size-12 items-center justify-center rounded-lg bg-primary/10">
                  <TrendingUp className="size-6 text-primary" />
                </div>
                <CardTitle>Marketplace</CardTitle>
                <CardDescription>
                  Buy and sell with confidence. Secure transactions and verified seller ratings.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <div className="mb-2 flex size-12 items-center justify-center rounded-lg bg-primary/10">
                  <Users className="size-6 text-primary" />
                </div>
                <CardTitle>Community</CardTitle>
                <CardDescription>
                  Connect with collectors worldwide. Share your finds and trade duplicates.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <div className="mb-2 flex size-12 items-center justify-center rounded-lg bg-primary/10">
                  <TrendingUp className="size-6 text-primary" />
                </div>
                <CardTitle>Analytics</CardTitle>
                <CardDescription>
                  Track collection value over time with detailed analytics and market insights.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <div className="mb-2 flex size-12 items-center justify-center rounded-lg bg-primary/10">
                  <Car className="size-6 text-primary" />
                </div>
                <CardTitle>Wishlist</CardTitle>
                <CardDescription>
                  Create wishlists and get notified when models become available on the marketplace.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>
    </div>
  )
}
