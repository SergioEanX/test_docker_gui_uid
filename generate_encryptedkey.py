from cryptography.fernet import Fernet


def generate_key():
    """
    Generates a Fernet encryption/decryption key.
    """
    return Fernet.generate_key()


def encrypt_string(key, string_to_encrypt):
    """
    Encrypts a string using the provided key.

    :param key: The encryption key.
    :param string_to_encrypt: The string to encrypt.
    :return: The encrypted string.
    """
    fernet = Fernet(key)
    return fernet.encrypt(string_to_encrypt.encode()).decode()


def decrypt_string(key, encrypted_string):
    """
    Decrypts an encrypted string using the provided key. Returns False if decryption fails.

    :param key: The decryption key.
    :param encrypted_string: The encrypted string to decrypt.
    :return: True if decryption is successful, False otherwise.
    """
    fernet = Fernet(key)
    try:
        # Attempt to decrypt the string
        decrypted_string = fernet.decrypt(encrypted_string.encode()).decode()
        return True
    except Exception as e:
        # Return False if decryption fails
        return False


if __name__ == "__main__":
    # Generate a new key
    # key = generate_key()
    # print(f"Generated key: {key.decode()}")
    key="OvX-ujaqTCH3S1u11CfC1dxY3YDmR97fUln8fKu-u7w="

    # Encrypt a test string
    test_string = "Invoke health-check"
    encrypted_string = encrypt_string(key, test_string)
    print(f"Encrypted string: {encrypted_string}")

    # Decrypt the encrypted string
    result = decrypt_string(key, encrypted_string)
    if result:
        print(f"Decryption successful: {encrypted_string} -> {test_string}")
    else:
        print("Decryption failed.")
