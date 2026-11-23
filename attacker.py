import os
import sys
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization


def main():
    # Check the argument count before touching sys.argv[1]; otherwise a
    # missing argument would crash with an IndexError instead of a clear message.
    if len(sys.argv) != 2:
        print("Usage: python attacker.py <notice_file>")
        sys.exit(1)
    notice_path = sys.argv[1]

    # Confirm the notice exists BEFORE generating keys, so a typo in the
    # file name does not leave unused attacker key files behind.
    if not os.path.isfile(notice_path):
        print(f"Error: notice file '{notice_path}' not found.")
        sys.exit(1)

    # Generate a brand-new Ed25519 key pair. This is the attacker's own key,
    # completely unrelated to the faculty key pair.
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Save the private key as PEM (PKCS8 format, no password).
    # private_bytes() returns bytes, so the file is opened in binary mode ("wb")
    # to write them exactly as produced. The key itself is never printed.
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open("attacker_private.pem", "wb") as f:
        f.write(private_pem)

    # Save the public key as PEM (SubjectPublicKeyInfo, the standard format
    # for public keys). Also bytes, so binary mode again.
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open("attacker_public.pem", "wb") as f:
        f.write(public_pem)

    # Read the notice in binary mode ("rb") so we sign the exact bytes on disk.
    # Text mode could change line endings (\r\n vs \n) or the encoding, and
    # then the signature would not match the file that verify.py reads.
    with open(notice_path, "rb") as f:
        data = f.read()

    # Sign the raw bytes directly. Ed25519 hashes internally (SHA-512),
    # so we must NOT hash the data ourselves first.
    signature = private_key.sign(data)

    # Store the raw 64-byte signature (not hex, not base64) in binary mode,
    # because verify.py expects the raw signature bytes.
    with open("attacker.sig", "wb") as f:
        f.write(signature)

    # Report what happened. The private key file is listed by name only.
    print("Attacker key pair generated (Ed25519)")
    print()
    print(f"Notice signed:   {notice_path} ({len(data)} bytes)")
    print("Private key:     attacker_private.pem  (kept secret, not shown)")
    print("Public key:      attacker_public.pem")
    print("Signature file:  attacker.sig")
    print(f"Signature size:  {len(signature)} bytes")
    print(f"Signature (hex): {signature.hex()}")
    print("Note: running this again creates a NEW attacker key pair and overwrites these files.")


if __name__ == "__main__":
    main()
