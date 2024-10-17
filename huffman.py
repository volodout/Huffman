# huffman.py

import heapq
import os
import json
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(data):
    frequency = defaultdict(int)

    # Подсчет частоты символов
    for char in data:
        frequency[char] += 1

    # Создание приоритетной очереди
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]  # Возвращаем корень дерева

def build_codes(node, current_code="", codes={}):
    if node is None:
        return

    if node.char is not None:
        codes[node.char] = current_code

    build_codes(node.left, current_code + "0", codes)
    build_codes(node.right, current_code + "1", codes)

    return codes

def huffman_encode(data):
    if not data:
        return "", {}

    root = build_huffman_tree(data)
    codes = build_codes(root)

    encoded_output = "".join(codes[char] for char in data)
    return encoded_output, codes

def huffman_decode(encoded_data, codes):
    reversed_codes = {v: k for k, v in codes.items()}
    current_code = ""
    decoded_output = ""

    for bit in encoded_data:
        current_code += bit
        if current_code in reversed_codes:
            decoded_output += reversed_codes[current_code]
            current_code = ""

    return decoded_output

def save_codes(codes, file_path):
    with open(file_path, 'w') as f:
        json.dump(codes, f)

def load_codes(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
