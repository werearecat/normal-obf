import marshal
import random
import base64
import random
import codecs
from python_minifier import minify as pyminify
from need.superobf import *
import py_compile

nopqrstuvwxyzabcdefghijklm = "abcdefghijklmnopqrstuvwxyz"

characters = list(nopqrstuvwxyzabcdefghijklm + nopqrstuvwxyzabcdefghijklm.upper())
random.shuffle(characters)
nopqrstuvwxyzabcdefghijklm = ''.join(characters)

random.shuffle(characters)
randomcha = ''.join(characters)

random.shuffle(characters)
nopqrstuvwxyzabcdefghijklm1 = ''.join(characters)
print(nopqrstuvwxyzabcdefghijklm)



def generate_var(length=10):
    return ''.join(f'__{random.randint(0, 255):02x}__gay__' for _ in range(length))

def string_to_hex(string):
    return ''.join(f'\\x{ord(c):02x}' for c in string)

def split_string(text):
    # Tính toán điểm chia chuỗi
    mid_index = len(text) // 2
    # Tách chuỗi thành hai phần
    first_part = text[:mid_index]
    second_part = text[mid_index:]
    return first_part, second_part

def split_string1(text):
    first_part, second_part = split_string(text)
    return first_part

def split_string2(text):
    first_part, second_part = split_string(text)
    return second_part


def t(code):
    letter = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper()
    letter2 = f"{nopqrstuvwxyzabcdefghijklm}"
    print(letter)
    obfuscated_code = code.translate(str.maketrans(letter, letter2))
    return obfuscated_code


with open('code.txt', 'r', encoding='utf-8') as file:
    content = file.read()


def encryptcode(codee):
    compliecode = compile(codee, '<string>', 'exec')
    dump = marshal.dumps(compliecode)
    return f"exec(marshal.loads({dump}))"

def string_to_ascii_values(s):
    return [ord(c) for c in s]

def encryptcode2(code):
    print("\nencryptcode...")
    code = code.replace("dell(", f"{randomcha}(")
    code = encryptcode(code)
    print("\ndone!")
    return code

random = f"hello{random.randint(1000000, 9999999)}hi{generate_var(10)}"

execcodevar = pyminify(f"""
a{random} = "{string_to_hex(split_string1(t(encryptcode(content))))}"
""")

execcodevar1 = pyminify(f"""
aa{random} = "{string_to_hex(split_string2(t(encryptcode(content))))}"
""")

xor_exec = f"""
{execcodevar1}
def xor_encrypt_decrypt(data, key="{random}{random}"):
    # Ensure the key is long enough
    extended_key = (key * (len(data) // len(key) + 1))[:len(data)]
    
    # Perform XOR operation between data and extended key
    result = ''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(data, extended_key))
    
    return result
"""
exec(xor_exec)

execcode = f"""
skid = a{random} + aa{random}
exec(dell(skid))
"""

abcdefghijklmnopqrstuvwxyz = base64.b64encode("abcdefghijklmnopqrstuvwxyz".encode('utf-8')).decode('utf-8')
encoded_nopqrstuvwxyzabcdefghijklm = base64.b64encode(nopqrstuvwxyzabcdefghijklm.encode('utf-8')).decode('utf-8')

defcode = f"""
{execcodevar}

def dell(code):
    letter = base64.b64decode("{abcdefghijklmnopqrstuvwxyz}").decode('utf-8') + base64.b64decode("{abcdefghijklmnopqrstuvwxyz}").decode('utf-8').upper()
    nopqrstuvwxyzabcdefghijklm = base64.b64decode("{encoded_nopqrstuvwxyzabcdefghijklm}").decode('utf-8')
    letter2 = nopqrstuvwxyzabcdefghijklm
    obfuscated_code = code.translate(str.maketrans(letter2, letter))
    return obfuscated_code
"""


code = pyminify(f"""
import marshal
import base64
{encryptcode2(xor_exec)}
exec(xor_encrypt_decrypt("{string_to_hex(xor_encrypt_decrypt(encryptcode2(defcode)))}"))
exec(xor_encrypt_decrypt("{string_to_hex(xor_encrypt_decrypt(encryptcode2(execcode)))}"))
""")


with open('output.txt', 'w') as file:
    file.write(pyminify(super_obfcode(pyminify(code))))

hai1723 = generate_var(100)

obfcode = f"""
import zlib
import codecs
import base64
import marshal
# https://github.com/werearecat/normal-obf
# obf code
{hai1723} = ""
"""

def generate_random_zeroes(length):
    return '\\x00' * length

with open('output.txt', 'r', encoding='utf-8') as file:
    for line in file:
        obfcode += f"""
\n{hai1723} += "{split_string1(string_to_hex(line.strip()))}" + "{generate_random_zeroes(random.randint(1, 10))}" + "{split_string2(string_to_hex(line.strip()))}"
"""

obfcode += f"\n\nexec({hai1723}.replace('\x00', ''))"
with open('output.txt', 'w') as file:
    file.write(obfcode)
