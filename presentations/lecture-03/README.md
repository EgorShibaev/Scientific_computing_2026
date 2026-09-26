# Lecture 3 presentation

[Open the PDF slide deck](lecture-03.pdf).

The 42-slide, 16:9 presentation follows Chapter 3 of the cumulative conspect.
It uses the same LaTeX Beamer layout, typography, colors, and native boxes as
Lecture 4. Blue boxes identify definitions, teal boxes state theorems, and
neutral boxes highlight key results. Short derivations and worked examples
remain outside the boxes.

| Slides | Conspect section |
| --- | --- |
| 2-5 | 3.1 Joint and marginal distributions |
| 6-11 | 3.2 Joint densities: probability over a region |
| 12-14 | 3.3 Correlation and nonlinear dependence |
| 15-17 | 3.4 Conditional means as prediction rules |
| 18-21 | 3.5 Random vectors and covariance matrices |
| 22-23 | 3.6 Linear transformations of random vectors |
| 24-33 | 3.7 The multivariate Gaussian |
| 34-36 | 3.8 What one Gaussian measurement tells us about another |
| 37-41 | 3.9 Gaussian class-conditional models |
| 42 | Summary of the chapter's operations |

The nine chart compositions use the chapter's analytic probability models:
ordered arrival times and their marginals, a conditional arrival density,
nonlinear dependence, Gaussian contours, Mahalanobis distance, the random-sign
counterexample, conditional Gaussian density, and the two-class sensor model.
All chart axes and curves are vector graphics. The PDF embeds Latin Modern
text and math fonts.

## Source and build

- `lecture-03.tex` contains slide text, formulas, tables, and boxes.
- `plots.tex` contains the TikZ/PGFPlots charts.

Install Tectonic, then run from the repository root:

```sh
make lecture-03-slides
```

The command compiles into `build/lecture-03-slides/` and copies the PDF here.
No Python packages, external images, or generated numerical data are required.
The conspect and the Lecture 4 presentation remain independent of this build.
