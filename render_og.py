from playwright.sync_api import sync_playwright
import pathlib, sys

url = pathlib.Path("og-card.html").resolve().as_uri()
out = "og.png"
launched = None
try:
    with sync_playwright() as p:
        for opt in [dict(channel="chrome", args=["--enable-unsafe-swiftshader"]),
                    dict(args=["--enable-unsafe-swiftshader"])]:
            try:
                browser = p.chromium.launch(**opt); launched = opt; break
            except Exception as e:
                print("launch fail", opt, repr(e)[:120])
        if launched is None:
            print("NO_BROWSER"); sys.exit(2)
        pg = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=2)
        pg.goto(url); pg.wait_for_timeout(1800)
        pg.screenshot(path=out, clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        browser.close()
    print("OK", out)
except Exception as e:
    print("ERR", repr(e)[:200]); sys.exit(3)
