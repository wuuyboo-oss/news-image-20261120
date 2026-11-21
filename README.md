# news-image-20261120 — "The World Today"

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) [![rank](https://make.fun/badge/news-image-20261120/wuuyboo-oss/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) [![reward](https://make.fun/badge/news-image-20261120/wuuyboo-oss/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-page newspaper front page summing up world news for Friday,
20 November 2026, drawn from scratch with PIL + Liberation fonts.
1024x1024 RGB PNG, no AI imagery.

## The six stories

1. **LEAD — Summit in Shenzhen:** Trump, Xi and Putin hold the first-ever
   three-way summit (APEC sidelines) and release a peace declaration;
   nuclear arms control is on the agenda.
2. **WORLD COURT:** the ICJ rules Myanmar committed genocide against the
   Rohingya; the ruling cannot be appealed.
3. **GULF:** Iran widens attacks on Gulf states and tankers; the IEA calls
   it the biggest energy security threat in history.
4. **UKRAINE:** the Crimean Bridge is attacked a third time this week;
   Russian strikes damage the Austrian and Dutch embassies in Kyiv.
5. **WEATHER:** Cyclone Akvan nears India's east coast, landfall expected
   20 November; Odisha shuts schools and evacuates coastal areas.
6. **BUSINESS:** Anthropic's valuation reportedly reaches $1.5 trillion.

## Layout

Masthead ("THE WORLD TODAY", dated Friday, 20 November 2026) on top,
the lead story with a skyline illustration, a 2x2 grid of the four
middle stories (each with a hand-drawn line icon: scales, tanker,
bridge, storm), and a navy business strip along the bottom.

## Run

```sh
python3 gen_page.py          # draws entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies it
```
