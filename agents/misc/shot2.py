import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for name,(w,h),ids in [("desk",(1300,850),["notight"]),("phone",(390,800),["notight","peel"])]:
            pg = await b.new_page(viewport={"width":w,"height":h})
            errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("http://localhost:8765/index.html"); await pg.wait_for_timeout(700)
            await pg.screenshot(path=f"/home/claude/claims/{name}.png")
            for i in ids:
                await pg.evaluate("()=>{}")
                el = await pg.query_selector(f'.node[data-id="{i}"]'); box = await el.bounding_box()
                await pg.mouse.click(box["x"]+box["width"]/2, box["y"]+box["height"]/2); await pg.wait_for_timeout(600)
                await pg.screenshot(path=f"/home/claude/claims/{name}_{i}.png")
                await pg.keyboard.press("Escape")
            print(name, errs)
        await b.close()
asyncio.run(main())
