# Scientific Computing 2026

LaTeX source for a cumulative course conspect. The document begins with the
complete course structure and currently contains:

- Lecture 1: probability models, conditioning, Bayes' theorem, random variables,
  PMFs, PDFs, and CDFs.
- Lecture 2: expectation and variance; Exponential, Poisson, Gamma, Bernoulli,
  Binomial, Geometric, and Gaussian distributions; mixtures and heterogeneity;
  and a short extension on Student's t-distribution.
- Lecture 3: joint, marginal, and conditional distributions; correlation and
  nonlinear dependence; conditional means as prediction rules; random vectors and
  covariance matrices; multivariate Gaussians, linear transformations, and
  Gaussian class-conditional models.
- Lecture 4: samples and standard errors; Markov and Chebyshev inequalities;
  the law of large numbers and central limit theorem; dependence and heavy
  tails; Monte Carlo estimation and independent model evaluation.

Lecture 2 develops each distribution from a concrete experiment, with worked
examples, derivations, five original vector figures, and a distribution
reference table.

Lecture 3 builds on the shared-user and sensor examples from Lecture 2. It
uses the covariance and conditional-moment results already developed there,
without reintroducing them. It includes worked joint distributions, three
vector figures, and an example where
the relationship between two features carries all the class information.

The notes are cumulative: new chapters should reference earlier definitions
and derivations rather than repeat them, even when the programme lists a
topic again.

Lecture 4 follows one exponential-waiting example from sampling variability
to error bounds and Gaussian approximation. Seven original vector figures
distinguish exact distributions, bounds, approximations, and simulations.

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

Chapter 4's numerical plot data are committed, so a normal build needs no
Python packages. To reproduce them, including the fixed-seed simulations, run:

```bash
python3 scripts/generate_chapter4_figures.py
```

The generator uses only the Python standard library.

## Source layout

- `main.tex` assembles the cumulative course document.
- `preamble.tex` contains shared notation and formatting.
- `frontmatter/course-structure.tex` records the full course plan.
- `lectures/` contains one source file per lecture.
- `figures/` contains the LaTeX/PGFPlots source for the figures, rebuilt with the document.
- `figures/data/` contains reproducible numerical tables for Chapter 4.
- `scripts/` contains the generator for those tables.
- `dist/` contains the current compiled PDF.

The programme describes thirteen substantive lecture units but repeats the
label `Slot 7`. The manuscript normalizes the sequence to Lectures 1--13 while
preserving every listed unit.
