import { test, expect } from "@playwright/test"

test.describe("Collection Management", () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto("/auth/login")
    await page.fill('input[id="email"]', "test@example.com")
    await page.fill('input[id="password"]', "password123")
    await page.click('button[type="submit"]')
    await page.waitForURL("/catalog/models")
  })

  test("should display collection page", async ({ page }) => {
    await page.goto("/collection")

    await expect(page.locator("h1:has-text('My Collection')")).toBeVisible()
  })

  test("should show collection stats", async ({ page }) => {
    await page.goto("/collection")

    // Check for stats cards
    await expect(page.locator("text=Total Items")).toBeVisible()
    await expect(page.locator("text=Total Value")).toBeVisible()
  })

  test("should navigate to analytics page", async ({ page }) => {
    await page.goto("/collection")

    // Click on analytics link in header dropdown
    await page.click('button:has-text("testuser")')
    await page.click("text=Analytics")

    await expect(page).toHaveURL("/analytics")
    await expect(page.locator("h1:has-text('Collection Analytics')")).toBeVisible()
  })
})
