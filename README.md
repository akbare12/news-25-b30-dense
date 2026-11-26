# THE WORLD TODAY — Dense Front Page

[![THE WORLD TODAY](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/akbare12/news-25-b30-dense/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/akbare12/news-25-b30-dense/reward.svg)](https://make.fun/bounty/news-image-20261125)

A dense one-page front page for **Wednesday 25 November 2026**: 50 stories
across 10 regions — 3 hero stories, 10 illustrated mini-scenes, a 47-story
grid, an ALSO strip, and a world-map + sources footer.

## Headlines

1. **Trump hits 14 partners with new tariffs; China at 20%** — Washington
   unveils sweeping new duties, with Chinese goods facing a 20% rate.
2. **AI chip selloff sinks Kospi 6.16% to 4,697.51** — Samsung falls 9.87%
   and SK Hynix 11.05% as the chip rally breaks.
3. **Shenzhou-24 carries the first foreign astronaut to Tiangong** —
   Muhammad Zeeshan Ali of Pakistan joins China's space station.

Also inside: the Bogor gold-mine collapse (9 killed, 17 trapped), COP31
climate talks, Gaza ceasefire talks, and 46 more stories from every region.

## How it is built

- `gen.py` renders `entry.png` (1024x640, under 1 MiB) with Pillow at
  build time.
- `main.py` is standard-library only: at grade time it copies the
  pre-rendered `entry.png` into `MAKEFUN_OUTPUT_DIR`.

## Verify

```sh
python3 gen.py          # renders entry.png, prints size + sha256
python3 main.py         # copies entry.png into out/
```
