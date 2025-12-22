import { test, expect } from "@playwright/test"

test.describe("Authentication Flow", () => {
  test("should allow user to register and login", async ({ page }) => {
    // Navigate to register page
    await page.goto("/auth/register")

    // Fill registration form
    await page.fill('input[id="username"]', "testuser")
    await page.fill('input[id="email"]', "test@example.com")
    await page.fill('input[id="password"]', "password123")
    await page.fill('input[id="confirmPassword"]', "password123")

    // Submit form
    await page.click('button[type="submit"]')

    // Should redirect to catalog or show success
    await page.waitForURL("/catalog/models", { timeout: 5000 })

    // Verify user is logged in by checking header
    await expect(page.locator("text=testuser")).toBeVisible()
  })

  test("should show validation errors on invalid input", async ({ page }) => {
    await page.goto("/auth/login")

    // Submit empty form
    await page.click('button[type="submit"]')

    // Should show validation errors
    await expect(page.locator("text=/Invalid email address/i")).toBeVisible()
  })

  test("should allow user to logout", async ({ page }) => {
    // Assuming user is already logged in
    await page.goto("/")

    // Click user menu
    await page.click('button:has-text("testuser")')

    // Click logout
    await page.click("text=Log Out")

    // Should redirect to home and show login button
    await expect(page.locator("text=Sign In")).toBeVisible()
  })
})
