import time
from polygon import MaxTriangleCounter, NPolygon


def benchmark(fn, samples: int = 1) -> list[float]:
    times = []
    for _ in range(samples):
        t0 = time.time()
        fn()
        t1 = time.time()
        times.append(t1 - t0)
    return times


def benchmark_with_cache():
    N = 11
    SAMPLES = 1
    no_cache_counter = MaxTriangleCounter(NPolygon(N), False)
    cache_counter = MaxTriangleCounter(NPolygon(N), True)

    print(f"Running benchmark for {N} with {SAMPLES} samples")

    result1 = no_cache_counter.get_all_max_triangle_counts()
    result2 = cache_counter.get_all_max_triangle_counts()
    if result1 != result2:
        print("mismatch in result!")

    no_cache_times = benchmark(no_cache_counter.get_all_max_triangle_counts, SAMPLES)
    cache_times = benchmark(cache_counter.get_all_max_triangle_counts, SAMPLES)

    print(f"cached time: {sum(cache_times) / len(cache_times)}")
    print(f"No cached time: {sum(no_cache_times) / len(no_cache_times)}")


def MTC(n, include_cache=True):
    return MaxTriangleCounter(NPolygon(n), include_cache)
