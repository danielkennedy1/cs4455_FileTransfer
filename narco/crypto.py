from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Util.Padding import pad, unpad


def encrypt_file(shared_secret, file_path):
    cipher = AES.new(shared_secret, AES.MODE_CBC)

    with open(file_path, "rb") as file:
        plaintext = file.read()

    padded_data = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext


def decrypt_file(shared_secret, ciphertext):
    cipher = AES.new(shared_secret, AES.MODE_CBC)
    plaintext = cipher.decrypt(ciphertext)
    return unpad(plaintext, AES.block_size)


def derive_shared_secret(sender_private_key, receiver_public_key):
    shared_secret = scrypt(
        sender_private_key.export_key(),
        receiver_public_key.export_key(),
        key_len=32,
        N=2**14,
        r=8,
        p=1,
    )

    return (
        shared_secret  # 32 bytes of a shared secret generated by scrypt (AES-256 key)
    )


def file_to_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        return file.read()
