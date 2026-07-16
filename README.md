# u1-force-macros

A co-repo of Bespok3d plugins for the Snapmaker U1 that publishes its own sub-list.

Plugins:

- **force-bed-mesh-adaptive** - Mesh just the area your model covers, before each print.
- **force-bed-mesh** - Always run a full bed mesh before each print.
- **force-timelapse** - Capture a timelapse on every print, no app toggle needed.
- **print-prefs-core** - Shared engine for the print-start 'force' options.

## Layout

```text
u1-force-macros/
  <plugin-id>/          # one plugin = one dir; its name is the manifest .name
    manifest.json
    files/              # payload the daemon places on the printer
    doc/README.md       # rendered in-app; not deployed
  .github/workflows/release.yml
  index.json            # the published sub-list (committed; referenced by main-index lists[])
  dist/                 # build output (gitignored)
```

Each plugin declares WHAT (a destination `class` + a `restart` hook), never a path or a raw
command; the printer-side adapter realizes it. See `Bespok3d/doc/anatomy-of-a-plugin.md`.

## Build locally

Needs Node.js 20+. Builds run through the shared `Bespok3d/b3-builder` tool:

```sh
npm install github:Bespok3d/b3-builder
npx b3-builder build --source ./force-bed-mesh --atom-repo Bespok3d/u1-force-macros
# -> dist/force-bed-mesh-<ver>.b3 + dist/force-bed-mesh.atom.json
```

Drop `--source` to build every plugin in the repo at once.

## Releasing

Bump a plugin's `manifest.json` `version` and push to `main`. CI runs the `Bespok3d/b3-builder`
Action over the whole repo, which packs each `.b3`, cuts a release per plugin, assembles this repo's
`index.json` sub-list as `U1 Force Macros`, and registers it in `Bespok3d/main-index`
(`lists/<repo>.json`). Secret: `MAIN_INDEX_TOKEN` (contents:write on main-index). Signing deferred.

## Maintainership

These plugins are published and maintained by the Bespok3d org, and several of them repackage or
build on upstream source material. If you own the source material a plugin is based on and would
rather manage it yourself, you are welcome to contact the org to claim it back. The one condition is
that it stays actively maintained: a claimed plugin left to rot will be reclaimed so users are never
stranded on an abandoned package.
