import { createSlice, type PayloadAction } from "@reduxjs/toolkit"
import { setAccessToken, setRefreshToken } from "@/shared/api/base-query"
import type { User } from "@/shared/types"

const ACCESS_TOKEN_KEY = "hw_access_token"

interface AuthState {
  user: User | null
  isAuthenticated: boolean
}

// Check if we have a token stored (for hydration after page reload)
// Use direct localStorage access to avoid circular dependency
const getInitialAuthState = (): AuthState => {
  // Only check localStorage on client side
  if (typeof window !== "undefined") {
    const token = localStorage.getItem(ACCESS_TOKEN_KEY)
    if (token) {
      return {
        user: null, // User will be fetched via /auth/me
        isAuthenticated: true,
      }
    }
  }
  return {
    user: null,
    isAuthenticated: false,
  }
}

const initialState: AuthState = getInitialAuthState()

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setCredentials: (state, action: PayloadAction<{ user?: User; accessToken: string; refreshToken?: string }>) => {
      if (action.payload.user) {
        state.user = action.payload.user
      }
      state.isAuthenticated = true
      setAccessToken(action.payload.accessToken)
      if (action.payload.refreshToken) {
        setRefreshToken(action.payload.refreshToken)
      }
    },
    clearCredentials: (state) => {
      state.user = null
      state.isAuthenticated = false
      setAccessToken(null)
      setRefreshToken(null)
    },
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload
    },
    // New action to restore auth state from localStorage
    hydrateAuth: (state) => {
      if (typeof window !== "undefined") {
        const token = localStorage.getItem(ACCESS_TOKEN_KEY)
        if (token) {
          state.isAuthenticated = true
        }
      }
    },
  },
})

export const { setCredentials, clearCredentials, setUser, hydrateAuth } = authSlice.actions
export default authSlice.reducer
