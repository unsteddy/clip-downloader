# downloader/tiktok/tiktok_scraper.py
import asyncio
import logging
from pathlib import Path
from datetime import datetime
import json
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
logger.addHandler(console_handler)


async def scrape_tiktok_hashtag(hashtag: str, max_results: int = 20):
    url = f"https://www.tiktok.com/tag/{hashtag}"
    stealth_path = Path(__file__).parent / "stealth.min.js"
    cookies_path = Path(__file__).parent / "cookies.json"

    stealth_script = stealth_path.read_text(encoding="utf-8")
    cookies = json.loads(cookies_path.read_text(encoding="utf-8"))

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        ))
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.add_init_script(stealth_script)
        await page.goto(url)
        await page.wait_for_timeout(5000)

        for _ in range(5):
            await page.mouse.wheel(0, 1000)
            await page.wait_for_timeout(1500)

        links = await page.query_selector_all("a[href*='/video/']")
        logger.info(f"Found {len(links)} video links.")

        results = []
        for i, link in enumerate(links[:max_results]):
            href = await link.get_attribute("href")
            title = await link.inner_text()
            results.append({
                "title": title.strip()[:80] if title else "Untitled",
                "url": href,
                "views": None,
                "likes": None,
                "fetched_at": datetime.now()
            })
            logger.debug(f"[{i + 1}] Title: {title} | URL: {href}")

        await browser.close()
        return results


if __name__ == "__main__":
    async def run():
        videos = await scrape_tiktok_hashtag("funny", 10)
        for i, video in enumerate(videos, 1):
            logger.info(f"{i}. {video['title']} | {video['url']}")


    asyncio.run(run())
