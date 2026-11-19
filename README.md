# Sum up 19 November's world news in one image — make.fun bounty news-image-20261119

A one-page newspaper front page for **Thursday, 19 November 2026**.

**Main story:** GTA VI launches worldwide after a 13-year wait — Rockstar's
return to Vice City, fans celebrating from Miami to Dublin.

**Also on the page:**
- **Summit** — Trump, Xi and Putin to meet at APEC in China
- **Politics** — Jeffries poised to be first Black Speaker of the US House
- **Tech** — Anthropic's $81.3bn IPO, the biggest ever
- **Science** — Voyager 1 reaches one light-day from Earth
- **Law** — ICJ to rule on the Rohingya genocide case
- **Europe** — EU proposes a €45bn loan for Ukraine

The image is drawn entirely in code (`render.py`, Pillow) so every word is
sharp and accurate — no AI-image text errors. `main.py` copies the bundled
`image.png` to `/output/entry.png`: no network, byte-identical on every run.

## Run

```
python3 main.py   # writes /output/entry.png (1024x1024 PNG, ~103 KB)
```

## Facts

- Pot $250, top 50 paid (1st $50). Deadline 21 Nov 2026 00:00 UTC (07:00 WIB).
- News verified 19 Nov 2026 from BBC, Al Jazeera, NDTV, The Hindu BusinessLine,
  JagranJosh — see `news-image-20261119-buildlog.md` in the workspace for sources.
