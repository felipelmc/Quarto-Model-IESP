# Modelo Quarto de dissertações e teses do IESP-UERJ

Modelo [Quarto](https://quarto.org) para dissertações de mestrado e teses de
doutorado do **IESP-UERJ** (Instituto de Estudos Sociais e Políticos da
Universidade do Estado do Rio de Janeiro), seguindo as normas ABNT. Permite
escrever o trabalho em Markdown/Quarto (`.qmd`) e gerar um PDF idêntico ao modelo
LaTeX oficial do instituto.

> 🇬🇧 An English version of this guide is available in [README.en.md](README.en.md).

## Conformidade ABNT

O modelo segue as versões **mais recentes** das normas:

- **NBR 14724:2024** — apresentação de trabalhos acadêmicos (estrutura, páginas
  pré-textuais contadas mas não numeradas, ficha catalográfica sem AACR2).
- **NBR 6023:2018** — referências (sobrenomes em CAIXA-ALTA na lista de
  referências).
- **NBR 10520:2023** — citações. A principal mudança: o sobrenome do autor na
  citação entre parênteses agora vem em **inicial maiúscula** — `(Amado, 1991)`
  em vez de `(AMADO, 1991)`; `et al.` em itálico a partir de 4 autores.

As citações são processadas pelo **citeproc** (motor nativo do Quarto) usando a
CSL `_extensions/iesp-uerj/abnt.csl` (NBR 6023:2018 + 10520:2023), e **não** pelo
`abntex2cite`, que continua preso à grafia de 2002.

## Pré-requisitos

1. **Quarto** ≥ 1.4 — <https://quarto.org/docs/get-started/>
2. Uma distribuição **LaTeX** com `pdflatex`. A mais simples é o TinyTeX:
   ```sh
   quarto install tinytex
   ```
   (ou uma instalação TeX Live completa).

## Estrutura do repositório

```
.
├── main.qmd                 # exemplo em português (edite este arquivo)
├── main-en.qmd              # exemplo em inglês
├── bibliografia.bib         # base de referências (BibTeX)
├── main.pdf / main-en.pdf   # PDFs renderizados de exemplo
└── _extensions/iesp-uerj/   # o "motor" — não precisa editar
    ├── _extension.yml       # define o formato iesp-uerj-pdf
    ├── template.tex         # template LaTeX (rótulos PT/EN)
    ├── repUERJ.cls          # classe LaTeX do IESP-UERJ
    ├── repUERJformat.sty    # regras de formatação ABNT
    ├── repUERJpseudocode.sty
    ├── abnt.csl             # estilo de citação ABNT 2023
    └── logo / marcadagua    # imagens da capa e folha de rosto
```

## Como usar

1. Edite os metadados no cabeçalho YAML de `main.qmd` (veja a tabela abaixo).
2. Escreva os capítulos no corpo do documento, em Markdown.
3. Renderize:
   ```sh
   quarto render main.qmd
   ```
   O resultado é `main.pdf`.

Para começar um trabalho novo, copie `main.qmd` (e `bibliografia.bib`) e mantenha
a pasta `_extensions/` ao lado.

### Campos do YAML

| Campo | Descrição |
|---|---|
| `university`, `inst-center`, `unit` | Instituição (3 linhas do cabeçalho da capa). |
| `author-first`, `author-last`, `author-abbrev` | Nome, sobrenome e inicial(is) do autor. |
| `title` | Título do trabalho (capa e cabeçalho do Resumo). |
| `title-en` | Título no outro idioma (cabeçalho do Abstract). |
| `degree` | `Mestre`, `Doutor`, `Bacharel` ou `Licenciado`. |
| `program` | Programa de pós-graduação (ex.: `Ciência Política`). |
| `city`, `day`, `month`, `year` | Local e data. |
| `advisor` | Orientador: `title`, `first`, `last`, `institution`. |
| `co-advisor` | Coorientador (opcional, mesma estrutura). |
| `kw-pt-1`…`kw-pt-4` / `kw-en-1`…`kw-en-4` | Palavras-chave (4 slots por idioma; `""` para vazio). |
| `banca` | Lista de membros da banca (`name`, `institution`; máx. 6). |
| `dedicatoria`, `agradecimentos`, `epigrafe` | Elementos pré-textuais (texto livre). |
| `resumo`, `abstract` | Resumo (PT) e Abstract (EN). |
| `thesis-nature` | (Opcional) Texto da natureza do trabalho na folha de rosto. Se omitido, é gerado automaticamente. |
| `abreviaturas`, `simbolos`, `glossario`, `apendices`, `anexos` | Listas opcionais (veja `main.qmd`). |
| `bibliography` | Arquivo `.bib` (padrão: `bibliografia.bib`). |

### Citações

Use a sintaxe de citação do Pandoc, referenciando as chaves do `.bib`:

- `[@bib:Amado1991]` → citação entre parênteses: **(Amado, 1991)**
- `@bib:Andrade1997` → citação textual: **Andrade (1997)**
- `[@chaveA; @chaveB]` → múltiplas citações.

A lista de **Referências** é gerada automaticamente no fim do documento. Por isso
o `main.qmd` termina com:

```markdown
# Referências {.unnumbered}

::: {#refs}
:::
```

Mantenha esse bloco no final do seu documento.

### Figuras e tabelas

Use a sintaxe normal do Quarto:

```markdown
![Legenda da figura](caminho/imagem.png){#fig-exemplo}

Veja a @fig-exemplo.
```

## Versão em inglês

Para escrever a tese em inglês, use `main-en.qmd` como base. A diferença essencial
é a flag `lang-en: true` no YAML, que troca os rótulos estruturais para o inglês
(Contents, References, List of Tables…) e coloca o **Abstract antes do Resumo**.
O **Resumo em português continua presente**, pois é exigido pela ABNT mesmo em
trabalhos redigidos em inglês.

```sh
quarto render main-en.qmd
```

Por convenção de documento institucional brasileiro, a **ficha catalográfica** e a
**folha de aprovação** permanecem em português mesmo na versão em inglês.

## Limitações conhecidas

- A CSL ABNT pode exigir ajuste manual em casos de borda (subtítulos saem em
  negrito; obras sem autor cujo título serve de entrada). Veja
  [virgilinojuca/csl-abnt](https://github.com/virgilinojuca/csl-abnt).
- Entradas `.bib` que usam `\i` (i sem ponto) com acento — ex.: `cient{\'\i}fica`
  — podem falhar no pdflatex. Prefira UTF-8 pré-composto (`científica`).

## Créditos

- **Modelo LaTeX original (classe `repUERJ`)**: [Mateus Pestana](https://github.com/mateuspestana/modelo_latex_iespuerj).
- A classe `repUERJ` é derivada do trabalho do Prof. Luís Fernando de Oliveira.
- Estilo de citação ABNT 2023 (CSL): [virgilinojuca/csl-abnt](https://github.com/virgilinojuca/csl-abnt).
- Port para Quarto: este repositório.

## Licença

Veja [LICENSE](LICENSE).
