# Trailguess

A daily "guess the rig" game for the group, in the spirit of Playcardle:
5 guesses, image reveals more each miss, guess Vehicle / Era / Trip from dropdowns,
green (correct) / yellow (adjacent on the timeline) / red (way off) feedback, with an
arrow telling you whether the real answer is earlier or later.

## Files
- `index.html` — the whole game (UI + logic)
- `vehicles.json` — each vehicle + its era timeline in order (e.g. Stock → LS Swap → Bullbar)
- `trips.json` — every trip, in chronological order (this order IS the timeline used for "close" guesses)
- `puzzles.csv` — **the answer key you actually edit.** One row per day: date, image, focus point, and which vehicle/era/trip.
- `puzzles.json` — generated file, built from `puzzles.csv`. Don't hand-edit this.
- `build_puzzles.py` — run this after editing `puzzles.csv`; it validates every ID and regenerates `puzzles.json`
- `images/` — the photos. One real one (`Juans_Truck-Stock-Letts_Lake.png`) plus 2 placeholders so you can test the mechanic before swapping in real ones.

## How the answer key works
Don't hand-edit `puzzles.json`. Instead:
1. Add vehicles/eras to `vehicles.json`, trips to `trips.json` (append to the end — order matters, it's the timeline).
2. Add a row to `puzzles.csv` for each day, referencing the IDs you just added.
3. Run `python3 build_puzzles.py` — it'll error out with the exact bad row if you typo an ID, rather than silently breaking the game.

Filenames like `Juans_Truck-Stock-Letts_Lake.png` are still a good habit for browsing
the folder yourself, but the game never parses them — the CSV row is the source of truth.

## Scoring
Same idea as Cardle: each of the 3 fields scores `(6 − the guess number you solved it on)`,
so solving all 3 on guess 1 = 15 pts, on guess 2 = 12 pts, etc. Unsolved fields score 0.
Max 15/day.

## Running it locally
Because `index.html` fetches `puzzles.json`, you can't just double-click the file —
browsers block `fetch()` on `file://` paths. Run a tiny local server instead:

```
cd cardle-clone
python3 -m http.server 8000
```
Then open `http://localhost:8000`.

## Putting it on GitHub Pages
1. Create a repo, push these files to the `main` branch.
2. Repo Settings → Pages → Deploy from branch → `main` / root.
3. Your game will be live at `https://<username>.github.io/<repo>/`.

If you want the repo **private** (recommended if you care about answers being
spoilable — see below), GitHub Pages from a private repo requires GitHub Pro/Team,
or a GitHub Actions workflow that publishes a public `docs/` folder from a private
source repo. Happy to set that workflow up if you want to go that route — just
say the word.

## Adding a new day's puzzle
1. Make sure the vehicle/era exists in `vehicles.json` and the trip exists in `trips.json`.
2. Add a row to `puzzles.csv`:

```
date,image,focusX,focusY,vehicleId,eraId,tripId
2026-07-25,images/2026-07-25.jpg,55,60,clay_4runner,y2001,anza_borrego_2018
```

- `date` is matched against **Pacific Time** (handles PST/PDT automatically), so the
  new puzzle goes live at midnight PT — decided this since most of the group leans US.
- `focusX`/`focusY` (0–100) is the point the zoomed-in crop centers on — pick the
  most identifying detail (grille, sticker, roof rack) rather than dead center, or
  the first guess will be too easy or impossible.
3. Run `python3 build_puzzles.py`.

## Real challenges, decided so far

1. **Spoilers.** Public repo, honor system — decided. Everyone in the group can
   technically see the answer key and images in the repo if they go looking; that's
   an accepted tradeoff for simplicity, not a secret.
2. **Timezone.** Midnight Pacific Time for everyone, regardless of where a given
   friend actually lives. That'll be earlier evening for you in Australia and won't
   be "midnight" locally for anyone outside California — that's expected, not a bug.
3. **Repo size.** Keep images to roughly 1200–1600px long edge, JPEG ~80% quality.
   Keeps hundreds of camping photos well under GitHub's 1GB soft limit.
4. **Guess matching.** Dropdowns instead of free text — no typo/synonym problem
   anymore, but it does mean every vehicle/era/trip needs to be added to
   `vehicles.json`/`trips.json` *before* it can be used in a puzzle. This is the
   one-time setup cost: build out the full timelines first, then puzzles are quick to add.
5. **"Close" only works within a timeline.** Yellow/adjacent logic is based on list
   *order* in `vehicles.json`/`trips.json`, not on actual date math — so keep those
   lists in true chronological order as you add to them, or the arrows will lie.
