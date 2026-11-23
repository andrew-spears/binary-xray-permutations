import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":1300,"height":850}); errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("http://localhost:8765/index.html"); await pg.wait_for_timeout(700)
        await pg.screenshot(path="/home/claude/claims/t_desk.png")
        await pg.wait_for_timeout(200)
        await pg.screenshot(path="/home/claude/claims/t_desk_zoom.png")
        ph = await b.new_page(viewport={"width":390,"height":800}); ph.on("pageerror", lambda e: errs.append(str(e)))
        await ph.goto("http://localhost:8765/index.html#n-dual"); await ph.wait_for_timeout(800)
        h0 = await ph.evaluate("document.getElementById('panel').offsetHeight")
        hd = await (await ph.query_selector(".phead h2")).bounding_box()
        await ph.mouse.click(hd["x"]+20, hd["y"]+5); await ph.wait_for_timeout(300)
        h1 = await ph.evaluate("[document.getElementById('panel').offsetHeight, document.getElementById('panel').getBoundingClientRect().top]")
        await ph.screenshot(path="/home/claude/claims/t_phone_full.png")
        print(errs, h0, h1)
        await b.close()
asyncio.run(main())
