from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from base64 import b64encode, b64decode
from python_minifier import minify
import os
import random
import string
import threading
import time

def random_chinese_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def obfuscate_python_code(code):
    obfuscated_code = code.translate(str.maketrans('abcdefghijklmnopqrstuvwxyz', 'nopqrstuvwxyzabcdefghijklm'))
    return obfuscated_code

def string_to_hex(string):
    string = obfuscate_python_code(string)
    return ''.join(f'\\x{ord(c):02x}' for c in string)

print(string.digits + string.punctuation)

def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key().decode('utf-8')
    public_key = key.publickey().export_key().decode('utf-8')
    return private_key, public_key

# AES encryption
def aes_encrypt(data, aes_key):
    cipher = AES.new(aes_key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce + ciphertext

# XOR encryption
def xor_encrypt_decrypt(data, key):
    key_bytes = key.encode()
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])


# Encrypt AES key with RSA
def rsa_encrypt(aes_key, public_key):
    rsa_cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
    encrypted_aes_key = rsa_cipher.encrypt(aes_key)
    return encrypted_aes_key

def encrypt_file(file_path, public_key, xor_key):
    with open(file_path, 'rb') as file:
        file_data = file.read()

    aes_key = os.urandom(32)
    encrypted_data = aes_encrypt(file_data, aes_key)
    xor_encrypted_data = xor_encrypt_decrypt(encrypted_data, xor_key)

    encrypted_aes_key = rsa_encrypt(aes_key, public_key)

    encrypted_file_data = b64encode(encrypted_aes_key + xor_encrypted_data).decode('utf-8')
    return encrypted_file_data

def generate_decrypt_script(private_key, xor_key, encrypted_data):
    with open('script.txt', 'r', encoding="utf-8") as file:
        script = file.read()
        script = minify(script)
    
#     I = random_chinese_string(2)
#     l = random_chinese_string(1)
    I = "I"
    l = "l"
    script = script.replace("I", I).replace("l", l).replace(f"Pub{l}icKey", "PublicKey").replace(f"{l}en", "len").replace(f"compi{l}e", "compile").replace(f"rep{l}ace", "replace").replace(f"trans{l}ate", "translate").replace(f"marsha{l}", "marshal")
    test = random_chinese_string(100)
    encrypted_data = string_to_hex(encrypted_data)
    script = script.replace("%encrypted_data%", encrypted_data)
    private_key = string_to_hex(private_key)
    script = script.replace("%private_key%", private_key)
    xor_key = string_to_hex(xor_key)
    script = script.replace("%xor_key%", xor_key)

    with open('decrypt.py', 'w', encoding="utf-8") as file:
        scriptt = minify(script)
        file.write(scriptt)


def main():
    file_path = 'input.txt'


    private_key, public_key = generate_rsa_keys()
    xor_key = random_chinese_string(5)
    encrypted_data = encrypt_file(file_path, public_key, xor_key)

    # Generate decryption script
    generate_decrypt_script(private_key, xor_key, encrypted_data)

    print("Encryption complete. Decryption script saved to 'decrypt.py'.")

if __name__ == "__main__":
    main()