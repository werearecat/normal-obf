import base64
import codecs
import marshal
import zlib

def xor_encrypt(codee, key=42):
    return ''.join(chr(ord(c) ^ key) for c in codee)

def obfuscate_string(s):
    return ''.join(chr(((ord(c) + 3) % 256)) for c in s)

def custom_substitution(codee):
    return ''.join(chr(ord(c) + 5) for c in codee)

def super_obfcode(codee):
    # Compile and marshal the code
    print("\n[!] gen decrypt code")
    compiled_code = compile(codee, '<string>', 'exec')
    print("\n[!] complie done")
    marshaled_code = marshal.dumps(compiled_code)
    print("\n[!] marshal done")
    # Apply Base64 encoding
    base64_encoded = base64.b64encode(marshaled_code).decode()
    print("\n[!] base64 encode done")

    # Apply XOR encryption
    xor_encrypted = xor_encrypt(base64_encoded)
    print("\n[!] xor encrypted done")
    
    # Apply custom substitution
    substituted_code = custom_substitution(xor_encrypted)
    print("\n[!] xor substituted code done")
    
    # Apply obfuscation
    obfuscated_code = obfuscate_string(substituted_code)
    print("\n[!] obfuscated code done")
    
    # Apply zlib compression
    compressed_code = zlib.compress(obfuscated_code.encode())
    print("\n[!] zlib done")
    
    # Final decryption function
    final_code = f'''
import zlib
import codecs
import base64
import marshal

def xor_encrypt(codee, key=42):
    return ''.join(chr(ord(c) ^ key) for c in codee)

def obfuscate_string(s):
    return ''.join(chr(((ord(c) - 3) % 256)) for c in s)

def custom_substitution(codee):
    return ''.join(chr(ord(c) - 5) for c in codee)

def decrypt_code(encrypted_code):
    # Decompress
    decompressed_code = zlib.decompress(encrypted_code).decode()
    
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

decrypt_code({repr(compressed_code)})
'''
    print("\n[!] done code")
    return final_code

# Example usage
print(super_obfcode('print("Hello World!")'))
