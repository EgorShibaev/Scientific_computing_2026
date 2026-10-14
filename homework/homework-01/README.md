# Homework 1: probability through simulation

[Open the student notebook](homework-01.ipynb).

Eight problems, each combining a mathematical derivation with a reproducible
coding experiment. Part I covers Lectures 1 and 2:

1. Inverse-CDF sampling and empirical distribution comparisons.
2. Bayesian inference in a Bernoulli-Binomial-Gaussian chain.
3. Exponential gaps, Poisson counts, and Gamma arrival times.
4. Shared calibration offsets versus independently selected sensors.

Part II adds the seminar team's multivariate problems:

5. Equal pairwise correlations, valid covariance matrices, and singular endpoints.
6. Distances and angles in high dimensions.
7. Accumulated Gaussian noise and dependence along a random walk.
8. Random neuron weights, variance scaling, and correlated outputs.

Part II assumes the course's multivariate material and basic matrix algebra
(including eigenvalues). It includes a matrix/array mini-lab and a supplied
Gaussian sampler that supports singular positive-semidefinite covariances.

Only basic Python is assumed: variables, lists, conditions, loops, and functions.
No prior NumPy, pandas, SciPy, or Matplotlib knowledge is needed. The notebook
introduces arrays, masks, seeds, histograms, distribution functions, and array
axes through short runnable examples, with additional guidance before each task.
Pandas only displays tables; students do not need to learn data-frame operations.

The starter contains the complete questions, guided function scaffolds, answer
cells, ready-made experiment/plot templates, and per-task implementation checks.
Ordinary Python loops are accepted. Tutorial outputs are included, but there
are no completed homework implementations or solution outputs. The unfinished
functions raise `NotImplementedError` if called; a successful starter run does
not mean the problems have been solved.

## Run locally

Use Python 3.11 or newer. From the repository root:

```sh
python -m venv .venv-homework
source .venv-homework/bin/activate
python -m pip install -r homework/homework-01/requirements.txt
python -m jupyterlab homework/homework-01/homework-01.ipynb
```

On Windows, activate with `.venv-homework\Scripts\activate` instead.
Run cells with **Shift+Enter**, from top to bottom. Start with the short toolkit
examples and change their values to see what happens.

For each task:

1. Write the derivation and complete its function scaffolds, replacing the
   `NotImplementedError` lines.
2. Enable just that task in the setup cell, for example `RUN_TASKS[1] = True`.
   Leave the other entries `False` until they are ready.
3. Keep `QUICK_RUN = True` for small debugging experiments, then run the
   supplied plots and checks. Checks use their own fixed test sample sizes.
4. Interpret the results and complete the remaining tasks.

Before submitting, set all eight `RUN_TASKS` entries to `True` and
`QUICK_RUN = False`. Restart the kernel and run all cells. Submit the completed
notebook with derivations, code, full-size outputs, and interpretations.

## Fresh-kernel validation

The validation script uses the Python environment from which it is launched.
It creates a temporary kernel specification without changing registered kernels:

```sh
python scripts/check_homework_notebooks.py homework/homework-01/homework-01.ipynb
```

By default this does not modify the notebook. Add `--write` to save executed
outputs. It executes arbitrary notebook code, so use it only on trusted files.

Dependencies are listed in `requirements.txt`. No external dataset, network
access, credentials, or local data files are needed by the notebook itself.
