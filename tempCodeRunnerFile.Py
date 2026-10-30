from hashlib import sha256
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt(plaintext: str, timestamp: int) -> str:
    timestamp = int(time.time())
    print(timestamp)
    key = sha256(str(timestamp).encode()).digest()[:16]
    print(key)
    cipher = AES.new(key, AES.MODE_ECB)
    print(cipher)
    padded = pad(plaintext.encode(), AES.block_size)
    print(padded)
    ciphertext = cipher.encrypt(padded)
    print(ciphertext)
    return ciphertext.hex()

if __name__ == "__main__":
    key = " "
    timestamp = int(time.time())
    plaintext = "academy{...}"
    result = encrypt(plaintext, key)
    print(f"Hint: The encryption was done around {timestamp} UTC\n")
    print(f"Ciphertext (hex): {result}\n")