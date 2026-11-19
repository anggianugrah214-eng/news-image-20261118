# The World Today — Wednesday 18 November 2026

A newspaper front page for one day's world news, drawn entirely in code
with Python and Pillow (`draw_image.py`, 1024 × 1024). No photographs or
outside images are used: every picture on the page — the summit table, the
rocket, the ballot box, the drone, the chip — is drawn from shapes.

## The six stories

1. **Lead — Shenzhen.** Xi Jinping and Vladimir Putin meet in Shenzhen
   ahead of Thursday's three-way summit with President Trump.
2. **Space.** NASA's Voyager 1 reaches one light-day from Earth — 16
   billion miles out, its signal now taking 24 hours to arrive.
3. **United States.** Mary Peltola wins Alaska's Senate seat, giving
   Democrats a 56–44 majority; she is the first Alaska Native senator.
4. **Middle East.** Drones from Iran reach Kuwait, where Ali Al Salem
   base engaged them; Bahrain intercepted more.
5. **Asia.** Quad leaders meet in Manila — their first leaders' meeting
   in more than two years — alongside a Philippines trade deal.
6. **Technology.** OpenAI launches GPT-6.2 Astra and Sol, with lower
   API prices for developers.

## Running it

```sh
python3 draw_image.py        # regenerates entry.png
MAKEFUN_OUTPUT_DIR=out node main.ts   # copies entry.png to out/
```

`main.ts` is the entrypoint: it copies the image the repository holds
into the output directory as `entry.png`.

## License

MIT — see `LICENSE`.
