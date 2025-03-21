from cryptography.fernet import Fernet


_path = "/opt/projects/secret.key"


def generate_key():
  key = Fernet.generate_key()

  with open(_path, "wb") as key_file:
    key_file.write(key)


# 🔹 Load the stored key
def load_key():
  with open(_path, "rb") as key_file:
    return key_file.read()


# 🔹 Encrypt a password
def encrypt_password(password: str) -> str:
  key = load_key()

  cipher = Fernet(key)
  encrypted_password = cipher.encrypt(password.encode())

  return encrypted_password.decode()


def decrypt_password(encrypted_password: str) -> str:
  key = load_key()

  cipher = Fernet(key)
  decrypted_password = cipher.decrypt(encrypted_password.encode())

  return decrypted_password.decode()


