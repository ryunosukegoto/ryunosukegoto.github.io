# How to update this site

The site is built by GitHub Pages using Jekyll. **There is no build step to run** — commit and
push, and GitHub rebuilds the site (usually within a minute). If a build ever fails, GitHub emails
you the error.

Almost every update means editing **one file in `_data/`**. Both the English and Japanese pages read
from the same data, so you add things once.

---

## Add a publication

Open [`_data/publications.yml`](_data/publications.yml) and add an entry at the top of the relevant
section. `area` decides which tab it appears on: `compbio` or `epi`.

```yaml
- area: compbio
  year: 2026
  authors: Ryunosuke Goto, A. Coauthor, B. Coauthor
  title: The title of the paper, exactly as published
  venue: Nature Genetics
  url: https://doi.org/10.1234/example
  preprint: false        # true adds a "Preprint" / 「プレプリント」 tag
```

Your own name is bolded automatically — just type it normally in the author list.

**Joint / equal authorship.** Put `*` or `†` directly in the `authors` list — they render as
superscripts — and add a `notes:` block for the legend:

```yaml
  authors: Ronghui Zhu*, Emma Dann*, Jun Yan, Ryunosuke Goto, Alexander Marson
  notes:
    en: '* Joint first authors'
    ja: '*共同筆頭著者'
```

If you omit `ja:`, the English note is used on both pages.

### …or paste BibTeX instead

If you already have the BibTeX (every publisher has an "Export citation" button), let the converter
write the entry for you:

```bash
pbpaste | python3 bin/bib2yml.py --area compbio
```

That prints the YAML block for you to paste in. Add `--append` and it writes straight into
`_data/publications.yml`, at the top of that area:

```bash
python3 bin/bib2yml.py --area epi --append paper.bib
```

It reorders authors from `Goto, Ryunosuke and Naito, Tatsuhiko` into `Ryunosuke Goto, Tatsuhiko
Naito`, converts LaTeX escapes (`{\"o}` → ö, `{\'E}` → É, `---` → —), strips the `{brace
protection}` publishers wrap around titles, builds the URL from the DOI (or from an arXiv eprint id),
and sets `preprint: true` for arXiv/bioRxiv/medRxiv.

**Always read the result before committing.** Publisher BibTeX is routinely wrong about
capitalisation, sometimes drops the period in initials (`Scott L Fleming`), and uses a plain hyphen
where the journal name has an en dash. The converter reproduces its input faithfully, including the
mistakes. It warns on stderr if a required field came out empty.

BibTeX carries no joint-authorship information, so the converter can't produce it. Use `--notes` to
add the legend, and put the `*` markers in by hand afterwards:

```bash
python3 bin/bib2yml.py --area compbio --notes '* Joint first authors' paper.bib
```

Why not a real BibTeX plugin? `jekyll-scholar` is the usual answer, but it is not on GitHub Pages'
allowed-plugin list, so using it would mean replacing the automatic build with a GitHub Actions
workflow you'd have to maintain. This script keeps the zero-build-step deploy.

## Add an award, grant, degree, or media appearance

Same idea, in [`_data/awards.yml`](_data/awards.yml), [`_data/grants.yml`](_data/grants.yml),
[`_data/education.yml`](_data/education.yml), or [`_data/media.yml`](_data/media.yml):

```yaml
- when: 2026
  title:
    en: Some Award
    ja: 何かの賞
  title_url: https://example.org/     # optional, makes the title a link
  where:
    en: Awarding Body
    ja: 授与機関
  where_url: https://example.org/     # optional
  desc:
    en: One line of explanation.      # optional; omit `ja:` to hide it on the Japanese page
```

Leave out a `ja:` line and that text simply won't appear on the Japanese page — which is how the
award descriptions currently work (English only).

## Write a post

Create a file in `_posts/` named `YYYY-MM-DD-short-title.md`:

```markdown
---
layout: default
lang: en
counterpart: posts-ja.html
title: What polygenic scores can and cannot tell us
description: A short summary shown in the posts list.
---

Write in Markdown here.
```

It appears automatically in the Posts tab for that language. Set `lang: ja` for a Japanese post.
Until you add one, the Posts tab shows the "under construction" notice on its own.

## Rename, reorder, or add a tab

[`_data/nav.yml`](_data/nav.yml). The `file:` value must match the page's filename so the active
tab highlights correctly.

## Change wording that appears on every page

[`_data/i18n.yml`](_data/i18n.yml) holds all interface text in both languages — section headings,
the CV link label, the "under construction" message, and so on.

## Change the sidebar, top bar, or `<head>`

[`_layouts/default.html`](_layouts/default.html) — one file, applies to all eight pages.
Reusable pieces live in `_includes/`.

## Change how things look

[`assets/css/site.css`](assets/css/site.css). Plain CSS, no preprocessor. It supports light and dark
mode via `prefers-color-scheme`; colours are defined once as custom properties at the top.

---

## Previewing locally

```bash
bin/preview.sh
```

Builds the site, serves it at <http://127.0.0.1:4000/>, then watches your files and rebuilds every
time you save. Edit a `_data` file, refresh the browser, see the change. Ctrl-C to stop.
`PORT=8080 bin/preview.sh` if 4000 is taken.

If a build fails it says so and leaves the last good version being served, so the browser never
shows a half-built site.

You never *need* this — pushing is enough, and GitHub emails you if its build fails.

<details>
<summary>How it picks a Jekyll</summary>

macOS ships Ruby 2.6, too old for current Jekyll, and `jekyll serve` needs a native gem that won't
compile against it. So the script tries two things in order:

1. `bundle exec jekyll` — the proper route, if you've run `brew install ruby` and `bundle install`.
2. A pinned gem set in `~/.gem-jekyll`, driven through `bin/_jekyll_build.rb`, which calls Jekyll's
   Ruby API directly and so sidesteps the native-gem problem.

If neither is available the script tells you what to install.
</details>

## Hiding a section

Wrap it in a **Liquid** comment, not an HTML comment:

```liquid
{% comment %}
<section class="section">…</section>
{% endcomment %}
```

An HTML `<!-- -->` comment only hides the section from *display* — Liquid still runs, and the content
ships inside the page source where anyone can read it via View Source. That matters for things like
grant amounts. `{% comment %}` emits nothing at all.

The Home page sections are assembled in
[`_includes/home-sections.html`](_includes/home-sections.html). The **Grants** section is currently
hidden this way — delete the `{% comment %}` / `{% endcomment %}` lines around it to show it again.

## Things to know

- **`archive/`** holds the pre-reboot version of the site as plain HTML. Those files have no Jekyll
  front matter, so Jekyll copies them through untouched. Don't add front matter to them.
- **The CV filename is all lowercase** (`CV_ryunosuke_goto.pdf`) because that is the name recorded in
  git. The file on disk is capitalised, but macOS is case-insensitive and git never noticed the
  rename, so the lowercase name is what GitHub Pages actually serves. See
  [`archive/README.md`](archive/README.md) if you want to change it.
- **`_config.yml` excludes** the `gene_centric_*` and `sparse-direct-effects-*` research files, so
  they won't be published even if they get committed by accident.
- **Publication lists are ordered by the file, not sorted automatically.** Add new entries at the
  top of their section.
