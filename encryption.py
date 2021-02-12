from cryptography.fernet import Fernet

def encrypt_message(message):
    key = Fernet.generate_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    encrypted_message = encrypted_message.decode()
    encrypted_message += f",{key.decode()}"
    return encrypted_message


def decrypt_message(message):
    key = message.split(",")[1].encode()
    f = Fernet(key)
    encoded_message = message.encode()
    decrypted_message = f.decrypt(encoded_message)
    return decrypted_message.decode()
