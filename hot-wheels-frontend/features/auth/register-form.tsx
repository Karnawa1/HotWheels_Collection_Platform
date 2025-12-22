"use client"
import { useRouter } from "next/navigation"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Spinner } from "@/shared/ui/spinner"
import { useRegisterMutation } from "@/shared/api/auth-api"
import { useAppDispatch } from "@/shared/lib/hooks"
import { setCredentials } from "@/entities/auth/model/auth-slice"
import { registerSchema, type RegisterInput } from "@/shared/lib/validations"
import { ROUTES } from "@/shared/lib/constants"

export function RegisterForm() {
  const router = useRouter()
  const dispatch = useAppDispatch()
  const [registerUser, { isLoading }] = useRegisterMutation()
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterInput>({
    resolver: zodResolver(registerSchema),
  })

  const onSubmit = async (data: RegisterInput) => {
    try {
      const result = await registerUser({
        username: data.username,
        email: data.email,
        password: data.password,
      }).unwrap()
      dispatch(setCredentials({ user: result.user, accessToken: result.accessToken, refreshToken: result.refreshToken }))
      toast.success("Account created successfully!")
      router.push(ROUTES.CATALOG)
    } catch (err: unknown) {
      const error = err as { data?: { message?: string } }
      toast.error(error.data?.message || "Registration failed. Please try again.")
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="username">Username</Label>
        <Input
          id="username"
          type="text"
          placeholder="johndoe"
          {...register("username")}
          className={errors.username ? "border-destructive" : ""}
        />
        {errors.username && <p className="text-sm text-destructive">{errors.username.message}</p>}
      </div>

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

      <div className="space-y-2">
        <Label htmlFor="confirmPassword">Confirm Password</Label>
        <Input
          id="confirmPassword"
          type="password"
          placeholder="••••••••"
          {...register("confirmPassword")}
          className={errors.confirmPassword ? "border-destructive" : ""}
        />
        {errors.confirmPassword && <p className="text-sm text-destructive">{errors.confirmPassword.message}</p>}
      </div>

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? <Spinner size="sm" className="mr-2" /> : null}
        Create Account
      </Button>
    </form>
  )
}
