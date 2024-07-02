import base64
import codecs
import marshal
import zlib
import heapq
from collections import Counter, defaultdict

# Huffman Coding
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = Counter(text)
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)
    
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    
    return priority_queue[0]

def build_codes(node, prefix='', codebook=defaultdict()):
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        build_codes(node.left, prefix + '0', codebook)
        build_codes(node.right, prefix + '1', codebook)
    return codebook

def huffman_encode(text):
    root = build_huffman_tree(text)
    codes = build_codes(root)
    encoded_text = ''.join(codes[char] for char in text)
    padding = 8 - len(encoded_text) % 8
    encoded_text = f"{padding:08b}" + encoded_text + '0' * padding
    b = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        b.append(int(byte, 2))
    return bytes(b), codes

def huffman_decode(encoded_text, codes):
    reverse_codes = {v: k for k, v in codes.items()}
    binary_string = ''.join(f'{byte:08b}' for byte in encoded_text)
    padding = int(binary_string[:8], 2)
    binary_string = binary_string[8:-padding]
    current_code = ''
    decoded_chars = []
    for bit in binary_string:
        current_code += bit
        if current_code in reverse_codes:
            decoded_chars.append(reverse_codes[current_code])
            current_code = ''
    return ''.join(decoded_chars)

# Encryption Functions
def xor_encrypt(codee, key=42):
    return ''.join(chr(ord(c) ^ key) for c in codee)

def obfuscate_string(s):
    return ''.join(chr(((ord(c) + 3) % 256)) for c in s)

def custom_substitution(codee):
    return ''.join(chr(ord(c) + 5) for c in codee)

# Main Obfuscation Function
def super_obfcode(codee):
    # Compile and marshal the code
    compiled_code = compile(codee, '<string>', 'exec')
    marshaled_code = marshal.dumps(compiled_code)
    
    # Apply Base64 encoding
    base64_encoded = base64.b64encode(marshaled_code).decode()

    # Apply XOR encryption
    xor_encrypted = xor_encrypt(base64_encoded)
    
    # Apply custom substitution
    substituted_code = custom_substitution(xor_encrypted)
    
    # Apply obfuscation
    obfuscated_code = obfuscate_string(substituted_code)
    
    # Apply zlib compression
    compressed_code = zlib.compress(obfuscated_code.encode())
    
    # Apply Huffman encoding
    huffman_encoded, huffman_codes = huffman_encode(compressed_code.decode('latin1'))
    
    # Final decryption function
    final_code = f'''
import zlib
import codecs
import base64
import marshal
import heapq
from collections import defaultdict, Counter

# Huffman Coding
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = Counter(text)
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)
    
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    
    return priority_queue[0]

def build_codes(node, prefix='', codebook=defaultdict()):
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        build_codes(node.left, prefix + '0', codebook)
        build_codes(node.right, prefix + '1', codebook)
    return codebook

def huffman_encode(text):
    root = build_huffman_tree(text)
    codes = build_codes(root)
    encoded_text = ''.join(codes[char] for char in text)
    padding = 8 - len(encoded_text) % 8
    encoded_text = f"{padding:08b}" + encoded_text + '0' * padding
    b = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        b.append(int(byte, 2))
    return bytes(b), codes

def huffman_decode(encoded_text, codes):
    reverse_codes = {v: k for k, v in codes.items()}
    binary_string = ''.join(f'{byte:08b}' for byte in encoded_text)
    padding = int(binary_string[:8], 2)
    binary_string = binary_string[8:-padding]
    current_code = ''
    decoded_chars = []
    for bit in binary_string:
        current_code += bit
        if current_code in reverse_codes:
            decoded_chars.append(reverse_codes[current_code])
            current_code = ''
    return ''.join(decoded_chars)

def xor_encrypt(codee, key=42):
    return ''.join(chr(ord(c) ^ key) for c in codee)

def obfuscate_string(s):
    return ''.join(chr(((ord(c) - 3) % 256)) for c in s)

def custom_substitution(codee):
    return ''.join(chr(ord(c) - 5) for c in codee)

def decrypt_code(encrypted_code):
    # Decode Huffman
    decoded_code = huffman_decode(encrypted_code, huffman_codes)
    
    # Decompress
    decompressed_code = zlib.decompress(decoded_code.encode('latin1')).decode()
    
    # Reverse obfuscation
    deobfuscated_code = obfuscate_string(decompressed_code)
    
    # Reverse custom substitution
    unsubstituted_code = custom_substitution(deobfuscated_code)
    
    # Reverse XOR encryption
    base64_encoded = xor_encrypt(unsubstituted_code)
    
    # Decode Base64
    marshaled_code = base64.b64decode(base64_encoded)
    
    # Load and execute the code
    compiled_code = marshal.loads(marshaled_code)
    exec(compiled_code)

decrypt_code({repr(huffman_encoded)})
'''

    return final_code

# Example usage
print(super_obfcode('print("Hello World!")'))
