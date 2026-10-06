"""Reproduce Chapter 5 plot tables using only the Python standard library.

All curves are analytic except the explicitly labeled uniform-estimator
histograms. The fixed seed makes that repeated-sampling illustration reproducible.
"""
from pathlib import Path
import math
import random

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures/data"


def table(name, header, rows):
    with (OUT / name).open("w", encoding="utf-8") as stream:
        stream.write(" ".join(header) + "\n")
        for row in rows:
            stream.write(" ".join(f"{value:.12g}" for value in row) + "\n")


def normal(x, mean, variance):
    return math.exp(-(x - mean)**2 / (2 * variance)) / math.sqrt(2 * math.pi * variance)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rate_grid = sorted(set([0.01 + i * 0.004 for i in range(299)] + [1 / 3]))
    table("ch5-likelihood.dat", ["rate", "n5", "n50"], [
        [rate, math.exp(5 * (math.log(rate / (1/3)) - 3 * (rate - 1/3))),
         math.exp(50 * (math.log(rate / (1/3)) - 3 * (rate - 1/3)))]
        for rate in rate_grid])

    rng = random.Random(20261005)
    repetitions, n, bins = 50_000, 5, 80
    width = 2 / bins
    counts_mm, counts_ml = [0] * bins, [0] * bins
    total_mm = total_ml = error_mm = error_ml = 0.0
    for _ in range(repetitions):
        sample = [rng.random() for _ in range(n)]
        mm, ml = 2 * sum(sample) / n, max(sample)
        counts_mm[min(bins - 1, int(mm / width))] += 1
        counts_ml[min(bins - 1, int(ml / width))] += 1
        total_mm += mm
        total_ml += ml
        error_mm += (mm - 1)**2
        error_ml += (ml - 1)**2
    assert abs(total_mm / repetitions - 1) < 0.005
    assert abs(total_ml / repetitions - 5/6) < 0.005
    assert abs(error_mm / repetitions - 1/15) < 0.002
    assert abs(error_ml / repetitions - 1/21) < 0.002
    assert sum(counts_mm) == sum(counts_ml) == repetitions
    histogram_rows = [[i*width, counts_mm[i]/(repetitions*width), counts_ml[i]/(repetitions*width)]
                      for i in range(bins)]
    histogram_rows.append([2, 0, 0])
    table("ch5-uniform-estimates.dat", ["endpoint", "moments", "mle"], histogram_rows)

    sigmas = sorted(set([0.5 + i * 0.025 for i in range(221)] + [2.0]))
    table("ch5-variance-loss.dat", ["sigma", "scaled_residual", "log_scale", "total"], [
        [s, 2/s**2, math.log(s), 2/s**2 + math.log(s)] for s in sigmas])
    beta_constant = math.factorial(13) / (math.factorial(8) * math.factorial(4))
    assert beta_constant == 6435
    table("ch5-beta.dat", ["p", "prior", "posterior"], [
        [i/500, 6*(i/500)*(1-i/500), beta_constant*(i/500)**8*(1-i/500)**4]
        for i in range(501)])
    table("ch5-gaussian-prior.dat", ["mu", "prior", "likelihood", "posterior"], [
        [x, normal(x, 0, 1), normal(x, 1.6, 1), normal(x, 0.8, 0.5)]
        for x in [-3 + 0.02*i for i in range(401)]])
    print(f"Uniform estimator simulation, {repetitions} datasets of size {n}:")
    print(f"  means: MoM={total_mm/repetitions:.6f}, MLE={total_ml/repetitions:.6f}")
    print(f"  MSEs: MoM={error_mm/repetitions:.6f}, MLE={error_ml/repetitions:.6f}")
    print("Created five plot tables; numerical checks passed.")


if __name__ == "__main__":
    main()
