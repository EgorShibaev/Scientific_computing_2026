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
- Lecture 5: statistical models and estimators; method of moments; maximum
  likelihood; Gaussian estimation; bias, MSE, consistency, and the variance
  correction; likelihood-based training losses; MAP and regularization.
- Lecture 6: confidence-interval coverage and pivot inversion; Gaussian and
  Student mean intervals; an exact exponential-rate interval; proportion
  intervals; bootstrap standard errors and percentile intervals; paired model
  comparisons; and the assumptions and limits of resampling.
- Lecture 7: surprisal, entropy, cross-entropy, and KL divergence; connections
  to classification, language-model losses, distillation, and approximate
  posteriors; observed and Fisher information; the Cramér–Rao bound; MLE
  uncertainty; and the local quadratic relation between KL and information.

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

## Presentations

[Lecture 3 slides (PDF)](presentations/lecture-03/lecture-03.pdf) follow Chapter 3
in the same LaTeX Beamer format, with boxed definitions and results and vector
charts. The [presentation folder](presentations/lecture-03/) contains the PDF,
editable LaTeX source, and section mapping. Build with `make lecture-03-slides`.

[Lecture 4 slides (PDF)](presentations/lecture-04/lecture-04.pdf) follow Chapter 4
of the conspect. The separate [presentation folder](presentations/lecture-04/)
contains the LaTeX Beamer source and PDF, with typeset formulas and vector
charts based on the same data as the notes. Build with `make lecture-04-slides`.
The original PowerPoint version remains available in the same folder.

[Lecture 5 slides (PDF)](presentations/lecture-05/lecture-05.pdf) follow Chapter 5
in the same Beamer format. The [presentation folder](presentations/lecture-05/)
contains editable LaTeX source and the section mapping. Build with
`make lecture-05-slides`. Five shared vector figures keep the slides and
conspect aligned, including the distinction between normalized posterior
densities and relative likelihood curves.

[Lecture 6 slides (PDF)](presentations/lecture-06/lecture-06.pdf) follow Chapter 6
in the same LaTeX Beamer format. The [presentation folder](presentations/lecture-06/)
contains the editable source and section mapping. Build with
`make lecture-06-slides`. Five shared vector charts show repeated confidence
intervals, Gaussian and Student references, proportion-interval coverage,
bootstrap means, and paired accuracy differences.

[Lecture 7 slides (PDF)](presentations/lecture-07/lecture-07.pdf) follow Chapter 7
in the same LaTeX Beamer format, with boxed definitions and results and no
footer text. The [presentation folder](presentations/lecture-07/) contains
the editable source and section mapping. Build with `make lecture-07-slides`.
Six shared vector charts connect entropy, prediction loss, likelihood
curvature, and estimator variance through Bernoulli and Gaussian examples.

## Homework

[Homework 1](homework/homework-01/) contains eight coding problems with
theoretical derivations: four on Lectures 1 and 2, followed by four multivariate
problems from the seminar team. Only basic Python is assumed: runnable
mini-lessons introduce NumPy, plotting, and distribution functions as needed.
The student notebook includes guided function scaffolds, supplied experiment
templates, and per-task checks. Its folder contains the dependencies and
instructions for running it locally.

## Seminars and quizzes

The [seminar problem sheets](seminars/) accompany the probability block.
Seminar 1 has editable LaTeX source; rebuild it with `make seminar-01`.
The [short quizzes](output/pdf/) contain five questions each for a five-minute
check of Lectures 3--4 or Lecture 5.

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

Chapter 5's plot tables are also committed. Reproduce their analytic curves and
the fixed-seed uniform-estimator experiment with:

```bash
python3 scripts/generate_chapter5_figures.py
```

Chapter 6's numerical tables include fixed-seed resampling experiments and
exact binomial coverage calculations. Reproduce them using only the Python
standard library:

```bash
python3 scripts/generate_chapter6_figures.py
```

Chapter 7's tables contain analytic information-theory curves and a
fixed-seed Gaussian estimator experiment. Reproduce them using only the
Python standard library:

```bash
python3 scripts/generate_chapter7_figures.py
```

## Source layout

- `main.tex` assembles the cumulative course document.
- `preamble.tex` contains shared notation and formatting.
- `frontmatter/course-structure.tex` records the full course plan.
- `lectures/` contains one source file per lecture.
- `figures/` contains the LaTeX/PGFPlots source for the figures, rebuilt with the document.
- `figures/data/` contains reproducible numerical tables for Chapters 4--7.
- `scripts/` contains the generator for those tables.
- `dist/` contains the current compiled PDF.
