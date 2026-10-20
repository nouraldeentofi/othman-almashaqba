#!/usr/bin/env python3
"""Draws the link-preview card (assets/img/og.jpg, 1200×630) and the home-screen icon
(assets/img/icon-180.png) with the site's own fonts, photo and thread field.
Needs Playwright for Python with Chromium:  python3 og.py"""
import os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
A = "file://" + os.path.join(HERE, "assets")

OG = f"""<!doctype html><html lang="ar" dir="rtl" data-theme="light"><head><meta charset="utf-8">
<link rel="stylesheet" href="{A}/style.css">
<style>
  html,body{{margin:0;width:1200px;height:630px;overflow:hidden;background:#F3F5F8}}
  .card{{position:relative;width:1200px;height:630px;isolation:isolate}}
  .card>.threads{{position:absolute;inset:auto 0 0;width:1200px;height:250px;z-index:-1}}
  .copy{{position:absolute;inset-inline-start:72px;top:92px;width:600px}}
  .copy .mark{{width:58px;height:58px;margin-bottom:26px}}
  .ar{{font-family:var(--display);font-weight:650;font-size:74px;line-height:1.25;color:#13213E;margin:0}}
  .en{{font-family:var(--font);font-weight:600;font-size:34px;letter-spacing:-.02em;color:#13213E;margin:6px 0 18px;direction:ltr;text-align:right}}
  .stm{{font-family:var(--display);font-weight:420;font-size:30px;line-height:1.5;color:#2B4C9B;margin:0}}
  .ph{{position:absolute;inset-inline-end:84px;top:70px;width:340px;height:425px;border-radius:30px;overflow:hidden;box-shadow:0 30px 60px -20px rgba(19,33,62,.45)}}
  .ph img{{width:100%;height:100%;object-fit:cover;object-position:50% 18%}}
</style></head><body>
<div class="card">
  <canvas class="threads" data-threads="band" aria-hidden="true"></canvas>
  <div class="copy">
    <svg class="mark" viewBox="0 0 40 40"><path class="mk-a" d="M37 10C30 6 25 15 28 19S35 16 30 13 22 14 18 14H3"/><path class="mk-c" d="M37 20C32 25 27 13 22 18S19 20 17 20H3"/><path class="mk-b" d="M37 30C30 34 27 22 23 24S21 26 18 26H3"/></svg>
    <p class="ar">عثمان المشاقبة</p>
    <p class="en">Othman Almashaqba</p>
    <p class="stm">أبدأ من الناس، وأنتهي بأثر يُقاس.</p>
  </div>
  <div class="ph"><img src="{A}/img/othman-634.jpg" alt=""></div>
</div>
<script src="{A}/threads.js"></script>
</body></html>"""

ICON = """<!doctype html><html><body style="margin:0;background:transparent">
<svg width="180" height="180" viewBox="0 0 64 64"><rect width="64" height="64" rx="0" fill="#13213E"/>
<g transform="translate(5 5) scale(1.35)" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="3.1">
<path d="M37 10C30 6 25 15 28 19S35 16 30 13 22 14 18 14H3" stroke="#C99B79"/>
<path d="M37 20C32 25 27 13 22 18S19 20 17 20H3" stroke="#FFFFFF"/>
<path d="M37 30C30 34 27 22 23 24S21 26 18 26H3" stroke="#8FAEF2"/></g></svg></body></html>"""


def main():
    tmp = os.path.join(HERE, ".og.html")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(OG)
        pg.goto("file://" + tmp)
        pg.wait_for_timeout(1600)
        pg.screenshot(path=os.path.join(HERE, "assets/img/og.jpg"), type="jpeg", quality=88)
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(ICON)
        pg.set_viewport_size({"width": 180, "height": 180})
        pg.goto("file://" + tmp)
        pg.screenshot(path=os.path.join(HERE, "assets/img/icon-180.png"))
        b.close()
    os.remove(tmp)
    print("wrote assets/img/og.jpg and assets/img/icon-180.png")


if __name__ == "__main__":
    main()
