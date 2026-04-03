# build123d skill for Claude Code

A skill that teaches Claude Code to create 3D CAD models using [build123d](https://github.com/gumyr/build123d), a Python parametric BREP modeling library built on OpenCascade.

Algebra mode only. Focused API subset. Includes a decomposition strategy for translating natural language descriptions into geometry.

## Install

```bash
git clone https://github.com/you/build123d-skill ~/.claude/skills/build123d
```

## Update

```bash
cd ~/.claude/skills/build123d && git pull
```

## Project-scoped install

To share the skill with everyone who clones a specific project:

```bash
cd your-project
git clone https://github.com/you/build123d-skill .claude/skills/build123d
```

## What's inside

| File | Lines | What it does |
|------|-------|-------------|
| `SKILL.md` | ~160 | Core instructions: workflow, intent-to-shape mapping, tips |
| `references/examples.md` | ~390 | 16 code recipes covering every common pattern |
| `references/api_catalogue.md` | ~650 | Constructor signatures for ~50 key classes and functions |
| `scripts/extract_api.py` | ~130 | Regenerate the catalogue from build123d source |

## Usage

Just ask Claude Code to design something:

```
Design a mounting bracket with 4 screw holes and a slot
```

```
Create a cylindrical enclosure with a snap-fit lid
```

```
Model a pipe elbow with flanges on both ends
```

The skill triggers automatically. Claude will produce a parametric Python script and export STEP/STL files.

## Regenerating the API catalogue

If build123d releases a new version:

```bash
git clone https://github.com/gumyr/build123d /tmp/build123d
BUILD123D_REPO=/tmp/build123d python3 scripts/extract_api.py > references/api_catalogue.md
```

## Prerequisites

The target machine needs `pip install build123d` for the generated scripts to run. The skill itself has no dependencies.

## License

MIT
