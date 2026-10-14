# Lecture 6 presentation

[Open the PDF slide deck](lecture-06.pdf).

The 42-slide presentation follows Chapter 6 of the cumulative conspect in the
same 16:9 LaTeX Beamer format as Lectures 3–5. Definitions and key results
appear in colored boxes. Mathematical derivations and worked examples remain
outside those boxes.

| Slides | Conspect section |
| --- | --- |
| 2–4 | 6.1 What uncertainty remains after fitting |
| 5–10 | 6.2 Confidence intervals and repeated sampling |
| 11–18 | 6.3 Mean intervals with unknown variance |
| 19–23 | 6.4 Proportion intervals and test accuracy |
| 24–31 | 6.5 Bootstrap and the empirical distribution |
| 32–36 | 6.6 Comparing two models on the same examples |
| 37–42 | 6.7 What resampling can and cannot recover |

The exponential example returns to the five waiting times from Chapter 5 and
closes with an exact rate interval. Mean intervals distinguish the exact
Gaussian result from an asymptotic approximation and from prediction for a
future observation. Proportion intervals compare Wald and Wilson coverage.
Bootstrap examples cover empirical resampling, standard errors, percentile
and basic intervals, and paired classifier comparisons.

Five shared vector charts show repeated-sample coverage, Gaussian and Student
densities, exact binomial coverage calculations, bootstrap means, and paired
bootstrap accuracy differences. The charts use the same definitions and data
as the conspect.

## Source and build

From the repository root:

```sh
make lecture-06-slides
```

`lecture-06.tex` contains the editable slide source. Shared chart definitions
are in `figures/ch6-plots.tex`, and their committed numerical tables are in
`figures/data/ch6-*.dat`. A normal Tectonic build needs no Python packages.
The figure-generation script reproduces the data and records the numerical
details of the simulated examples.

The chapter distinguishes uncertainty in evaluating fixed fitted models from
variation caused by refitting models on new training samples. It also explains
limits caused by dependence, rare outcomes, sample selection, and the ordinary
bootstrap for a uniform endpoint.
