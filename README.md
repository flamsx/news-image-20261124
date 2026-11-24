# Tuesday 24 November 2026 — the world in one page

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/flamsx/news-image-20261124/rank.svg)](https://make.fun/c/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/flamsx/news-image-20261124/reward.svg)](https://make.fun/c/news-image-20261124)

One image summing up the world's news of **Tuesday 24 November 2026**:
35 stories across 7 regions — Seoul's air-raid alert as jets near Ulleung
Island, Huang's comeback shaking Wall Street, the search going on at the
Indonesia candy factory, the chess world title match opening in Geneva,
and an Oxfam report calling Gaza a "toxic wasteland".

## How it is made

`draw.py` draws the newspaper front page with Pillow (Lexend type, committed
under `fonts/`) and writes `entry.png` (1024x1024). `main.py` is the entry
point: using only the Python standard library it copies the committed
`entry.png` to the output directory, so the program runs with no network and
writes byte-identical output on every run.

```sh
python3 draw.py            # regenerate entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Every story was researched fresh on 24 November 2026 from Reuters, AP,
AFP, the UN, Oxfam, FIDE and other named sources; each card names its
source. Stories first reported before 24 November are listed in the
DATE CHECK box on the page itself, not presented as the day's news.

Entry for the [news-image-20261124](https://make.fun/c/news-image-20261124)
bounty on make.fun.
