"""Reproduce Chapter 6 scientific plot tables with the Python standard library.

The repeated-interval and nonparametric-bootstrap illustrations use fixed seeds.
The normal/t densities and binomial coverage curves are computed analytically.
The paired bootstrap resamples whole paired accuracy differences, never the two
classifiers independently. Committed tables keep PDF builds dependency-free.
"""
from pathlib import Path
import math
import random
import statistics

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures/data"
SEED = 20261011
Z975 = 1.959963984540054
T9_975 = 2.2621571628540993


def table(name, header, rows):
    with (OUT / name).open("w", encoding="utf-8") as stream:
        stream.write(" ".join(header) + "\n")
        for row in rows:
            stream.write(" ".join(f"{value:.12g}" for value in row) + "\n")


def quantile(sorted_values, probability):
    """Linear interpolation, identical to the usual default sample quantile."""
    location = probability * (len(sorted_values) - 1)
    lower = int(location)
    fraction = location - lower
    return (1 - fraction) * sorted_values[lower] + fraction * sorted_values[min(lower + 1, len(sorted_values) - 1)]


def histogram(name, values, width, first=None, last=None):
    first = math.floor(min(values) / width) * width if first is None else first
    last = math.ceil(max(values) / width) * width if last is None else last
    bins = int(round((last - first) / width))
    counts = [0] * bins
    for value in values:
        index = min(bins - 1, max(0, int((value - first) / width)))
        counts[index] += 1
    assert sum(counts) == len(values)
    rows = [[first + index * width, count / (len(values) * width)]
            for index, count in enumerate(counts)]
    rows.append([last, 0])
    table(name, ["value", "density"], rows)


def proportion_intervals(k, n):
    estimate = k / n
    wald_half = Z975 * math.sqrt(estimate * (1 - estimate) / n)
    denominator = 1 + Z975**2 / n
    center = (estimate + Z975**2 / (2 * n)) / denominator
    half = Z975 / denominator * math.sqrt(estimate * (1 - estimate) / n + Z975**2 / (4 * n**2))
    return (estimate - wald_half, estimate + wald_half), (max(0, center - half), min(1, center + half))


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # A 95% procedure does not promise that exactly 95% of 40 intervals cover.
    rng = random.Random(SEED + 2)
    true_mean, sigma, n, repetitions = 10.0, 2.0, 25, 40
    half_width = Z975 * sigma / math.sqrt(n)
    hits, misses = [], []
    for trial in range(1, repetitions + 1):
        mean = statistics.mean(rng.gauss(true_mean, sigma) for _ in range(n))
        row = [trial, mean, half_width, mean - half_width, mean + half_width]
        (hits if abs(mean - true_mean) <= half_width else misses).append(row)
    table("ch6-coverage-hit.dat", ["trial", "mean", "halfwidth", "lower", "upper"], hits)
    table("ch6-coverage-miss.dat", ["trial", "mean", "halfwidth", "lower", "upper"], misses)

    # Student's t: the extra uncertainty from estimating sigma makes heavier tails.
    nu = 9
    t_constant = math.gamma((nu + 1) / 2) / (math.sqrt(nu * math.pi) * math.gamma(nu / 2))
    density_grid = sorted(set([-4 + i / 100 for i in range(801)] + [-T9_975, T9_975]))
    table("ch6-student.dat", ["x", "normal", "t9", "lefttail", "righttail"], [
        [x, math.exp(-x*x / 2) / math.sqrt(2 * math.pi),
         t_constant * (1 + x*x / nu)**(-(nu + 1) / 2),
         t_constant * (1 + x*x / nu)**(-(nu + 1) / 2) if x <= -T9_975 else 0,
         t_constant * (1 + x*x / nu)**(-(nu + 1) / 2) if x >= T9_975 else 0]
        for x in density_grid])

    # Exact binomial coverage: sum the probabilities of the counts whose
    # interval contains p. A dense grid reveals real discrete oscillations.
    count_n = 20
    intervals = [proportion_intervals(k, count_n) for k in range(count_n + 1)]
    coverage_rows = []
    for i in range(1001):
        p = i / 1000
        coverage = [0.0, 0.0]
        for k, bounds in enumerate(intervals):
            mass = math.comb(count_n, k) * p**k * (1-p)**(count_n-k)
            for method, (lower, upper) in enumerate(bounds):
                if lower - 1e-12 <= p <= upper + 1e-12:
                    coverage[method] += mass
        coverage_rows.append([p, *coverage])
    table("ch6-proportion-coverage.dat", ["p", "wald", "wilson"], coverage_rows)

    # One observed sample, resampled with replacement: this is conditional on
    # that sample. We plot the bootstrap distribution alone to avoid confusing
    # it with the true sampling distribution under the exponential population.
    rng = random.Random(SEED)
    sample_n, bootstrap_repetitions = 40, 20_000
    sample = [rng.expovariate(1 / 5) for _ in range(sample_n)]
    original_mean = statistics.mean(sample)
    bootstrap_means = sorted(statistics.mean(rng.choices(sample, k=sample_n))
                             for _ in range(bootstrap_repetitions))
    bootstrap_se = statistics.stdev(bootstrap_means)
    bootstrap_lower, bootstrap_upper = [quantile(bootstrap_means, q) for q in (0.025, 0.975)]
    histogram("ch6-bootstrap-mean.dat", bootstrap_means, 0.1)
    table("ch6-bootstrap-sample.dat", ["index", "waitingtime"], enumerate(sample, start=1))

    # Two fixed classifiers evaluated on the SAME 200 test examples:
    # both correct=150, A only=30, B only=10, both wrong=10.
    # A has accuracy 180/200, B 160/200; the estimand is their paired difference.
    rng = random.Random(SEED + 1)
    paired_n = 200
    differences = [1] * 30 + [-1] * 10 + [0] * 160
    paired_mean = statistics.mean(differences)
    paired_replicates = sorted(sum(rng.choices(differences, k=paired_n)) / paired_n
                               for _ in range(bootstrap_repetitions))
    paired_se = statistics.stdev(paired_replicates)
    paired_lower, paired_upper = [quantile(paired_replicates, q) for q in (0.025, 0.975)]
    # Discrete probability masses, rather than a continuous density: possible
    # accuracy differences are spaced by 1/200 = 0.005.
    paired_counts = {}
    for value in paired_replicates:
        paired_counts[value] = paired_counts.get(value, 0) + 1
    table("ch6-paired-accuracy.dat", ["difference", "mass"], [
        [value, paired_counts[value] / bootstrap_repetitions] for value in sorted(paired_counts)])

    assert len(hits) + len(misses) == repetitions
    assert abs(statistics.mean(bootstrap_means) - original_mean) < 0.02
    assert abs(bootstrap_se - statistics.stdev(sample) * math.sqrt((sample_n-1) / sample_n**2)) < 0.02
    assert abs(statistics.mean(paired_replicates) - paired_mean) < 0.002
    assert abs(paired_se - math.sqrt((0.2 - 0.1**2) / paired_n)) < 0.002
    assert paired_lower > 0
    assert all(0 <= row[1] <= 1 + 1e-12 and 0 <= row[2] <= 1 + 1e-12 for row in coverage_rows)

    table("ch6-summary.dat", ["coveragehits", "coveragetrials", "samplemean", "samplesd",
                              "bootstrapse", "bootstraplower", "bootstrapupper", "pairedmean",
                              "pairedse", "pairedlower", "pairedupper"], [[
        len(hits), repetitions, original_mean, statistics.stdev(sample), bootstrap_se,
        bootstrap_lower, bootstrap_upper, paired_mean, paired_se, paired_lower, paired_upper]])
    print(f"Known-sigma Gaussian intervals, seed={SEED+2}: {len(hits)}/{repetitions} cover mu=10 ({len(hits)/repetitions:.1%}).")
    print(f"Exponential sample n={sample_n}, population mean=5, seed={SEED}:")
    print(f"  observed mean={original_mean:.9f}, sample SD={statistics.stdev(sample):.9f}")
    print(f"  bootstrap B={bootstrap_repetitions}, SE={bootstrap_se:.9f}, percentile CI=[{bootstrap_lower:.9f}, {bootstrap_upper:.9f}]")
    print(f"Paired accuracies A=0.90, B=0.80, n={paired_n}, seed={SEED+1}:")
    print(f"  bootstrap SE={paired_se:.9f}, percentile CI=[{paired_lower:.9f}, {paired_upper:.9f}]")
    print("Exact binomial coverage at p=.05:", coverage_rows[50][1:])
    print("Created Chapter 6 plot tables; numerical checks passed.")


if __name__ == "__main__":
    main()
