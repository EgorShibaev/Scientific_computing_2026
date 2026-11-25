# Lecture 6 presentation

[Open the PDF slide deck](lecture-06.pdf).

The 37-slide presentation follows Chapter 6 of the cumulative conspect in the
same 16:9 LaTeX Beamer format as Lectures 3–5. Definitions and key results
appear in colored boxes. Mathematical derivations and worked examples remain
outside those boxes.

| Slides | Conspect section |
| --- | --- |
| 2–4 | 6.1 What uncertainty remains after fitting |
| 5–10 | 6.2 Confidence intervals and repeated sampling |
| 11–17 | 6.3 Mean intervals with unknown variance |
| 18–21 | 6.4 Proportion intervals and test accuracy |
| 22–30 | 6.5 Bootstrap and the empirical distribution |
| 31–35 | 6.6 Comparing two models on the same examples |
| 36–37 | 6.5 Bootstrap: observations versus resamples |

The chi-square definition is connected to Gamma sums before it is used for
sample variance and the exponential-rate pivot. The sample-variance result
includes an explicit two-observation example; the longer general proof is
stated without deriving the Gaussian coordinate rotation. The deck retains
the exponential-rate pivot and the exact versus asymptotic mean intervals.
The separate numerical mean and rate examples and the prediction-interval
comparison remain in the conspect rather than in the slides.

Bootstrap notation starts with a resample mean, followed by its standard
error and interval calculations. Percentile and basic intervals use the same
40-observation example, with a separate comparison of their endpoints.
The paired-classifier example derives both the mean difference and its
standard error. The deck has no gray takeaway text or footer labels.

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

The two final slides distinguish the number of bootstrap repetitions from
the number of independent observations. A fixed five-observation example
shows that increasing B estimates a nonzero bootstrap spread more precisely.
A second table shows the decrease in standard error with n when the
population variance is held fixed. The more technical bootstrap limitations
and the discussion of training uncertainty, other metrics, and sampling bias
remain in the conspect.
