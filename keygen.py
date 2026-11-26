import os
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization


PRIVATE_FILE = "faculty_private.pem"
PUBLIC_FILE = "faculty_public.pem"


def main():
    # TODO: if os.path.exists(PRIVATE_FILE), print a warning and exit
    if os.path.exists(PRIVATE_FILE):
        print("Warning: Private key already exists.")
        return

    # TODO: private_key = Ed25519PrivateKey.generate()
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # TODO: write PRIVATE_FILE in binary mode ("wb")
    #   private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
    with open(PRIVATE_FILE, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # TODO: write PUBLIC_FILE in binary mode ("wb")
    #   public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
    with open(PUBLIC_FILE, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    # TODO: print the file names and the raw sizes (32 bytes each)
    #   private: private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    #   public:  public_bytes(Encoding.Raw, PublicFormat.Raw)
    private_raw = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    print(f"Private key saved to: {PRIVATE_FILE}")
    print(f"Public key saved to: {PUBLIC_FILE}")
    print(f"Private key size: {len(private_raw)} bytes")
    print(f"Public key size: {len(public_raw)} bytes")

if __name__ == "__main__":
    main()
