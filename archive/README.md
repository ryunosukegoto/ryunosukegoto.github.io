# Archive

Snapshots of previous versions of this site, kept so any earlier design can be restored or referenced.

## `2026-08/` — pre-reboot version

The single-page HTML5 UP "Read Only" version of the site that was live until the August 2026 reboot.

- English: [`2026-08/index.html`](2026-08/index.html) — live at `/archive/2026-08/`
- Japanese: [`2026-08/japanese.html`](2026-08/japanese.html) — live at `/archive/2026-08/japanese.html`

These are faithful copies of the pages as they were, with two mechanical changes so they still render from
this subdirectory:

1. Relative paths to `assets/`, `images/`, the paper thumbnails, and the PDFs were prefixed with `../../`.
2. The English/Japanese cross-links now point within the archive, and an amber notice bar at the top links
   back to the current site.

Known pre-existing issues, left as-is for fidelity: both pages reference `assets/js/jquery.scrollex.min.js`,
`assets/js/jquery.scrolly.min.js`, and `favicon.ico`, none of which have ever been present in this repo.
They 404 on the original site too; the pages degrade gracefully without them.

### A note on the CV filename

Everything here links the CV as `CV_ryunosuke_goto.pdf` (all lowercase), because that is the name actually
recorded in git and therefore the name GitHub Pages serves. The file in the working directory is named
`CV_Ryunosuke_Goto.pdf`, but macOS is case-insensitive and this repo has `core.ignorecase = true`, so git
never noticed the rename and still tracks the lowercase name. Confirmed live:

- `https://ryunosukegoto.github.io/CV_ryunosuke_goto.pdf` → 200
- `https://ryunosukegoto.github.io/CV_Ryunosuke_Goto.pdf` → 404

If you would rather the published filename be properly capitalized, force the rename into git and then
update the 14 links across the site:

```bash
git mv CV_ryunosuke_goto.pdf CV_tmp.pdf && git mv CV_tmp.pdf CV_Ryunosuke_Goto.pdf
```

### Restoring this version

The commit immediately before the reboot is also tagged, so the whole tree can be recovered:

```bash
git checkout v1-pre-reboot
```

To bring just the old pages back to the site root:

```bash
git checkout v1-pre-reboot -- index.html japanese.html
```
