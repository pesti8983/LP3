# Huffman Encoding using a Greedy Strategy
# Greedy choice: always merge the two nodes with the smallest frequencies.

import heapq
from collections import Counter


class Node:
    def __init__(self, ch, freq, left=None, right=None):
        self.ch = ch          # character (None for internal nodes)
        self.freq = freq      # frequency
        self.left = left
        self.right = right


def build_huffman_tree(freq_map):
    """Build the Huffman tree using a min-heap (priority queue)."""
    heap = []
    order = 0  # tie-breaker so heap never compares Node objects
    for ch, f in freq_map.items():
        heapq.heappush(heap, (f, order, Node(ch, f)))
        order += 1

    # Greedy step: repeatedly take two smallest nodes and merge them
    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)
        merged = Node(None, f1 + f2, left, right)
        heapq.heappush(heap, (merged.freq, order, merged))
        order += 1

    return heap[0][2]


def generate_codes(node, code="", codes=None):
    """Traverse the tree: left edge = '0', right edge = '1'."""
    if codes is None:
        codes = {}
    if node is None:
        return codes
    if node.left is None and node.right is None:   # leaf
        codes[node.ch] = code if code else "0"     # single-character case
        return codes
    generate_codes(node.left, code + "0", codes)
    generate_codes(node.right, code + "1", codes)
    return codes


def encode(text, codes):
    return "".join(codes[ch] for ch in text)


def decode(bits, root):
    result = []
    node = root
    for b in bits:
        node = node.left if b == "0" else node.right
        if node.left is None and node.right is None:
            result.append(node.ch)
            node = root
    return "".join(result)


def main():
    print("1. Enter a text string")
    print("2. Enter characters and frequencies manually")
    choice = input("Choose option (1/2): ").strip()

    if choice == "2":
        n = int(input("Number of characters: "))
        freq_map = {}
        for _ in range(n):
            ch = input("  Character: ")
            freq_map[ch] = int(input("  Frequency: "))
        text = None
    else:
        text = input("Enter text: ")
        if not text:
            print("Empty input.")
            return
        freq_map = Counter(text)

    root = build_huffman_tree(freq_map)
    codes = generate_codes(root)

    print("\nCharacter | Frequency | Huffman Code")
    print("-" * 36)
    for ch, code in sorted(codes.items(), key=lambda x: (len(x[1]), x[1])):
        print(f"{repr(ch):>9} | {freq_map[ch]:>9} | {code}")

    total_bits_huff = sum(freq_map[ch] * len(codes[ch]) for ch in codes)
    total_chars = sum(freq_map.values())
    total_bits_fixed = total_chars * 8
    print(f"\nTotal bits using Huffman : {total_bits_huff}")
    print(f"Total bits using 8-bit   : {total_bits_fixed}")
    print(f"Space saved              : {100 * (1 - total_bits_huff / total_bits_fixed):.2f}%")

    if text is not None:
        encoded = encode(text, codes)
        print("\nEncoded text :", encoded)
        print("Decoded text :", decode(encoded, root))

    print("\nTime Complexity  : O(n log n)  (n heap insertions + n-1 merges, each O(log n))")
    print("Space Complexity : O(n)        (heap + tree with 2n-1 nodes)")


if __name__ == "__main__":
    main()