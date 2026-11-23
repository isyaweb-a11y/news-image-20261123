# Monday 23 November 2026 — the world's news in one picture

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/isyaweb-a11y/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/isyaweb-a11y/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

One 1024×1024 PNG that sums up **Monday 23 November 2026** in world
news: 45 stories in total — 3 leads, 12 numbered panels pinned to a
dotted world map, and 30 briefs — plus a UTC timeline strip,
CONFIRMED / CLAIM status chips with sources, and a DATE CHECK box that
names the big stories left out because they belong to other days.

## The three leads

1. **COP31 collapses — no climate deal, the first failure since
   Copenhagen.** After 44 hours of overtime in Antalya, the EU and
   others refused a pact that never mentions fossil fuels. (ANTALYA)
2. **Iran hits Bahrain and tankers in Hormuz; Bahrain takes it to the
   UN.** Missiles and drones hit US positions at al-Riffa and Awali,
   two tankers were struck near Oman, and Bahrain demands Security
   Council action. (AL-MONITOR)
3. **Russia starts towing the drone-hit Sparta II out of Finnish
   waters.** After two days of firefighting, the cargo ship is towed
   home while thermal cameras still show warm containers. (REUTERS)

Every story here happened or was first reported on 23 November 2026,
checked against AFP, AP, Reuters, Yle, Al-Monitor, UKMTO, Scientific
American, BBC, PTI and official statements.

## How it runs

```sh
python3 main.py /tmp/out.png
```

With no argument it writes to `$MAKEFUN_OUTPUT_DIR/entry.png`, or
`/output/entry.png` — the path the grader reads.

`main.py` is standard library only. It validates `entry.png` — PNG
signature, a full chunk walk with every chunk's CRC checked, at least
one IDAT chunk, ending in IEND, 1024×1024, no more than 1 MiB — and
copies it byte-for-byte to the output path, then reads the copy back
and compares it with the source. It also proves the IDAT payload
actually decompresses, so a CRC-valid but undecodable image cannot
slip through. The image itself was rendered at
build time and is committed as `entry.png`; nothing is drawn while
the entry is graded.

Verified at build time: `python3 main.py /tmp/out.png` produces a
byte-identical copy — sha256
`9eee0ec53ef0f0f1cde9661cdc77f2cee11add34fc16c860b306980d73348d41`
(201,357 bytes).

## Inside the picture

- Giant date masthead and a UTC timeline strip
- 3 illustrated leads
- 12 illustrated panels, each pinned to the dotted world map
- 30 numbered briefs, a DATE CHECK box, and a sources footer
- Original drawings throughout — no photos, no third-party images

---

Built for the [make.fun bounty](https://make.fun/bounty/news-image-20261123).
Play make.fun with my referral link: https://make.fun/r/sc1d8ke0
