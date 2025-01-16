const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false }); // Launch browser in non-headless mode
  const page = await browser.newPage(); // Open a new page
  await page.goto('https://google.com'); // Navigate to Google

  // Wait for input/textarea elements to load
  await page.waitForSelector('input, textarea');

  // Find the likely search box based on name, placeholder, or aria-label
  const searchBox = await page.$('input[name="q"], textarea[name="q"], input[aria-label="Search"], textarea[aria-label="Search"]');

  if (searchBox) {
    // Fill the search box with the query
    await searchBox.fill('Adani share price');

    // Find and click the "Google Search" button (submit button)
    const searchButton = await page.$('input[name="btnK"], input[type="submit"]');
    if (searchButton) {
      await searchButton.click(); // Click the search button to execute the search
    }

    // Wait for the results to load by checking for the results section
    await page.waitForSelector('#search');

    // Take a screenshot of the search results
    await page.screenshot({ path: 'adani_share_price.png' });
    console.log('Search executed successfully and screenshot saved.');
  } else {
    console.log('Search box not found.');
  }

  await browser.close(); // Close the browser
})();
