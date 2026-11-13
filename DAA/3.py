# Fractional Knapsack Problem using a Greedy Method
# Greedy choice: pick items in descending order of value/weight ratio.
# If the next item doesn't fit completely, take only the fraction that fits.


class Item:
    def __init__(self, index, value, weight):
        self.index = index
        self.value = value
        self.weight = weight
        self.ratio = value / weight


def fractional_knapsack(items, capacity):
    # Step 1: sort by value/weight ratio (highest first)  -> O(n log n)
    items = sorted(items, key=lambda it: it.ratio, reverse=True)

    total_value = 0.0
    remaining = capacity
    selection = []  # (item number, fraction taken, value gained)

    # Step 2: greedily fill the knapsack                  -> O(n)
    for it in items:
        if remaining == 0:
            break
        if it.weight <= remaining:           # take the whole item
            fraction = 1.0
        else:                                # take only the part that fits
            fraction = remaining / it.weight
        gain = it.value * fraction
        total_value += gain
        remaining -= it.weight * fraction
        selection.append((it.index, fraction, gain))

    return total_value, selection


def main():
    n = int(input("Enter number of items: "))
    if n <= 0:
        print("Number of items must be positive.")
        return

    items = []
    for i in range(1, n + 1):
        v = float(input(f"Item {i} - value  : "))
        w = float(input(f"Item {i} - weight : "))
        if w <= 0:
            print("Weight must be greater than 0.")
            return
        items.append(Item(i, v, w))

    capacity = float(input("Enter knapsack capacity: "))
    if capacity < 0:
        print("Capacity cannot be negative.")
        return

    total_value, selection = fractional_knapsack(items, capacity)

    print("\nItem | Fraction taken | Value gained")
    print("-" * 38)
    for idx, frac, gain in selection:
        print(f"{idx:>4} | {frac:>14.2f} | {gain:>12.2f}")

    print(f"\nMaximum value in knapsack = {total_value:.2f}")
    print("\nTime Complexity  : O(n log n)  (sorting dominates; selection loop is O(n))")
    print("Space Complexity : O(n)        (sorted copy of items / selection list)")


if __name__ == "__main__":
    main()