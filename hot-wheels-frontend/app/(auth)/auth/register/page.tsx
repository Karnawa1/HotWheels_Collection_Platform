import Link from "next/link"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { RegisterForm } from "@/features/auth/register-form"
import { ROUTES } from "@/shared/lib/constants"

export default function RegisterPage() {
  return (
    <Card>
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold text-balance">Create Account</CardTitle>
        <CardDescription>Join the Hot Wheels collector community</CardDescription>
      </CardHeader>
      <CardContent>
        <RegisterForm />
      </CardContent>
      <CardFooter className="flex flex-col gap-4">
        <div className="text-center text-sm text-muted-foreground">
          Already have an account?{" "}
          <Link href={ROUTES.LOGIN} className="font-medium text-primary hover:underline">
            Sign in
          </Link>
        </div>
      </CardFooter>
    </Card>
  )
}
