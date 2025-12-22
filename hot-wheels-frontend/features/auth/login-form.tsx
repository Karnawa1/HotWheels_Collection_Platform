"use client"
import { useRouter } from "next/navigation"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Spinner } from "@/shared/ui/spinner"
import { useLoginMutation } from "@/shared/api/auth-api"
import { useAppDispatch } from "@/shared/lib/hooks"
import { setCredentials } from "@/entities/auth/model/auth-slice"
import { loginSchema, type LoginInput } from "@/shared/lib/validations"
import { ROUTES } from "@/shared/lib/constants"

export function LoginForm() {
  const router = useRouter()
  const dispatch = useAppDispatch()
  const [login, { isLoading }] = useLoginMutation()
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginInput>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginInput) => {
    try {
      const result = await login(data).unwrap()
      dispatch(setCredentials({ user: result.user, accessToken: result.accessToken, refreshToken: result.refreshToken }))
      toast.success("Welcome back!")
      router.push(ROUTES.CATALOG)
    } catch (err: unknown) {
      const error = err as { data?: { message?: string } }
      toast.error(error.data?.message || "Login failed. Please try again.")
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="you@example.com"
          {...register("email")}
          className={errors.email ? "border-destructive" : ""}
        />
        {errors.email && <p className="text-sm text-destructive">{errors.email.message}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          type="password"
          placeholder="••••••••"
          {...register("password")}
          className={errors.password ? "border-destructive" : ""}
        />
        {errors.password && <p className="text-sm text-destructive">{errors.password.message}</p>}
      </div>

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? <Spinner size="sm" className="mr-2" /> : null}
        Sign In
      </Button>
    </form>
  )
}
