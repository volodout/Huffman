import heapq
from collections import defaultdict
from node import Node


def build_tree(text):
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1

    heap = [Node(char, freq) for char, freq in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]
