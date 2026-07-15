import asyncio
import httpx
from playwright.async_api import async_playwright

BACKEND_URL = "http://localhost:8000/api/v1/leads/"

async def audit_website(company_name: str, target_url: str):
    print(f"🚀 Initializing diagnostic sweep for: {company_name} ({target_url})")
    
    async with async_playwright() as p:
        # Launch a headless browser instance
        browser = await p.chromium.launch(headless=True)
        
        # Emulate a mobile device or desktop layout context
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()

        # 1. Measure Page Load Speed Performance
        start_time = asyncio.get_event_loop().time()
        try:
            # Go to the website and wait until network connections drop to 0
            response = await page.goto(target_url, wait_until="networkidle", timeout=15000)
            end_time = asyncio.get_event_loop().time()
            load_speed = round(end_time - start_time, 2)
        except Exception as e:
            print(f"❌ Network timeout reaching target {target_url}: {e}")
            await browser.close()
            return

        # 2. Check for Modern Tracking Pixels in the page source code
        html_content = await page.content()
        tracking_pixels = []
        if "connect.facebook.net" in html_content or "fbevent" in html_content:
            tracking_pixels.append("Facebook Pixel")
        if "googletagmanager.com" in html_content or "google-analytics" in html_content:
            tracking_pixels.append("Google Analytics/Tag Manager")
        if "tiktok.com/i18n/pixel" in html_content:
            tracking_pixels.append("TikTok Pixel")

        # 3. Check Mobile Responsiveness Elements
        # We check if a viewport meta tag exists (standard requirement for mobile responsive builds)
        has_viewport_meta = await page.query_selector("meta[name='viewport']") is not None

        await browser.close()

        # Package the scraped parameters into your Pydantic Schema layout
        payload = {
            "company_name": company_name,
            "website_url": target_url,
            "data_payload": {
                "page_load_speed_seconds": load_speed,
                "is_mobile_responsive": has_viewport_meta,
                "tracking_pixels": tracking_pixels
            }
        }

        # 4. Programmatic Ingestion: Push the data into your FastAPI Backend Pipeline
        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(BACKEND_URL, json=payload, timeout=10.0)
                if res.status_code == 201:
                    print(f"✅ Target fully processed and committed to DB. Score: {res.json().get('opportunity_score')}/100")
                else:
                    print(f"❌ Backend ingestion failed: {res.text}")
            except Exception as e:
                print(f"❌ Unable to establish communication with local backend servers: {e}")

# Example Run to simulate real targets
async def main():
    # You can loop through a list of local business websites here
    await audit_website("Example Slow Store", "https://example.com")

if __name__ == "__main__":
    asyncio.run(main())