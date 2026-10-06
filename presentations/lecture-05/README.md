# Lecture 5 presentation

[Open the PDF slide deck](lecture-05.pdf).

The 40-slide presentation follows Chapter 5 of the cumulative conspect in the
same 16:9 LaTeX Beamer format as Lectures 3 and 4. Definitions and key results
appear in colored boxes, with derivations and examples outside them.

| Slides | Conspect section |
| --- | --- |
| 2–4 | 5.1 Statistical models, estimators, and identifiability |
| 5–8 | 5.2 Method of moments, including a two-parameter Gamma fit |
| 9–14 | 5.3 Likelihood, exponential MLE, and parameter-dependent support |
| 15–16 | 5.4 Gaussian mean and variance estimation |
| 17–22 | 5.5 Bias, MSE, variance correction, and consistency |
| 23–28 | 5.6 Gaussian and Bernoulli likelihoods as training losses |
| 29–39 | 5.7 MAP, Beta and Gaussian priors, and quadratic regularization |
| 40 | Comparison of the three point-estimation rules |

Five shared vector charts show relative likelihoods, repeated-sample uniform
endpoint estimates, the Gaussian variance-loss terms, a Beta update, and a
Gaussian posterior. The curves and numerical examples match the conspect.
The uniform-estimator histogram uses 50,000 fixed-seed simulated datasets;
all other plotted curves are analytic.

## Source and build

From the repository root:

```sh
make lecture-05-slides
```

`lecture-05.tex` contains the editable slide source. The shared chart definitions
are in `figures/ch5-plots.tex`, and their committed numerical tables are in
`figures/data/ch5-*.dat`. A normal Tectonic build needs no Python packages.
To reproduce those tables using only the Python standard library:

```sh
python3 scripts/generate_chapter5_figures.py
```

The chapter leaves interval estimation and Fisher information to their planned
later lectures. The presentation introduces training objectives without assuming
the optimization or linear-algebra material from the second block.
