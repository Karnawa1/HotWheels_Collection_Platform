import { configureStore } from "@reduxjs/toolkit"
import authReducer, { setCredentials, clearCredentials, setUser } from "@/entities/auth/model/auth-slice"
import type { User } from "@/shared/types"

const mockUser: User = {
  id: "1",
  username: "testuser",
  email: "test@example.com",
  role: "collector",
  createdAt: "2023-01-01T00:00:00Z",
  updatedAt: "2023-01-01T00:00:00Z",
}

describe("Auth Slice", () => {
  let store: ReturnType<typeof configureStore>

  beforeEach(() => {
    store = configureStore({
      reducer: {
        auth: authReducer,
      },
    })
  })

  it("should handle initial state", () => {
    expect(store.getState().auth).toEqual({
      user: null,
      isAuthenticated: false,
    })
  })

  it("should handle setCredentials", () => {
    store.dispatch(setCredentials({ user: mockUser, accessToken: "test-token" }))

    const state = store.getState().auth
    expect(state.isAuthenticated).toBe(true)
    expect(state.user).toEqual(mockUser)
  })

  it("should handle clearCredentials", () => {
    store.dispatch(setCredentials({ user: mockUser, accessToken: "test-token" }))
    store.dispatch(clearCredentials())

    const state = store.getState().auth
    expect(state.isAuthenticated).toBe(false)
    expect(state.user).toBeNull()
  })

  it("should handle setUser", () => {
    store.dispatch(setUser(mockUser))

    const state = store.getState().auth
    expect(state.user).toEqual(mockUser)
  })
})
