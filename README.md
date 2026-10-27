# sabren/blaze

> Team Trailblazer's PyWeek game work (2006–2007): three competition
> entries plus the shared pygame library they were built on, an IRC
> log bot, and a sandbox of experiments. The games are complete,
> playable, Python/pygame artifacts of the PyWeek era.
> Repo: https://github.com/sabren/blaze — 416 files, git history in
> this clone 2007-04-06 → 2007-09-19. **Keep — and hand to GodotBot
> for arcade porting (see below).**

## What it is

`blaze` is the code of Team Trailblazer, a PyWeek competition team
whose site was `blazeofglory.org` (named across the READMEs). The
repo holds the team's shared library, three games, a bot, and a
sandbox — all Python 2 + pygame, all GPL-licensed (the LICENSE.txt
files say GPL v2).

## The games

- **Forest-Patrol** (`Forest-Patrol/`) — a preparation game: "A simple
  game to 1: Prepare for pyweek, and 2: exercise directicus and see
  what could be done with it in future." Copyright 2007 Team
  Trailblazer. A ranger-with-bow game with its own art and audio:
  `lib/` holds `game.py`, `level.py`, `menus.py`, `sprites.py`,
  `resources.py`; `data/` holds animations (walk/shoot), sprites
  (ranger, castle, trees, grass), cursors (arrow, sword), a font,
  and music/sound effects (`battle.mp3`, `menu.mp3`, `winner.wav`,
  `loser.wav`, arrow/sword sounds). Requires "the latest version of
  python and pygame as well as our team lib Directicus". (The README
  says to run `run.py`; no `run.py` is present at the top level of
  the directory in this checkout — the entry point as committed is
  `Forest-Patrol.py`/`Forest-Patrol.pyw`. Flagged as a discrepancy,
  not resolved.)
- **Clad in Iron** (`pyweek2/`, "CII") — the team's PyWeek #2 entry
  (copyright 2006 in `main.py`). A top-down shooter with a
  steam-powered ironclad warship as the hero: WASD rudder movement,
  mouse-aimed left/right cannons, shore-based artillery enemies that
  "will not move but their weapons will eventually destroy your ship
  if you give them time". Requires Python 2.4+, pygame 1.7+, and the
  bundled `eventnet` library. Ships with its own tile-based level
  editor (`leveleditor/`), a jukebox sound engine (`jukebox.py`),
  a state machine (`states.py`), scrolling (`scrolling.py`), and
  sprites (`sprites.py`). The README credits the team by handle:
  Micah (mcferrill, team lead), Todd (Nuclear Ghecko), Adam
  (pyTM30), Vinko (Yango), Don (cooldmz), Andreas (DocTiger/elTigre),
  plus Danc Redmond for the tileset. The `steamship_draft2.jpg` in
  the directory is concept art for the ship.
- **Ascent of Justice** (`pyweek4/`) — the PyWeek #4 entry
  (https://www.pyweek.org/4/, team Trailblazer, member mcferrill).
  A side-view action game: arrow keys move, Left Control kicks, Left
  Alt punches, Left Shift sprints. Ships with a level generator
  (`levelGen.py`: `python levelGen.py <filename> <width> <height>`)
  and a level editor (`levelEdit.py`: arrow keys scroll, left mouse
  places, right mouse deletes). Its TODO.txt is honest about the
  state: "Save game doesn't work", "Cameras see through walls",
  "Ladders are dead", "Recieved complaints about freezing after
  'New Game'", "Gravity is too weak", "Add jumping again?" —
  this is a competition-week game, rough edges included. Requires
  Python, pygame, and Directicus.
- **pyweek/** (unnamed first entry) — the earliest game skeleton in
  the repo: a state-machine game (`main.py` with `Menu`/`Game`/
  `LevelList` states, `states.py`, `display.py`, `events.py`,
  `soundtrack.py`) with physics experiments (`physics.py`,
  `roomphysics.py`, `ode_to_pixel.py`, pyode-based demos requiring
  pyopengl and numeric) and SVG room art (`rooms/*.svg`, concept
  art in `concept/*.svg`). Its README is an unfilled skeleton
  ("What is it?" and "How to play." are blank), and no title for
  this game appears anywhere in the directory — so none is given
  here. The ASCII level sketch in the README (a room with a
  `.` path and a `\` ramp) is the only gameplay hint.

## The shared library: directicus

`directicus/` is the team's pygame helper library, and the reason the
games share a feel. Its README: "Directicus is latin for 'simple',
pointing to its purpose — to be a simple, flexible, and easy to use
code library. It builds on pygame and adds a few simple yet useful
components like pixel-perfect collision detection, menus, a state
engine, and things like that." Modules: `engine.py` (state engine),
`gfx.py` (animations, image storage), `sprite.py` (sprites, animated
sprites), `sfx.py` (sound/music engine with distance falloff),
`gui.py`, `layer.py`, `event.py` — each runnable standalone as its
own demo. A `release/` directory holds a packaged
`directicus-0.1` (Windows exe plus source tarball/zip).

## Everything else

- **BlazeBot** (`BlazeBot/`) — an IRC bot, not a game: started via
  an "undisclosed URL", it joins an IRC server/channel and takes
  admin commands from IRC (`BOT: admin`, `ban`, `start`, `stop`,
  `post`, `reset`, `disconnect`) to record a channel log and post it
  to the website. `irclib.py`/`ircbot.py` are the protocol code.
- **sandbox/** — experiments and leftovers: an early `eventnet`
  library copy, explosion-animation bitmaps, a `pydogfight.tar.bzip2`
  archive, SVG world art, and a "Screenshot-Clad in Iron.png".
- **CVSROOT/** — the repo is a CVS import (the `CVSROOT/` config
  files are committed in the tree), which is why the layout mixes
  project directories with version-control internals.

## Tech stack

Python 2.4–2.5, pygame 1.7+, plus pyode/pyopengl/numeric for the
physics demos and `eventnet` (bundled) for the state/event system.
Windows executables were produced (py2exe-era: `setup.py` files,
`.pyw` launchers, a packaged `directicus-0.1` exe). No test suite
beyond the `unittest` cases embedded in `pyweek/main.py`.

## Inventory (highlights)

| Path | Contents |
|------|----------|
| `Forest-Patrol/` | PyWeek prep game: ranger/bow game, full art + audio, `lib/` engine |
| `pyweek2/` | **Clad in Iron**: top-down ironclad shooter + tile level editor |
| `pyweek4/` | **Ascent of Justice**: PyWeek #4 action game + level generator/editor |
| `pyweek/` | Unnamed first entry: state-machine game skeleton, pyode physics demos, SVG rooms |
| `directicus/` | Shared pygame library (engine/gfx/sprite/sfx/gui/layer) + 0.1 release |
| `BlazeBot/` | IRC log bot (admin commands, post-to-website) |
| `sandbox/` | Experiments: eventnet copy, explosion bitmaps, pydogfight archive |
| `CVSROOT/` | Committed CVS configuration (this repo is a CVS import) |

## Surprising / notable

- **Three finished games, one library:** this is a real team's
  competition history, not a single demo — and `directicus` is the
  through-line that makes the games a body of work rather than
  three unrelated entries.
- **Clad in Iron is the most complete game here:** a playable
  shooter with an editor, a jukebox, and a credits list — the kind
  of PyWeek entry that holds up as a game, not just as code.
- **Ascent of Justice's TODO is the honest artifact:** a
  competition game mid-fix-list (broken saves, see-through cameras,
  dead ladders) is exactly what a week-long build looks like.
- **The arcade connection is direct:** these are small, complete,
  sprite-based pygame games with their own art and audio — the same
  shape as the Godot ports already on
  https://tangentstorm.github.io/arcade/ (see the cardinalrule and
  spiders-v-aliens docs). That is why the disposition below is
  porting, not just preservation.
- No linked streams or videos found in the repo.

## Verdict

Keep — and port. The games are worth preserving as PyWeek history,
and Clad in Iron, Ascent of Justice, and Forest-Patrol are all
plausible arcade ports: small scope, complete art/audio, self-contained
code. **Separate GTD inbox item filed alongside this doc: hand blaze
to GodotBot for arcade porting.**
