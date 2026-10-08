import numpy as np
import time

print("Testing Monte Carlo simulation performance...")
t0 = time.time()

# Quick benchmark of 100,000 iterations
n_sims = 100000
# 36 group matches + 8 R16 + 4 QF + 2 SF + 1 Final = 51 matches per tournament
# 51 * 100,000 = 5,100,000 match decisions.
deltas = np.random.randn(51, n_sims)
probs = 1.0 / (1.0 + np.exp(-1.2 * deltas))
random_draws = np.random.rand(51, n_sims)
outcomes = random_draws < probs

t1 = time.time()
print(f"5.1M vectorized match evaluations took: {t1 - t0:.2f} seconds!")
