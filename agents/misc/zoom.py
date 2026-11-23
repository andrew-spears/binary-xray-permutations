import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1300,"height":850})
        await pg.goto("http://localhost:8765/index.html"); await pg.wait_for_timeout(700)
        await pg.mouse.move(300, 520)
        for _ in range(6): await pg.mouse.wheel(0,-60) if False else None
        await pg.keyboard.down("Control")
        for _ in range(8): await pg.mouse.wheel(0,-30); await pg.wait_for_timeout(50)
        await pg.keyboard.up("Control"); await pg.wait_for_timeout(300)
        await pg.screenshot(path="/home/claude/claims/t_zoom.png")
        await b.close()
asyncio.run(main())
