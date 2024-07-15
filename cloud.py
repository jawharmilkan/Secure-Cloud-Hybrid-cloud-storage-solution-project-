from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import os

# Symmetric Encryption (AES)
def symmetric_encrypt(plain_text, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(plain_text.encode()) + encryptor.finalize()
    return iv + cipher_text

def symmetric_decrypt(cipher_text, key):
    iv = cipher_text[:16]
    actual_cipher_text = cipher_text[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plain_text = decryptor.update(actual_cipher_text) + decryptor.finalize()
    return plain_text.decode()

# Asymmetric Encryption (RSA)
def generate_asymmetric_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def asymmetric_encrypt(symmetric_key, public_key):
    cipher_text = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return cipher_text

def asymmetric_decrypt(cipher_text, private_key):
    symmetric_key = private_key.decrypt(
        cipher_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return symmetric_key

# Main Hybrid Encryption
def hybrid_encrypt(plain_text, public_key):
    symmetric_key = os.urandom(32)
    cipher_text = symmetric_encrypt(plain_text, symmetric_key)
    encrypted_key = asymmetric_encrypt(symmetric_key, public_key)
    return encrypted_key + cipher_text

def hybrid_decrypt(cipher_text, private_key):
    encrypted_key = cipher_text[:256]
    actual_cipher_text = cipher_text[256:]
    symmetric_key = asymmetric_decrypt(encrypted_key, private_key)
    plain_text = symmetric_decrypt(actual_cipher_text, symmetric_key)
    return plain_text

# Example Usage
private_key, public_key = generate_asymmetric_keys()
message = "SecureCloud: Hybrid Symmetric Encryption"
encrypted = hybrid_encrypt(message, public_key)
print(f"Encrypted: {encrypted}")

decrypted = hybrid_decrypt(encrypted, private_key)
print(f"Decrypted: {decrypted}")
