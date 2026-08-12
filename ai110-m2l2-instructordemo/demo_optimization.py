import random
import timeit

# Generate sample data
large_list = [random.randint(0, 100000) for _ in range(10000)]
queries = [random.randint(0, 100000) for _ in range(1000)]

# Pre-convert list to a set for fast O(1) lookups
large_set = set(large_list)


# O(N) list lookup per query -> O(M * N) overall
def slow_lookup():
    found = []
    for q in queries:
        if q in large_list:
            found.append(q)
    return found


# O(1) set lookup per query -> O(M + N) overall
def fast_lookup():
    return [q for q in queries if q in large_set]


# Run benchmark
iterations = 10

slow_time = timeit.timeit(slow_lookup, number=iterations)
fast_time = timeit.timeit(fast_lookup, number=iterations)

print(f"Slow lookup average time: {slow_time / iterations:.6f} seconds")
print(f"Fast lookup average time: {fast_time / iterations:.6f} seconds")
print(f"Speedup: {slow_time / fast_time:.2f}x faster")
