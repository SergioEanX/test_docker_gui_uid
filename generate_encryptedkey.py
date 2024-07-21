from cryptography.fernet import Fernet


def generate_encrypted_key(decryption_key: str, value_to_encrypt: str) -> str:
    fernet = Fernet(decryption_key.encode())
    encrypted_value = fernet.encrypt(value_to_encrypt.encode())
    return encrypted_value.decode()


def generate_decryption_key():
    key = Fernet.generate_key()
    return key.decode()


if __name__ == "__main__":
    generateEK= False
    if generateEK:
        # Generate a new decryption key
        decryption_key = generate_decryption_key()
        print(f"Decryption Key: {decryption_key}")

    # Replace this with the actual decryption key used in the Docker environment
    dk = "your_decryption_key"  # 32 url-safe base64-encoded bytes
    # The value that the server expects to decrypt and match
    value_to_encrypt = "rcjR4e4hFHJbwqTwlHBMgqnnklLwtTKuRjSeBtaTJaM="
    encrypted_value = generate_encrypted_key(dk, value_to_encrypt)
    print(f"Encrypted key: {encrypted_value}")
