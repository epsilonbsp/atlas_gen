# Atlas Gen

Generates a texture atlas from `.ttf` fonts using [msdf-atlas-gen](https://github.com/Chlumsky/msdf-atlas-gen). Produces a single PNG atlas and per-font JSON glyph data.

## Requirements

- Python 3.10+
- Windows (msdf-atlas-gen binary is win64)

## Usage

**Install dependencies** (downloads msdf-atlas-gen and optionally the Space Mono sample fonts):

```
python build.py install
```

**Generate atlas** from fonts in `input/fonts/`:

```
python build.py generate
```

Output is written to `output/`:
- `output/atlas.png` — texture atlas
- `output/fonts/<name>.json` — glyph data for each font

## Input

Place `.ttf` files in `input/fonts/`. The atlas size is determined automatically to minimize area.
