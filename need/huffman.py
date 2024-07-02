import heapq
from collections import Counter, defaultdict

def build_huffman_tree(s):
    heap = [[wt, [sym, ""]] for sym, wt in Counter(s).items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def huffman_encode(s):
    huff_tree = build_huffman_tree(s)
    huff_code = {sym: code for sym, code in huff_tree}
    encoded = ''.join(huff_code[ch] for ch in s)
    return encoded, huff_code

def huffman_decode(encoded, huff_code):
    reversed_code = {v: k for k, v in huff_code.items()}
    current_code = ""
    decoded = []
    for bit in encoded:
        current_code += bit
        if current_code in reversed_code:
            decoded.append(reversed_code[current_code])
            current_code = ""
    return ''.join(decoded)

# Ví dụ sử dụng
if __name__ == "__main__":
    s = "this is an example for huffman encoding"
    encoded, huff_code = huffman_encode(s)
    print(f"Encoded: {encoded}")
    decoded = huffman_decode(encoded, huff_code)
    print(f"Decoded: {decoded}")
