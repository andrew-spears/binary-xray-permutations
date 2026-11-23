import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for name,(w,h) in {"desk":(1300,850),"phone":(390,800)}.items():
            pg = await b.new_page(viewport={"width":w,"height":h})
            errs=[]; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
            await pg.goto("http://localhost:8765/index.html"); await pg.wait_for_timeout(800)
            await pg.screenshot(path=f"/home/claude/claims/{name}.png")
            el = await pg.query_selector('.node[data-id="conj"]')
            box = await el.bounding_box()
            await pg.mouse.click(box["x"]+box["width"]/2, box["y"]+box["height"]/2); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f"/home/claude/claims/{name}_sel.png")
            print(name, errs)
        await b.close()
asyncio.run(main())
