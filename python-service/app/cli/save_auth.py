# save_auth.py
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.upwork.com")
        print("Please log in in the opened browser window, then press ENTER in the terminal.")
        input()
        await context.storage_state(path="auth.json")
        print("Saved auth.json")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
