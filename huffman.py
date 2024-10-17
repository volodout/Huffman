import heapq
from collections import defaultdict


class HuffmanNode:
    def __init__(self, byte, freq):
        self.byte = byte
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(data):
    frequency = defaultdict(int)
    for byte in data:
        frequency[byte] += 1

    heap = [HuffmanNode(byte, freq) for byte, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]


def build_codes(node, current_code="", codes={}):
    if node is None:
        return

    if node.byte is not None:
        codes[node.byte] = current_code

    build_codes(node.left, current_code + "0", codes)
    build_codes(node.right, current_code + "1", codes)

    return codes


def huffman_encode(data):
    if not data:
        return "", {}

    root = build_huffman_tree(data)
    codes = build_codes(root)

    encoded_output = "".join(codes[byte] for byte in data)
    return encoded_output, codes


def huffman_decode(encoded_data, codes):
    reversed_codes = {v: k for k, v in codes.items()}
    current_code = ""
    decoded_output = bytearray()

    for bit in encoded_data:
        current_code += bit
        if current_code in reversed_codes:
            decoded_output.append(reversed_codes[current_code])
            current_code = ""

    return bytes(decoded_output)


def save_codes(codes, file):
    codes_str = str(codes).encode('utf-8')
    file.write(len(codes_str).to_bytes(4, byteorder='big'))
    file.write(codes_str)


def load_codes(file):
    length_bytes = file.read(4)
    length = int.from_bytes(length_bytes, byteorder='big')
    codes_str = file.read(length).decode('utf-8')
    codes = eval(codes_str)
    return codes
