// playwright_scaffold.js
// Tool script for generating base Playwright testing configuration and first test.

const fs = require('fs');
const path = require('path');

const configTemplate = `
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
`;

const testTemplate = `
const { test, expect } = require('@playwright/test');

test('homepage has correct title and renders main content', async ({ page }) => {
  await page.goto('/');
  
  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/App/);
  
  // Create your actual visually-verifiable assertions here.
  // await expect(page.locator('.main-header')).toBeVisible();
  
  // Visual regression snapshot
  // await expect(page).toHaveScreenshot('homepage.png');
});
`;

function scaffold(targetDir) {
    const testsDir = path.join(targetDir, 'tests');
    if (!fs.existsSync(testsDir)) {
        fs.mkdirSync(testsDir, { recursive: true });
    }

    const configPath = path.join(targetDir, 'playwright.config.js');
    const testPath = path.join(testsDir, 'example.spec.js');

    if (!fs.existsSync(configPath)) {
        fs.writeFileSync(configPath, configTemplate.trim());
        console.log('Created playwright.config.js');
    }

    if (!fs.existsSync(testPath)) {
        fs.writeFileSync(testPath, testTemplate.trim());
        console.log('Created tests/example.spec.js');
    }

    console.log('Playwright scaffolding complete. Run with: npx playwright test');
}

if (require.main === module) {
    const target = process.argv[2] || process.cwd();
    scaffold(target);
}
