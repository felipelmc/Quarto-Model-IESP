# IESP-UERJ Quarto template for dissertations and theses

A [Quarto](https://quarto.org) template for master's dissertations and doctoral
theses at **IESP-UERJ** (Institute of Social and Political Studies, Rio de Janeiro
State University), following Brazilian ABNT standards. Write your work in
Markdown/Quarto (`.qmd`) and produce a PDF identical to the institute's official
LaTeX model.

> 🇧🇷 A versão em português deste guia está em [README.md](README.md).

## ABNT compliance

The template follows the **latest** revisions of the standards:

- **NBR 14724:2024** — presentation of academic works (structure; pre-textual
  pages counted but not numbered; cataloguing sheet without AACR2).
- **NBR 6023:2018** — references (author surnames in UPPERCASE in the reference
  list).
- **NBR 10520:2023** — citations. The key change: the author surname in
  parenthetical citations is now in **initial caps** — `(Amado, 1991)` instead of
  `(AMADO, 1991)`; `et al.` in italics from 4 authors onward.

Citations are processed by **citeproc** (Quarto's native engine) using the CSL
`_extensions/iesp-uerj/abnt.csl` (NBR 6023:2018 + 10520:2023), **not** by
`abntex2cite`, which is still stuck on the 2002 casing.

## Requirements

1. **Quarto** ≥ 1.4 — <https://quarto.org/docs/get-started/>
2. A **LaTeX** distribution with `pdflatex`. The simplest is TinyTeX:
   ```sh
   quarto install tinytex
   ```
   (or a full TeX Live installation).

## Repository layout

```
.
├── _quarto.yml              # Quarto project (lets the subfolders find _extensions/)
├── pt/                      # PORTUGUESE example
│   ├── main.qmd             #   edit this file
│   ├── bibliografia.bib     #   reference database (BibTeX)
│   ├── regressao.png        #   example figure
│   └── main.pdf             #   rendered PDF
├── en/                      # ENGLISH example
│   ├── main.qmd
│   ├── bibliography.bib
│   ├── regression.png
│   └── main.pdf
├── tools/
│   └── make_figures.py      # regenerates the example figures
└── _extensions/iesp-uerj/   # the "engine" — no need to edit
    ├── _extension.yml       # defines the iesp-uerj-pdf format
    ├── template.tex         # LaTeX template (PT/EN labels)
    ├── repUERJ.cls          # IESP-UERJ LaTeX class
    ├── repUERJformat.sty    # ABNT formatting rules
    ├── repUERJpseudocode.sty
    ├── abnt.csl             # ABNT 2023 citation style
    └── logo / marcadagua    # cover and title-page images
```

## Usage

1. Edit the YAML metadata at the top of `en/main.qmd` (see the table below).
2. Write your chapters in the document body, in Markdown.
3. Render from the **repository root**:
   ```sh
   quarto render en/main.qmd     # -> en/main.pdf
   quarto render pt/main.qmd     # -> pt/main.pdf
   quarto render                 # renders both at once
   ```

> Always render from the root (where `_quarto.yml` lives): that file is what lets
> Quarto locate the `_extensions/iesp-uerj` extension from `pt/`/`en/`.

To start a new work, edit inside `en/` (or `pt/`) — each folder is self-contained
(`main.qmd` + `.bib` + figures).

## Reproducibility

Everything needed to build the PDFs is versioned in the repository — just **clone
and render**, with no manual steps and no internet access:

```sh
git clone https://github.com/felipelmc/Quarto-Model-IESP.git
cd Quarto-Model-IESP
quarto render            # builds pt/main.pdf and en/main.pdf
```

- The extension (class, `.sty`, CSL, logos) lives in `_extensions/iesp-uerj/` —
  nothing is downloaded at render time.
- The example figures (`pt/regressao.png`, `en/regression.png`) are versioned. To
  **regenerate** them from code (needs Python with `numpy` and `matplotlib`):
  `python3 tools/make_figures.py`.
- On the first render, TinyTeX automatically installs any missing LaTeX packages.
  Install TinyTeX with `quarto install tinytex`.

### Writing in English

The English example sets `lang-en: true` in the YAML. This switches the structural
labels to English (Contents, References, List of Tables…) and places the
**Abstract before the Resumo**. A **Portuguese Resumo is still required by ABNT**
even for theses written in English, so both are produced.

By Brazilian institutional convention, the **cataloguing sheet** (ficha
catalográfica) and the **approval sheet** (folha de aprovação) remain in
Portuguese even in the English version.

### YAML fields

| Field | Description |
|---|---|
| `lang-en` | `true` to render English labels (omit it for Portuguese). |
| `university`, `inst-center`, `unit` | Institution (3 cover-header lines). |
| `author-first`, `author-last`, `author-abbrev` | Author name, surname and initial(s). |
| `title` | Main title (cover + the same-language abstract header). |
| `title-en` | Title in the other language (the secondary abstract header). |
| `degree` | `Mestre`, `Doutor`, `Bacharel` or `Licenciado` (class keyword). |
| `program` | Graduate program (e.g. `Ciência Política`). |
| `city`, `day`, `month`, `year` | Place and date. |
| `advisor` | Advisor: `title`, `first`, `last`, `institution`. |
| `co-advisor` | Co-advisor (optional, same structure). |
| `kw-pt-1`…`kw-pt-4` / `kw-en-1`…`kw-en-4` | Keywords (4 slots per language; `""` for empty). |
| `banca` | Examination board members (`name`, `institution`; max 6). |
| `dedicatoria`, `agradecimentos`, `epigrafe` | Pre-textual elements (free text). |
| `resumo`, `abstract` | Resumo (PT) and Abstract (EN). |
| `thesis-nature` | (Optional) Nature-of-the-work text on the title page. |
| `abreviaturas`, `simbolos`, `glossario`, `apendices`, `anexos` | Optional lists (see `en/main.qmd`). |
| `bibliography` | `.bib` file (default: `bibliography.bib`). |

### Hiding pre-textual pages

To turn off specific pages, uncomment the matching flag in the YAML (all pages are
on by default):

```yaml
hide-ficha: true            # cataloguing sheet (ficha catalográfica)
hide-banca: true            # approval sheet (folha de aprovação)
hide-dedicatoria: true      # dedication
hide-agradecimentos: true   # acknowledgements
```

> The approval sheet, dedication and acknowledgements also disappear automatically
> if you drop the `banca`, `dedicatoria` or `agradecimentos` fields. The `hide-*`
> flags let you turn them off while keeping the content in the file.

### Citations

Use Pandoc citation syntax with the `.bib` keys:

- `[@bib:Amado1991]` → parenthetical: **(Amado, 1991)**
- `@bib:Andrade1997` → narrative: **Andrade (1997)**
- `[@keyA; @keyB]` → multiple citations.

The **References** list is generated automatically at the end of the document, so
the example ends with:

```markdown
# References {.unnumbered}

::: {#refs}
:::
```

Keep this block at the end of your document.

## Known limitations

- The ABNT CSL may need manual touch-ups in edge cases (subtitles render in bold;
  author-less works whose title acts as the entry). See
  [virgilinojuca/csl-abnt](https://github.com/virgilinojuca/csl-abnt).
- `.bib` entries using `\i` (dotless i) with an accent — e.g. `cient{\'\i}fica`
  — may fail under pdflatex. Prefer precomposed UTF-8 (`científica`).

## Credits

- **Original LaTeX model (`repUERJ` class)**: [Mateus Pestana](https://github.com/mateuspestana/modelo_latex_iespuerj).
- The `repUERJ` class derives from work by Prof. Luís Fernando de Oliveira.
- ABNT 2023 citation style (CSL): [virgilinojuca/csl-abnt](https://github.com/virgilinojuca/csl-abnt).
- Quarto port: this repository.

## License

See [LICENSE](LICENSE).
