# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A **Quarto** template for master's dissertations and doctoral theses at IESP-UERJ
(Instituto de Estudos Sociais e Políticos, Universidade do Estado do Rio de
Janeiro), following Brazilian ABNT norms. Authors write in Markdown/Quarto
(`.qmd`) and render a PDF identical to the institute's official LaTeX model.

It is a Quarto port of the LaTeX `repUERJ` model by **Mateus Pestana**
(<https://github.com/mateuspestana/modelo_latex_iespuerj>); the `repUERJ` class
itself derives from Prof. Luís Fernando de Oliveira's work. Most template prose is
in Brazilian Portuguese; an English variant is driven by a YAML flag.

## Building the PDF

Build with Quarto (it handles the pdflatex + citeproc passes automatically):

```sh
quarto render main.qmd       # Portuguese example -> main.pdf
quarto render main-en.qmd    # English example   -> main-en.pdf
```

Requires Quarto ≥ 1.4 and a `pdflatex` (TinyTeX: `quarto install tinytex`). The
engine is **pdflatex** (the class uses `mathptmx`/`inputenc`, not Unicode engines),
set in the extension — do not switch to lualatex/xelatex.

`main.pdf` is the committed rendered example. `Modelo_de_tese_IESP_UERJ.pdf` (the
original LaTeX output) was used to verify formatting fidelity and then removed.

## Architecture

The repository is a **Quarto extension**. The root holds only what an author
edits; the "engine" lives in `_extensions/iesp-uerj/`.

- **[main.qmd](main.qmd)** / **[main-en.qmd](main-en.qmd)** — example documents an
  author edits. YAML front matter carries all metadata (`title`, `author-*`,
  `advisor`, `degree`, `banca`, `resumo`, `abstract`, keywords, optional lists);
  the body is the chapters in Markdown. Both select `format: iesp-uerj-pdf` and end
  with a `# Referências`/`# References` heading + `::: {#refs} :::` block where
  citeproc injects the reference list.
- **[_extensions/iesp-uerj/_extension.yml](_extensions/iesp-uerj/_extension.yml)** —
  defines the `iesp-uerj-pdf` format: `template.tex`, `csl: abnt.csl`,
  `pdf-engine: pdflatex`, `top-level-division: chapter`, and `format-resources`
  (the `.cls`/`.sty`/images copied next to the intermediate `.tex` so pdflatex
  finds them).
- **[_extensions/iesp-uerj/template.tex](_extensions/iesp-uerj/template.tex)** —
  the Pandoc LaTeX template. Maps YAML → `repUERJ` metadata macros, fixes
  Pandoc/class incompatibilities (see below), and switches labels PT↔EN via
  `$if(lang-en)$` blocks.
- **[_extensions/iesp-uerj/repUERJ.cls](_extensions/iesp-uerj/repUERJ.cls)** — the
  self-contained document class (does not `\LoadClass`; reimplements a book-style
  class). Defines `\capa`, `\folhaderosto`, `\fichacatalografica`,
  `\pretextualchapter`, `\postextualchapter`, `\sumario`, etc.
- **[_extensions/iesp-uerj/repUERJformat.sty](_extensions/iesp-uerj/repUERJformat.sty)** —
  ABNT formatting: margins, spacing, the `folhadeaprovacao` environment,
  captions/legends, and the metadata setters (`\autor`, `\titulo`, `\orientador`,
  `\grau`, `\curso`, `\palavraschaves`, etc.). PT labels are set via
  `\addto\captionsbrazil`.
- **[_extensions/iesp-uerj/abnt.csl](_extensions/iesp-uerj/abnt.csl)** — ABNT
  NBR 6023:2018 + NBR 10520:2023 citation style (from virgilinojuca/csl-abnt). It
  was edited to remove `et-al-use-last="true"` (root `<style>`), which produced an
  invalid "first … last" in-text form; ABNT wants "First et al." for 4+ authors.

### Key conventions when editing the template

- **Citations use citeproc, NOT abntex2cite.** The template defines the canonical
  Quarto `$if(csl-refs)$` block (`\citeproctext`, `CSLReferences`, etc.); if
  references break, that block is the first place to check. The reference list is
  positioned by the `::: {#refs}` div in the `.qmd`, not by the template.
- **Citation casing** follows NBR 10520:2023: `(Amado, 1991)` in text (initial
  caps), `AMADO, Jorge.` in the reference list (uppercase). That is correct, not a
  bug.
- **`figure`/`table` are patched** in `template.tex` back to the standard
  `[pos]`-only signature (the class redefines them with a mandatory `{width}` arg
  that is incompatible with Pandoc output).
- **Duplicate-TOC fix**: `repUERJ`'s `\@schapter` adds a bold-uppercase TOC entry
  for `\chapter*`, and Pandoc adds another via `\addcontentsline`. `template.tex`
  suppresses the duplicate with an `\if@uerj@suppress@nexttoc` flag.
- **English variant** (`lang-en: true`): `template.tex` loads
  `babel[main=english]`, overrides labels via `\addto\captionsenglish`, renames
  `\orientadornome`→Advisor / `\abrevnome` / `\simbnome`, swaps `\cabecalho`/
  `\headertext` so the PT Resumo header shows the PT title and the EN Abstract
  header the EN title, and orders Abstract before Resumo. The ficha catalográfica
  and folha de aprovação intentionally stay in Portuguese.
- **`.bib` encoding**: prefer precomposed UTF-8. Entries with `\i` + accent (e.g.
  `cient{\'\i}fica`) make citeproc emit a decomposed dotless-i + combining acute
  that pdflatex's `inputenc` cannot compose; `bibliografia.bib` was normalized to
  `í`.
