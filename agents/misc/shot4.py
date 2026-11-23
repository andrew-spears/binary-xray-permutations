import asyncio,sys
from playwright.async_api import async_playwright
ids=sys.argv[1:]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        errs=[]
        pg = await b.new_page(viewport={"width":1300,"height":850}); pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("http://localhost:8765/index.html"); await pg.wait_for_timeout(700)
        await pg.screenshot(path="/home/claude/claims/t_desk.png")
        for i in ids:
            ph = await b.new_page(viewport={"width":390,"height":844}); ph.on("pageerror", lambda e: errs.append(str(e)))
            await ph.goto(f"http://localhost:8765/index.html#n-{i}"); await ph.wait_for_timeout(700)
            hd = await (await ph.query_selector(".phead h2")).bounding_box()
            await ph.mouse.click(hd["x"]+20, hd["y"]+5); await ph.wait_for_timeout(300)
            await ph.screenshot(path=f"/home/claude/claims/t_{i}.png", full_page=False)
        print(errs)
        await b.close()
asyncio.run(main())
