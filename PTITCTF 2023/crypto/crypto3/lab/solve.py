from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from pwn import *
def _encrypt(message):
    r.recvuntil("choice: ")
    r.sendline("1")
    r.recvuntil("to encrypt (in hex): ")
    r.sendline(message.encode("hex"))
    ct = r.recvline("ciphertext (in hex): ").strip()[37:]
    r.recvline()
    r.recvline()
    return ct.decode("hex")

def _decrypt(ciphertext):
    r.recvuntil("choice: ")
    r.sendline("2")
    r.recvuntil("to decrypt (in hex): ")
    r.sendline(ciphertext.encode("hex"))
    pt = r.recvline("plaintext (in hex): ").strip()[36:]
    r.recvline()
    r.recvline()
    return pt.decode("hex")

r = process("./encrypt.py")
r.recvline()
flag_enc = r.recvline().strip()[31:].decode("hex")
N = int(r.recvline().strip()[20:])
print("flag_enc: ", flag_enc)
print("N: ", N)
print("\n\n")

e = 65537
upper_limit = N
lower_limit = 0

flag = ""
i = 1
while i <= 1034:
    chosen_ct = long_to_bytes((bytes_to_long(flag_enc)*pow(2**i, e, N)) % N)
    output = _decrypt(chosen_ct)
    if ord(output[-1]) == 0:
        upper_limit = (upper_limit + lower_limit)/2
    elif ord(output[-1]) == 1:
        lower_limit = (lower_limit + upper_limit)/2
    else:
        break
        print("Unsuccessfull")
    i += 1

print("Flag : ", long_to_bytes(lower_limit))