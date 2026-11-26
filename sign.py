import sys
from cryptography.hazmat.primitives import serialization


def main():
    # TODO: if len(sys.argv) != 3, print usage and exit
    if len(sys.argv) != 3:
        print(f"How to use: python3 {sys.argv[0]} <Target File Name> <Private_Key.pem>")
        sys.exit(1)
    
    notice_path = sys.argv[1]
    key_path = sys.argv[2]

    # TODO: read key_path in binary mode and load the private key
    #   serialization.load_pem_private_key(data, password=None)
    with open(key_path, "rb") as key_file:
        data = key_file.read()
    private_key = serialization.load_pem_private_key(data, password=None)

    # TODO: read notice_path in binary mode ("rb")
    with open(notice_path, "rb") as notice_file:
        message = notice_file.read()

    # TODO: signature = private_key.sign(message)
    signature = private_key.sign(message)

    # TODO: write signature to "notice.sig" in binary mode ("wb")
    with open("notice.sig", "wb") as signature_file:
        signature_file.write(signature)

    # TODO: print the file name, len(message), len(signature)
    #       and signature.hex()
    print(f"File Name: {notice_path}")
    print(f"File Size: {len(message)} bytes")
    print(f"Signature Size: {len(signature)} bytes")
    print(f"Signature (hexidemal): {signature.hex()}")

if __name__ == "__main__":
    main()
