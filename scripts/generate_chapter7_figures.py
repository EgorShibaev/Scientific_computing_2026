"""Reproduce the Chapter 7 analytic curves and Gaussian variance experiment.

All logarithms are natural. The script uses only the standard library.
The Gaussian simulation samples X_1 and the independent sum of the remaining
observations from their exact laws; this is equivalent to generating each row.
"""

from pathlib import Path
import math
import random
import statistics

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures/data"
SEED = 20261020


def entropy(p):
    return -sum(x * math.log(x) for x in p if x > 0)


def cross_entropy(p, q):
    if any(a > 0 and b == 0 for a, b in zip(p, q)):
        return math.inf
    return -sum(a * math.log(b) for a, b in zip(p, q) if a > 0)


def kl(p, q):
    if any(a > 0 and b == 0 for a, b in zip(p, q)):
        return math.inf
    return sum(a * math.log(a / b) for a, b in zip(p, q) if a > 0)


def table(name, names, rows):
    with (OUT / name).open("w", encoding="utf-8") as stream:
        stream.write(" ".join(names) + "\n")
        for row in rows:
            stream.write(" ".join(f"{x:.12g}" for x in row) + "\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    target = [0.8, 0.2]
    h = entropy(target)
    table("ch7-entropy.dat", ["p", "entropy"], [
        [i / 500, entropy([i / 500, 1 - i / 500])] for i in range(501)])
    grid = [0.02 + 0.002 * i for i in range(481)]
    table("ch7-cross-entropy.dat", ["q", "ce", "entropy", "kl"], [
        [q, cross_entropy(target, [q, 1 - q]), h, kl(target, [q, 1 - q])]
        for q in grid])
    table("ch7-fisher.dat", ["p", "information"], [
        [p, 1 / (p * (1 - p))] for p in grid])
    table("ch7-likelihood.dat", ["offset", "n5", "n20", "n80"], [
        [d, *[math.exp(-n * d * d / 8) for n in (5, 20, 80)]]
        for d in [-2 + i / 100 for i in range(401)]])
    table("ch7-local-kl.dat", ["q", "kl", "quadratic"], [
        [q, kl(target, [q, 1 - q]), (q - 0.8)**2 / (2 * 0.8 * 0.2)]
        for q in [0.65 + 0.0005 * i for i in range(601)]])

    rng = random.Random(SEED)
    repetitions = 30_000
    rows = []
    for n in (1, 2, 5, 10, 20, 50, 100, 200):
        firsts, means = [], []
        for _ in range(repetitions):
            first = rng.gauss(0, 2)
            rest = rng.gauss(0, 2 * math.sqrt(n - 1)) if n > 1 else 0
            firsts.append(first)
            means.append((first + rest) / n)
        variance_mean = statistics.variance(means)
        variance_first = statistics.variance(firsts)
        assert abs(variance_mean / (4 / n) - 1) < 0.05
        assert abs(variance_first / 4 - 1) < 0.05
        rows.append([n, 4 / n, variance_mean, 4, variance_first])
    table("ch7-variance.dat", ["n", "bound", "meanvariance", "firsttheory", "firstvariance"], rows)

    assert abs(h - 0.5004024235381879) < 1e-12
    assert abs(cross_entropy(target, [0.8, 0.2]) - h) < 1e-12
    assert abs(kl(target, [0.5, 0.5]) - (math.log(2) - h)) < 1e-12
    assert kl(target, [0.5, 0.5]) != kl([0.5, 0.5], target)
    assert kl(target, [1, 0]) == math.inf
    assert entropy([1, 0]) == 0
    for q in grid:
        ce = cross_entropy(target, [q, 1 - q])
        divergence = kl(target, [q, 1 - q])
        assert abs(ce - h - divergence) < 1e-12
        assert divergence >= -1e-12
    for q in (0.8 - 1e-5, 0.8 + 1e-5):
        ratio = kl(target, [q, 1 - q]) / ((q - 0.8)**2 / (2 * 0.8 * 0.2))
        assert abs(ratio - 1) < 1e-3
    for p in (0.02, 0.2, 0.5, 0.8, 0.98):
        score_success, score_failure = 1 / p, -1 / (1 - p)
        assert abs(p * score_success + (1 - p) * score_failure) < 1e-12
        score_second_moment = p * score_success**2 + (1 - p) * score_failure**2
        expected_negative_curvature = p / p**2 + (1 - p) / (1 - p)**2
        assert abs(score_second_moment - 1 / (p * (1 - p))) < 1e-11
        assert abs(expected_negative_curvature - score_second_moment) < 1e-11
    # Observed curvature varies with the count; its binomial average is Fisher.
    for n, p in ((10, 0.8), (20, 0.3)):
        weights = [math.comb(n, k) * p**k * (1-p)**(n-k)
                   for k in range(n + 1)]
        observed = [k / p**2 + (n-k) / (1-p)**2 for k in range(n + 1)]
        expected = sum(w * j for w, j in zip(weights, observed))
        assert abs(expected - n / (p * (1-p))) < 1e-10
    assert abs(7 / 0.8**2 + 3 / 0.2**2 - 85.9375) < 1e-12
    assert abs(9 / 0.8**2 + 1 / 0.2**2 - 39.0625) < 1e-12
    assert abs(math.exp(-0.5 * 100 * 0.1**2) - 0.6065306597) < 1e-10
    assert abs(math.exp(-0.5 * 4 * 0.1**2) - 0.9801986733) < 1e-10
    # A finite-state posterior checks the variational identity numerically.
    joint = [0.08, 0.12]
    evidence = sum(joint)
    posterior = [v / evidence for v in joint]
    candidate = [0.7, 0.3]
    objective = sum(q * (math.log(q) - math.log(j))
                    for q, j in zip(candidate, joint))
    assert abs(kl(candidate, posterior) - objective - math.log(evidence)) < 1e-12
    assert abs(0.8 - 1.96 / math.sqrt(625) - 0.7216) < 1e-12
    assert abs(0.8 + 1.96 / math.sqrt(625) - 0.8784) < 1e-12

    print("Binary entropy:", h)
    for q in (0.5, 0.6, 0.8, 0.99):
        print(f"q={q}: CE={cross_entropy(target, [q, 1-q]):.9f}; KL={kl(target, [q, 1-q]):.9f}")
    print("KL directions:", kl(target, [0.5, 0.5]), kl([0.5, 0.5], target))
    print("Teacher P=(.7,.2,.1), student Q=(.6,.25,.15):")
    print("  entropy, CE, KL:", entropy([.7,.2,.1]), cross_entropy([.7,.2,.1], [.6,.25,.15]), kl([.7,.2,.1], [.6,.25,.15]))
    print("Token NLL:", -sum(math.log(v) for v in (.5,.25,.1)) / 3)
    print(f"Gaussian variance experiment: {repetitions} datasets per n; seed={SEED}")
    print("Created six Chapter 7 data tables; all numerical checks passed.")


if __name__ == "__main__":
    main()
