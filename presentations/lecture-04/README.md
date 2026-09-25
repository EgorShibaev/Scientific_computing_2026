# Lecture 4 presentation

[Open the slide deck](lecture-04.pptx).

The 35-slide, 16:9 presentation follows Chapter 4 of the cumulative conspect.
It retains the worked examples, theorem assumptions, and short proofs.
The deck contains editable text and formulas, two editable tables, and eleven
native charts representing all seven figure concepts in the chapter.

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
The deck uses Arial for prose and STIX Two Math for editable mathematical text.

## Source

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

The conspect and its normal `make` build are independent of this presentation.
