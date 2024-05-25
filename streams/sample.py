from typing import Counter
import numpy as np

"""
in a list of N, the probablity an element is selected if you select K is

1 - (N-1/N) * (N-2/N-1) ... (N-K/N-K+1)
= 1 - (N-K)/N
= K/N




x/N+1  = K/N

x = K(N+1)/N

k/(n+1)



P(replace) = k/(n)
p(not_replace) = (n-k)/(n)



1-(x) = k/n

(n-k)/n = x



"""


def random_int(logits: np.ndarray):
    logits = np.array(logits)
    k = logits.shape[0]
    probs = logits / logits.sum()
    return np.random.choice(range(k), p=probs)


def sample_simple(stream: list[int]):
    N = 0
    sample = None
    for e in stream:
        if sample is None:
            sample = e
        else:
            # extend P(replace) = N/(N+1)
            if np.random.random() > (N / (N + 1)):
                sample = e
        N += 1
    return sample


def sample_stream(stream: list[int], k: int) -> list[int]:
    samples = []
    counts = []
    N = 0
    for e in stream:
        N += 1
        if len(samples) < k:
            samples.append(e)
        else:
            p_replace = (N - k) / N
            idx = random_int([1 / N for _ in range(k)] + [p_replace])
            if idx < k:
                samples.pop(idx)
                samples.append(e)
    return samples


N_SAMPLES = 100_000
samples = []
for _ in range(N_SAMPLES):
    samples.extend(sample_stream(range(10), 3))
counts = Counter(samples)
print(counts)

# N_SAMPLES = 10000
# samples = []
# for _ in range(N_SAMPLES):
#     samples.extend(sample_stream(range(4), 1))
#
# counts = Counter(samples)
# print(counts)
