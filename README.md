# Scientific Computing 2026

LaTeX source for a cumulative course conspect. The document begins with the
complete course structure and currently contains Lecture 1: probability models,
conditioning, Bayes' theorem, random variables, PMFs, PDFs, and CDFs.

## Build

The repository uses [Tectonic](https://tectonic-typesetting.github.io/), which
handles the required LaTeX reruns automatically.

```bash
make
```

The compiled course PDF is written to:

```text
dist/scientific_computing_2026.pdf
```

## Source layout

- `main.tex` assembles the cumulative course document.
- `preamble.tex` contains shared notation and formatting.
- `frontmatter/course-structure.tex` records the full course plan.
- `lectures/` contains one source file per lecture.
- `dist/` contains the current compiled PDF.

The programme describes thirteen substantive lecture units but repeats the
label `Slot 7`. The manuscript normalizes the sequence to Lectures 1--13 while
preserving every listed unit.
