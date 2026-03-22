# main.py - اجرا روی Replit

import asyncio
import base64
import requests
from playwright.async_api import async_playwright

SERVER = "https://ytnet.pythonanywhere.com"
SEND_URL = f"{SERVER}/tw-send"
GET_CMD_URL = f"{SERVER}/tw-getdata"
DEFAULT_URL = "https://www.google.com"
INTERVAL = 5  # ثانیه


async def send_state(page):
    try:
        screenshot_bytes = await page.screenshot()
        screenshot_b64 = base64.b64encode(screenshot_bytes).decode()
        viewport = page.viewport_size or {"width": 1280, "height": 900}

        payload = {
            "screenshot": screenshot_b64,
            "url": page.url,
            "title": await page.title(),
            "width": viewport["width"],
            "height": viewport["height"]
        }

        requests.post(SEND_URL, json=payload, timeout=10)
        print(f"📤 ارسال شد | {page.url}")

    except Exception as e:
        print(f"⚠️ خطا در ارسال: {e}")


async def check_command(page):
    try:
        resp = requests.get(GET_CMD_URL, timeout=10).json()

        if not resp.get("has_command"):
            return

        cmd = resp["command"]
        cmd_type = cmd.get("type")

        if cmd_type == "click":
            await page.mouse.click(cmd["x"], cmd["y"])
            print(f"🖱️ کلیک: ({cmd['x']}, {cmd['y']})")

        elif cmd_type == "type":
            await page.mouse.click(cmd["x"], cmd["y"])
            await asyncio.sleep(0.3)
            await page.keyboard.type(cmd["text"])
            print(f"⌨️ تایپ: {cmd['text']}")

        elif cmd_type == "navigate":
            await page.goto(cmd["url"], wait_until="domcontentloaded")
            print(f"🌐 رفتن به: {cmd['url']}")

    except Exception as e:
        print(f"⚠️ خطا در دریافت دستور: {e}")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--window-size=1280,900"
            ]
        )

        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )

        page = await context.new_page()
        await page.goto(DEFAULT_URL, wait_until="domcontentloaded")
        print(f"✅ مرورگر آماده است | {DEFAULT_URL}")

        while True:
            await send_state(page)
            await check_command(page)
            await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
