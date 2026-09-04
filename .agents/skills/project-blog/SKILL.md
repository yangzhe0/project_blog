---
name: project-blog
description: Create, edit, adapt source articles into, and commit posts for the user's project_blog repository, and add a cover or inline image when needed (draw an SVG for abstract/text content, search Unsplash for specific subjects). Preserve the repository's portable location, existing Markdown format, file layout, image placement, naming conventions, and commit style. Use for personal blog content work, not Astro development, redesign, or deployment configuration.
metadata:
  short-description: Write posts, add images, and commit safely
---

# Project Blog

Use this skill for the user's personal blog content workflow. The same repository may be checked out on Windows or Linux. The cloud host builds and publishes after `git push`; this skill protects the source repository and does not perform cloud builds.

This skill is project-scoped and lives inside the repository at `.agents/skills/project-blog/` (and `.claude/skills/project-blog/`). It is not a global or user-level skill and is not meant for Claude Code on the web.

## Resolve the checkout

Do not hard-code a drive letter, username, home directory, or absolute path.

1. From the current working directory, run `git rev-parse --show-toplevel` and call the result `REPO_ROOT`.
2. Check `git remote get-url origin`. Accept the SSH or HTTPS form of `yangzhe0/project_blog` (normalize an optional `.git` suffix when comparing).
3. Confirm `REPO_ROOT` contains `src/content/posts/`, `src/content/posts/image/`, and `src/content/config.ts`.
4. If the current directory is not a matching checkout, ask the user for its directory. If several checkouts match, ask which one to use. Never guess between them or scan an entire disk.

All paths below are relative to `REPO_ROOT`, so they work in both Windows and Linux checkouts.

## Protect existing work

Before any edit, inspect `git status --short` and the current branch. Preserve unrelated modifications. Never use reset, clean, checkout, broad deletion, or an overwrite to make the tree convenient. If an existing dirty change overlaps the requested file, stop and explain the conflict before editing.

Do not change Astro, Svelte, Tailwind, deployment, site configuration, historical articles, or the existing directory layout unless the user explicitly asks for that separate change. Do not install dependencies, run a site build, preview, formatter, or linter for ordinary post work — the only exception is when the user explicitly asks to build or preview locally.

## Existing content contract

Posts are flat files directly under `src/content/posts/`; images are directly under `src/content/posts/image/`. Keep the established filename form `YYMMDD_Title.md`. Inspect neighboring files to choose the date prefix, title slug, extension, and the next unused image suffix; do not invent a new naming scheme or subdirectory.

Preserve this frontmatter order and the schema in `src/content/config.ts`:

```yaml
---
title: '...'
published: YYYY-MM-DD
description: '...'
image: './image/YYMMDD_01.ext'
tags: [Tag1, Tag2]
category: Notes
draft: false
---
```

Use the categories already present in the repository (`Notes`, `Work`, `LOL`, `Life`) unless the user explicitly requests a change. Keep existing metadata when editing. A non-empty `image` must resolve from the post to a real file in `src/content/posts/image/`. If there is no image yet, leave `image: ''` (empty) — several existing posts do this and the card renders without a cover. Do not add unsupported frontmatter fields, generated files, or dependency files.

The existing `scripts/new-post.js` is only a rough shell generator. It does not decide the final title, metadata, image, draft state, or safe YAML quoting; do not treat its output as finished.

## Convert source material into the user's post

When given a URL, pasted article, local notes, or other source:

1. Access the supplied material and say if it is unavailable, incomplete, paywalled, or not provided. Do not imply that an inaccessible source was read.
2. Separate the source's facts, evidence, instructions, examples, opinions, and open questions. Distinguish those from facts the user personally supplied.
3. Choose the requested mode: a concise source summary, or an independently structured blog post/tutorial. If the request does not make that distinction and it changes the result materially, ask before drafting.
4. For an adapted post, create a new outline and explain the ideas in the user's direct, practical Chinese style. Do not translate line by line, preserve distinctive wording, reproduce the source's structure at length, or present the source's experience as the user's.
5. Do not invent personal tests, screenshots, commands run, results, dates, or opinions. Mark source-reported results as source-reported and label uncertainty.
6. Paraphrase by default. Use only short, necessary quotations with attribution. Add a reference link or attribution when the source materially informs the post. Do not copy source images, diagrams, screenshots, or substantial code unless the user supplied them or has permission; use the user's own assets instead.
7. For technical or time-sensitive claims, verify against authoritative documentation when browsing is available. If verification is not possible, keep the claim qualified rather than asserting it as current fact.

When a post contains command signatures or tables, a literal `|` (pipe) inside a Markdown table cell breaks the table. Rewrite the `|` as `/` (both mean "or") or escape it as `\|`.

## Images: draw an SVG or search a photo

Posts usually need a cover image (frontmatter `image`); inline images are optional. Pick the method by the content, since image and text should complement each other:

- **Text-heavy or abstract content** (concepts, principles, flows) → **draw an SVG**.
- **Content with a specific, concrete subject** (a robot, a tool, a scene) → **search a photo** that approximates it.

### Draw an SVG cover

Generate covers with `scripts/generate_svg_cover.py`; it fills `references/svg-cover-template.svg`, validates the XML, and writes a 1280×448 SVG. This wide source is intentional: Fuwari's small centered `object-cover` card scales it up and exposes roughly the source's central `x=354..926` region, improving legibility without deleting content.

Non-negotiable cover rules:

- Preserve the article title exactly in SVG metadata. Supply it with `--title`, then repeat `--line` 2–4 times to add line breaks. The generator rejects missing letters, numbers, or Chinese characters.
- Visible cover text must not contain punctuation. The generator removes Chinese and ASCII punctuation from title lines, subtitle, and keywords automatically while retaining the original title verbatim in the SVG `<title>` element.
- Keep critical content centered at `x=640`; do not move the title to a left or right column.
- Use the maintained abstract vector frame, ambient glows, nodes, and dot field. Do not replace it with a terminal window, fake application window, or a text-only cover.
- Keep the 1280×448 canvas and all vector geometry fixed. Only title font sizes vary between covers.
- Keep each title line inside the measured `x=354..926` card-safe zone. The generator sizes each line independently and applies an additional 28% width reserve for font fallback and responsive rounding. Prefer semantic line breaks after a product name or clause.
- Do not add a category badge or English strip above the title. Use a concise subtitle and keyword line that complement the complete title. Do not repeat the title as the subtitle.
- Leave `--palette auto` unless the user asks for a color. Auto mode chooses one curated palette from a stable hash of the title, so a series varies in color while the same title remains reproducible. Use `--seed` only when a different stable variation is needed.
- For an existing output, pass `--force` only when replacing that exact cover is authorized.

Run from the repository root, using the path of the skill that was loaded:

```bash
python <SKILL_ROOT>/scripts/generate_svg_cover.py \
  --output src/content/posts/image/YYMMDD_01.svg \
  --title "完整文章标题" \
  --line "第一行（完整标题的一部分）" \
  --line "第二行（完整标题的其余部分）" \
  --subtitle "简洁副标题" \
  --tags "KEYWORD · KEYWORD · KEYWORD" \
  --date "YYMMDD" \
  --palette auto
```

After generation, parse the SVG as XML and render it when a local browser or SVG renderer is available. Inspect both the complete 1280×448 banner and a centered crop matching the actual card. Check that the full title is present, no line enters the decorative edge, supporting text remains legible, no hard-edged vector element extends outside the canvas, and no cropped peripheral word fragments appear. Then set frontmatter `image: './image/YYMMDD_01.svg'`.

### Image naming rule (Strict)

**All** images (covers and inline images, whether SVG, PNG, JPG, JPEG) placed in `src/content/posts/image/` **must strictly follow the `YYMMDD_01.ext`, `YYMMDD_02.ext`, `YYMMDD_03.ext`... naming format**, where:
- `YYMMDD` matches the article's publish date prefix.
- `01`, `02`, `03`... represents the sequence of images used in that post (01 is usually the cover).
- Never use descriptive slug names (e.g. `260708_k8s_arch.png` is forbidden, use `260708_02.png` instead).

### Search a photo (Unsplash)

Run:

```bash
python tools/image_search.py --object "<english keyword>" --number 1
```

The script prints Markdown (`![...](url)` plus photographer attribution) ready to paste as an inline image. For a cover, download the image into `src/content/posts/image/` first.

Keyword rules: English first, prefer scene + action, as specific as possible (e.g. `university student studying library`, not `student`).

### API key and .env

The search script needs an Unsplash Access Key. Keep it in a `.env` file at the skill root (`.agents/skills/project-blog/.env` or `.claude/skills/project-blog/.env`), which is git-ignored:

```
UNSPLASH_ACCESS_KEY=your-access-key
```

- `.env.example` is committed and documents the key name. Copy it to `.env` and fill the real key.
- Never hard-code the key in the script, and never commit `.env`.
- To share or update the search feature, share only the script and `.env.example`; the key stays local.

## Create or edit a post

1. Inspect one or two nearby posts and the content schema before writing.
2. For a new post, choose a non-conflicting `YYMMDD_Title.md` name and keep it flat under `src/content/posts/`. For an edit, preserve the existing filename unless the user explicitly requests a rename.
3. Put only explicitly supplied or newly created post images in `src/content/posts/image/`, using the next available date-number suffix. Update relative references when an image is added or replaced.
4. Keep the change limited to the requested Markdown file and its corresponding images. Do not create notes, reports, build output, or scratch files in the repository.
5. Review `git diff` and `git status`: check frontmatter syntax and order, date/title consistency, category, image paths, accidental files, leaked secrets or tokens, and unrelated changes. This is a content/diff review, not a build validation.

## Commit and publish

Only commit when the user explicitly asks for a commit or has clearly authorized it. Stage exact requested paths, never `git add .`. Existing history uses full-width Chinese-colon messages: new posts normally use `feat：简短说明`; corrections normally use `fix：简短说明`. Keep the message short and describe the actual change.

Treat `git push` as publication. Do not push merely because a commit was requested. Push only after an explicit request to publish/push, and report the branch, commit, and remote afterward. Do not claim the website is live before the push succeeds.

## Stop conditions

Ask before proceeding when the checkout identity is ambiguous, an overlapping dirty change exists, the requested metadata conflicts with the repository schema, the source cannot support a factual claim, or the user asks for a destructive rename/move. Otherwise make the smallest content-only change that satisfies the request.
