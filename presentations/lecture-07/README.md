# Lecture 7 presentation

[Open the PDF slide deck](lecture-07.pdf).

The 42-slide deck follows Chapter 7 of the cumulative conspect. It uses the
same 16:9 LaTeX Beamer format as the preceding lectures, with boxed
definitions and results, vector charts, and no footer text.

| Slides | Conspect section |
| --- | --- |
| 2–4 | 7.1 Surprise and entropy |
| 5–10 | 7.2 Cross-entropy and KL divergence |
| 11–15 | 7.3 Connections to learning |
| 16–30 | 7.4 Score, observed information, and Fisher information |
| 31–37 | 7.5 The Cramér–Rao lower bound |
| 38–40 | 7.6 MLE uncertainty from information |
| 41–42 | 7.7 A local connection between KL and Fisher information |

The first examples assume a binary population with success probability
0.8. Later, the probability becomes an unknown parameter to estimate.
Gaussian measurements with known variance provide a second running
example for sensitivity to a mean change, likelihood curvature, and
efficient estimation.
All logarithms are natural, with information measured in nats.

The information section begins with two possible Gaussian means at two noise
levels. Observed information describes the actual fitted log-likelihood's
curvature; Fisher information averages curvature across samples at a fixed
parameter. The squared-score expression then follows as an equivalent result.
The Gaussian example shows when observed and expected information coincide,
and the likelihood plot marks distances of 1/sqrt(information) from the peak.
A Bernoulli count example shows how observed curvature can vary while
Fisher information at the same candidate probability stays fixed.

The Cramér–Rao proof takes two slides: differentiating unbiasedness under
the joint sample density, then applying the covariance inequality.
The biased-estimator example remains self-contained, without a MAP comparison.

The ending states the MLE approximation without the score expansion or
convergence notation. Separate slides
calculate the estimated Bernoulli standard error and the confidence interval.
The KL connection uses one local formula and its Bernoulli plot.
The conspect retains the longer MLE and local-KL derivations, including
the Gaussian KL calculation, as well as variational inference and predictive
entropy. Those topics do not appear in the revised presentation.

## Build

From the repository root:

```sh
make lecture-07-slides
```

`lecture-07.tex` is the editable source. Shared charts are defined in
`figures/ch7-plots.tex`, with committed tables in `figures/data/ch7-*.dat`.
`plots.tex` adds the analytic Gaussian density comparison and the
likelihood plot with information and width annotations. Changes to these
slide-specific plots do not alter the conspect figures.
A normal build needs Tectonic but no Python packages. Regenerate the
tables and numerical checks with:

```sh
python3 scripts/generate_chapter7_figures.py
```

The variance experiment uses 30,000 independent Gaussian datasets at each
sample size, with seed 20261020. The other curves are analytic.

Mathematical background was checked against
[Deep Learning, Chapter 3](https://www.deeplearningbook.org/contents/prob.html)
and Stanford STATS 200 (2016),
[Lecture 14](https://web.stanford.edu/class/stats200/Lecture14.pdf) and
[Lecture 15](https://web.stanford.edu/class/stats200/Lecture15.pdf).
