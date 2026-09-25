# Lecture 4 presentation

[Open the PDF slide deck](lecture-04.pdf).

The 35-slide, 16:9 presentation follows Chapter 4 of the cumulative conspect.
It retains the worked examples, theorem assumptions, and short proofs.
The PDF uses LaTeX Beamer for proper mathematical typesetting: fractions,
summations, radicals, subscripts, and mathematical operators. The eleven
vector charts represent all seven figure concepts in the chapter.
Blue Beamer blocks identify definitions, teal blocks state theorems, and
neutral blocks highlight key results. Proofs and worked examples remain outside
these blocks.

| Slides | Conspect section |
| --- | --- |
| 2–6 | 4.1 Samples and standard errors |
| 7–11 | 4.2 Markov and Chebyshev inequalities |
| 12–14 | 4.3 Law of large numbers |
| 15–23 | 4.4 Central limit theorem |
| 24–28 | 4.5 The limits of averaging |
| 29–35 | 4.6 Monte Carlo and averages in machine learning |

The chart data come directly from `../../figures/data/ch4-*.dat`.
The four CLT panels span two slides to keep their axes readable.
The PDF uses embedded Latin Modern text and math fonts.

## LaTeX source and PDF build

- `lecture-04.tex` contains the slides and formulas.
- `plots.tex` contains the PGFPlots charts and LaTeX axis labels.

Install Tectonic, then run from the repository root:

```sh
make lecture-04-slides
```

This compiles into `build/lecture-04-slides/` and copies the PDF here.
The conspect and its normal `make` build remain independent of the presentation.

## Original PowerPoint version

The [original PowerPoint deck](lecture-04.pptx) is retained separately.
Its text, tables, and charts remain editable, but its formulas use Unicode
text rather than the LaTeX typesetting in the PDF. The files below rebuild
that earlier PowerPoint version, not the PDF:

- `build.mjs` contains the slide content, layouts, and native chart definitions.
- `set-chart-log-axes.py` sets explicit native logarithmic axes and chart
  rendering details without changing the numerical series.

The builder requires Node.js and the `@oai/artifact-tool` presentation runtime.
It can resolve the package normally, or use an absolute ES-module entry point
in `ARTIFACT_TOOL_MODULE`. Python 3 is sufficient for the chart postprocessor.
No Python plotting libraries are required.

From the repository root:

```sh
node presentations/lecture-04/build.mjs
python3 presentations/lecture-04/set-chart-log-axes.py \
  tmp/lecture-04-slides/build/candidate.pptx \
  tmp/lecture-04-slides/build/candidate-log.pptx \
  tmp/lecture-04-slides/build/log-axes.json
```

These commands write drafts into the ignored `tmp/` directory. The published
deck also includes embedded chart-data workbooks, added during presentation
finalization. Review a rebuilt draft before replacing the published deck.
