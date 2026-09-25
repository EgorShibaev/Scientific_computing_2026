#!/usr/bin/env python3
"""Reproduce Chapter 4 figure data using only Python's standard library.

Run from any directory: python3 scripts/generate_chapter4_figures.py
The script writes only figures/data/ch4-*.dat. All simulation seeds, repeat
counts, and analytic formulas are specified below; no runs are selected after
looking at the output. PGFPlots renders the tables as vector graphics.
"""

from __future__ import annotations

import math
from pathlib import Path
import random


OUTPUT = Path(__file__).resolve().parents[1] / "figures" / "data"
PATH_SEEDS = (104729, 130363, 155921)
MC_SEED = 20260925
MC_REPEATS = 2000
MC_SIZES = (10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10000)
MC_MEAN = 1 / 6
MC_VARIANCE = 1 / 11 - 1 / 36  # 25/396: E[exp(-2T)] - E[exp(-T)]^2.


def table(name: str, header: str, rows: list[tuple[float, ...]]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / name).open("w", encoding="ascii") as handle:
        handle.write(header + "\n")
        for row in rows:
            handle.write(" ".join(f"{value:.12g}" for value in row) + "\n")


def gamma_density(x: float, shape: int, rate: float) -> float:
    if x < 0:
        return 0.0
    if x == 0:
        return rate if shape == 1 else 0.0
    return math.exp(shape * math.log(rate) + (shape - 1) * math.log(x)
                    - rate * x - math.lgamma(shape))


def gamma_survival(shape: int, argument: float) -> float:
    """P(Gamma(shape, rate=1) > argument), using a finite Poisson sum."""
    return math.fsum(math.exp(-argument + k * math.log(argument)
                             - math.lgamma(k + 1)) for k in range(shape))


def gamma_cdf(shape: int, argument: float) -> float:
    """Compute the complementary Poisson tail directly, without cancellation."""
    term = math.exp(-argument + shape * math.log(argument)
                    - math.lgamma(shape + 1))
    terms = [term]
    k = shape
    while True:
        k += 1
        term *= argument / k
        terms.append(term)
        if k > argument and term < 1e-16 * math.fsum(terms):
            return math.fsum(terms)


def exponential_mean_error(n: int) -> float:
    # bar(T) ~ Gamma(shape=n, rate=n/5), hence the unit-rate arguments below.
    return gamma_cdf(n, 0.8 * n) + gamma_survival(n, 1.2 * n)


def make_tables() -> None:
    table("ch4-sampling-density.dat", "x n1 n4 n25", [
        (i / 25, *(gamma_density(i / 25, n, n / 5) for n in (1, 4, 25)))
        for i in range(401)
    ])

    paths = []
    for seed in PATH_SEEDS:
        rng = random.Random(seed)
        total = 0.0
        path = []
        for n in range(1, 1001):
            total += rng.expovariate(0.2)
            path.append(total / n)
        paths.append(path)
    table("ch4-running-means.dat", "n path1 path2 path3", [
        (n, *(path[n - 1] for path in paths)) for n in range(1, 1001)
    ])

    for n in (1, 4, 25, 100):
        # A common z-grid includes the visible support boundaries -1 and -2.
        rows = []
        for i in range(451):
            z = -4 + i / 50
            exact = math.sqrt(n) * gamma_density(n + math.sqrt(n) * z, n, 1)
            normal = math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
            rows.append((z, exact, normal))
        table(f"ch4-clt-n{n}.dat", "z exact normal", rows)

    table("ch4-tail-comparison.dat", "n exact chebyshev clt", [
        (n, exponential_mean_error(n), min(1, 25 / n),
         math.erfc(math.sqrt(n) / (5 * math.sqrt(2))))
        for n in range(1, 201)
    ])

    table("ch4-dependent-averages.dat", "n independent dependent", [
        (n, 1 / math.sqrt(n), math.sqrt(0.1 + 0.9 / n))
        for n in range(1, 1001)
    ])

    table("ch4-heavy-tail-means.dat", "x n1 n4 n25 cauchy", [
        (i / 100, *(math.sqrt(n / (2 * math.pi)) * math.exp(-n * (i / 100) ** 2 / 2)
                    for n in (1, 4, 25)), 1 / (math.pi * (1 + (i / 100) ** 2)))
        for i in range(-400, 401)
    ])

    # Independent replicates; each replicate reuses its prefix across n values.
    # Thus each RMSE is based on MC_REPEATS independent estimates, while the
    # plotted RMSE values for different n are intentionally correlated.
    rng = random.Random(MC_SEED)
    squared_errors = {n: [] for n in MC_SIZES}
    for _ in range(MC_REPEATS):
        total = 0.0
        for n in range(1, max(MC_SIZES) + 1):
            total += math.exp(-rng.expovariate(0.2))
            if n in squared_errors:
                squared_errors[n].append((total / n - MC_MEAN) ** 2)
    table("ch4-monte-carlo-error.dat", "n theory simulated", [
        (n, math.sqrt(MC_VARIANCE / n),
         math.sqrt(math.fsum(squared_errors[n]) / MC_REPEATS)) for n in MC_SIZES
    ])

    # Checks cover the exact-tail implementation and all visible densities.
    for n in (1, 4, 25, 100, 200):
        for argument in (0.8 * n, 1.2 * n):
            assert abs(gamma_cdf(n, argument) + gamma_survival(n, argument) - 1) < 1e-12
    assert abs(MC_VARIANCE - 25 / 396) < 1e-15
    assert abs(exponential_mean_error(1) - (1 - math.exp(-0.8) + math.exp(-1.2))) < 1e-14
    print(f"Exact P(|bar(T)-5|>1), n=100: {exponential_mean_error(100):.12f}")
    print(f"CLT approximation, n=100: {math.erfc(math.sqrt(2)):.12f}")
    print(f"MC E[exp(-T)]: {MC_MEAN:.12f}; variance: {MC_VARIANCE:.12f} = 25/396")
    print(f"Running-mean seeds: {PATH_SEEDS}; maximum plotted value: {max(map(max, paths)):.4f}")
    print(f"MC seed: {MC_SEED}; independent repetitions: {MC_REPEATS}")


if __name__ == "__main__":
    make_tables()
