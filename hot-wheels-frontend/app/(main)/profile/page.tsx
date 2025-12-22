"use client"

import { useRouter } from "next/navigation"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { AuthGuard } from "@/shared/components/auth-guard"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Spinner } from "@/shared/ui/spinner"
import { useGetMeQuery, useUpdateProfileMutation } from "@/shared/api/auth-api"
import { toast } from "sonner"
import { User } from "lucide-react"

const profileSchema = z.object({
  username: z.string().min(3, "Username must be at least 3 characters").max(30),
  email: z.string().email("Invalid email address"),
})

type ProfileInput = z.infer<typeof profileSchema>

export default function ProfilePage() {
  const router = useRouter()
  const { data: user, isLoading: userLoading } = useGetMeQuery()
  const [updateProfile, { isLoading }] = useUpdateProfileMutation()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ProfileInput>({
    resolver: zodResolver(profileSchema),
    values: user
      ? {
          username: user.username,
          email: user.email,
        }
      : undefined,
  })

  const onSubmit = async (data: ProfileInput) => {
    try {
      await updateProfile(data).unwrap()
      toast.success("Profile updated successfully!")
    } catch (err: unknown) {
      const error = err as { data?: { message?: string } }
      toast.error(error.data?.message || "Failed to update profile. Please try again.")
    }
  }

  return (
    <AuthGuard>
      <div className="container mx-auto max-w-2xl px-4 py-8">
        <div className="mb-8">
          <h1 className="mb-2 text-3xl font-bold">Profile</h1>
          <p className="text-muted-foreground">Manage your account settings</p>
        </div>

        {userLoading ? (
          <Card>
                <CardContent className="flex min-h-64 items-center justify-center p-6">
                  <Spinner size="lg" />
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-6">
                {/* Profile Info Card */}
                <Card>
                  <CardHeader>
                    <div className="flex items-center gap-4">
                      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary text-primary-foreground">
                        {user?.avatar ? (
                          <img
                            src={user.avatar || "/placeholder.svg"}
                            alt={user.username}
                            className="h-full w-full rounded-full"
                          />
                        ) : (
                          <User className="h-8 w-8" />
                        )}
                      </div>
                      <div>
                        <CardTitle>{user?.username}</CardTitle>
                        <CardDescription className="capitalize">{user?.role} Member</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                </Card>

                {/* Edit Profile Card */}
                <Card>
                  <CardHeader>
                    <CardTitle>Edit Profile</CardTitle>
                    <CardDescription>Update your account information</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="username">Username</Label>
                        <Input
                          id="username"
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
                          {...register("email")}
                          className={errors.email ? "border-destructive" : ""}
                        />
                        {errors.email && <p className="text-sm text-destructive">{errors.email.message}</p>}
                      </div>

                      <Button type="submit" disabled={isLoading}>
                        {isLoading ? <Spinner size="sm" className="mr-2" /> : null}
                        Save Changes
                      </Button>
                    </form>
                  </CardContent>
                </Card>

                {/* Account Stats */}
                <Card>
                  <CardHeader>
                    <CardTitle>Account Information</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Account Type</span>
                      <span className="font-medium capitalize">{user?.role}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Member Since</span>
                      <span className="font-medium">
                        {user ? new Date(user.createdAt).toLocaleDateString() : "N/A"}
                      </span>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </div>
    </AuthGuard>
  )
}
