const nextJest = require("next/jest")

const createJestConfig = nextJest({
  dir: "./",
})

const customJestConfig = {
  setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
  testEnvironment: "jest-environment-jsdom",
  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/$1",
  },
  testMatch: ["**/__tests__/**/*.test.ts?(x)"],
  collectCoverageFrom: [
    "app/**/*.{js,jsx,ts,tsx}",
    "shared/**/*.{js,jsx,ts,tsx}",
    "features/**/*.{js,jsx,ts,tsx}",
    "widgets/**/*.{js,jsx,ts,tsx}",
    "entities/**/*.{js,jsx,ts,tsx}",
    "!**/*.d.ts",
    "!**/node_modules/**",
    "!**/.next/**",
  ],
}

module.exports = createJestConfig(customJestConfig)
