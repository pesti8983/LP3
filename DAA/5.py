# Analysis of Quick Sort: Deterministic vs Randomized variant
# Deterministic : pivot = last element
# Randomized    : pivot = random element (swapped to the end, then same partition)

import random
import sys
import time

sys.setrecursionlimit(20000)   # deterministic QS on sorted input recurses n deep

comparisons = 0   # step counter (element comparisons with pivot)


def partition(arr, low, high):
    global comparisons
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        comparisons += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def deterministic_quick_sort(arr, low, high):
    if low < high:
        p = partition(arr, low, high)
        deterministic_quick_sort(arr, low, p - 1)
        deterministic_quick_sort(arr, p + 1, high)


def randomized_partition(arr, low, high):
    r = random.randint(low, high)              # choose random pivot
    arr[r], arr[high] = arr[high], arr[r]
    return partition(arr, low, high)


def randomized_quick_sort(arr, low, high):
    if low < high:
        p = randomized_partition(arr, low, high)
        randomized_quick_sort(arr, low, p - 1)
        randomized_quick_sort(arr, p + 1, high)


def run(sort_fn, data):
    """Sort a copy of data; return (sorted list, comparisons, time in ms)."""
    global comparisons
    arr = data[:]
    comparisons = 0
    start = time.perf_counter()
    sort_fn(arr, 0, len(arr) - 1)
    elapsed = (time.perf_counter() - start) * 1000
    return arr, comparisons, elapsed


def main():
    # ---------- Part 1: sort a user-given array ----------
    raw = input("Enter numbers separated by spaces: ").split()
    data = [int(x) for x in raw]

    print("\nOriginal array :", data)
    d_arr, d_cmp, d_time = run(deterministic_quick_sort, data)
    r_arr, r_cmp, r_time = run(randomized_quick_sort, data)
    print("Deterministic  :", d_arr, f"| comparisons = {d_cmp} | time = {d_time:.4f} ms")
    print("Randomized     :", r_arr, f"| comparisons = {r_cmp} | time = {r_time:.4f} ms")

    # ---------- Part 2: analysis on different input types ----------
    n = 1000
    inputs = {
        "Random input": random.sample(range(n * 10), n),
        "Sorted input (worst case for deterministic)": list(range(n)),
        "Reverse sorted input": list(range(n, 0, -1)),
        "All equal elements": [7] * n,
    }

    print(f"\nAnalysis for n = {n}")
    print(f"{'Input type':<46}{'Variant':<15}{'Comparisons':>12}{'Time (ms)':>12}")
    print("-" * 85)
    for name, arr in inputs.items():
        for label, fn in (("Deterministic", deterministic_quick_sort),
                          ("Randomized", randomized_quick_sort)):
            _, c, t = run(fn, arr)
            print(f"{name:<46}{label:<15}{c:>12}{t:>12.3f}")
        print()

    print("""COMPLEXITY
-----------------------------------------------------------------
                 Best / Average     Worst        Space
Deterministic    O(n log n)         O(n^2)       O(log n) avg, O(n) worst (stack)
Randomized       O(n log n)         O(n^2)*      O(log n) expected (stack)
-----------------------------------------------------------------
* Randomized worst case still exists but is very unlikely for sorted or
  reverse sorted input, because it depends on random choices, not on the
  input order. Deterministic (last-element pivot) hits O(n^2) on sorted /
  reverse sorted input, which is common in practice.
  Note: with many duplicate keys, this partition (<= pivot) gives O(n^2)
  for BOTH variants (see 'All equal elements'). Randomization does not
  fix that; a 3-way partition does.""")


if __name__ == "__main__":
    main()