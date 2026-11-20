# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/wuuyboo-oss/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/wuuyboo-oss/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A 1024×1024 newspaper front page — "THE WORLD, Friday 20 November 2026" — that sums up the day's world news in six stories: Trump, Xi and Putin hold the first-ever three-way summit in Shenzhen and release a peace declaration; the ICJ rules Myanmar committed genocide against the Rohingya; Iran widens attacks on Gulf states and tankers; the Crimean Bridge is hit a third time; Cyclone Akvan nears India's east coast; and Anthropic's valuation is reportedly $1.5 trillion. Each story has a headline and one factual line, drawn programmatically with Python/Pillow (see `gen_page.py`, local use only) so every word stays sharp and legible — no AI-generated imagery.

## Run it

```sh
python3 main.py
```

This copies `entry.png` to `/output/entry.png` (or to `$MAKEFUN_OUTPUT_DIR/entry.png` when that is set, e.g. for a local run: `mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py`).

---

<sub>Entered on [make.fun](https://make.fun/?ref=wkz0m1sg&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
