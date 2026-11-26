[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/salikamarlisa3-cell/global-edition-news-image-20261126-v4/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/salikamarlisa3-cell/global-edition-news-image-20261126-v4/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# The World in One Day — Thursday 26 November 2026 (v4)

Entry for **[news-image-20261126](https://make.fun/bounty/news-image-20261126)** on make.fun. One page sums up the day: **36 verified
stories** (every one cited in [SOURCES.md](SOURCES.md)), 13 of them drawn
as flat scene panels and pinned on a schematic dot-matrix world map, a
UTC timeline, a by-the-numbers band of the day's own figures, a status
chip on every story (CONFIRMED / OFFICIAL / REPORTED / CLAIM / ONGOING),
and an itemised date check that names what was held out, with dates.

The day's signature stories lead the page: the Macy's Thanksgiving
parade postponed for the first time in its 100 years, India marking 18
years since the 26/11 Mumbai attacks, and Game 3 of the Gukesh–Sindarov
world chess title in Geneva. All scenes are drawn, not photographed —
the poster says so on its face.

## How it is built

- `build_poster.py` authors the page as SVG from the story data and
  emits `poster.svg` (a build artifact — deliberately not committed, so
  generated lines never dilute the authored source).
- `generate.mjs` renders `poster.svg` to `entry.png` (1024×1024) with a
  local Chromium headless shell. No network, no external references.
- `main.ts` is the competition program: it only delivers `entry.png`
  byte-for-byte to the output directory and verifies the copy.

## Run

```
node generate.mjs   # rebuild entry.png from the story data
```
