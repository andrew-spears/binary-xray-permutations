import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width":390,"height":800}, has_touch=False)
        await pg.goto("http://localhost:8765/index.html#n-conj"); await pg.wait_for_timeout(800)
        h0 = await pg.evaluate("document.getElementById('panel').offsetHeight")
        g = await (await pg.query_selector(".grip")).bounding_box()
        await pg.mouse.move(g["x"]+g["width"]/2, g["y"]+8); await pg.mouse.down()
        await pg.mouse.move(g["x"]+g["width"]/2, 500, steps=8); await pg.mouse.up(); await pg.wait_for_timeout(200)
        h1 = await pg.evaluate("document.getElementById('panel').offsetHeight")
        await pg.click("[data-full]"); await pg.wait_for_timeout(200)
        h2 = await pg.evaluate("document.getElementById('panel').offsetHeight")
        await pg.screenshot(path="/home/claude/claims/phone_drag.png")
        pg2 = await b.new_page(viewport={"width":1300,"height":850})
        await pg2.goto("http://localhost:8765/index.html#n-conj"); await pg2.wait_for_timeout(800)
        w0 = await pg2.evaluate("document.getElementById('panel').offsetWidth")
        v = await (await pg2.query_selector(".vgrip")).bounding_box()
        await pg2.mouse.move(v["x"]+5, 400); await pg2.mouse.down(); await pg2.mouse.move(400, 400, steps=8); await pg2.mouse.up()
        w1 = await pg2.evaluate("document.getElementById('panel').offsetWidth")
        print(h0,h1,h2,w0,w1)
        await b.close()
asyncio.run(main())
