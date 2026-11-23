import sys
import hashlib
from cryptography.hazmat.primitives import serialization


def main():
    # Check the argument count before touching sys.argv[1]; otherwise a
    # missing argument would crash with an IndexError instead of a clear message.
    if len(sys.argv) != 2:
        print("Usage: python fingerprint.py <public_key.pem>")
        sys.exit(1)
    pem_path = sys.argv[1]

    # Read the PEM file in binary mode ("rb"): load_pem_public_key() expects
    # bytes, not a str.
    try:
        with open(pem_path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: key file '{pem_path}' not found.")
        sys.exit(1)

    # Parse the PEM into a public key object. If the file is not a PEM public
    # key (for example a private key or a text file), show a one-line error
    # instead of a traceback. The file's contents are never printed.
    try:
        public_key = serialization.load_pem_public_key(data)
    except ValueError:
        print(f"Error: '{pem_path}' is not a valid PEM public key.")
        sys.exit(1)

    # Extract the raw public key bytes (32 bytes for Ed25519). PEM adds
    # headers and ASN.1 wrapping; the raw form is just the key itself, so the
    # fingerprint depends only on the key and not on the file formatting.
    # Raw encoding only exists for Ed25519/X25519-style keys, so other key
    # types (e.g. RSA) raise ValueError here.
    try:
        raw = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
    except ValueError:
        print(f"Error: key type in '{pem_path}' is not supported "
              "(only Ed25519/X25519 public keys).")
        sys.exit(1)

    # SHA-256 of the raw key. The same key always gives the same digest, and
    # different keys give completely different digests.
    digest = hashlib.sha256(raw).hexdigest()

    # Short fingerprint: first 16 hex characters, in groups of 4 for reading.
    short = " ".join(digest[i:i + 4] for i in range(0, 16, 4))

    print(f"File:        {pem_path}")
    print(f"Raw key:     {len(raw)} bytes")
    print(f"Fingerprint: {short}")
    print(f"SHA-256:     {digest}")


if __name__ == "__main__":
    main()
