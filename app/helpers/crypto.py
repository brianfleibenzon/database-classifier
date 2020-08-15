import os
from cryptography.fernet import Fernet

def encrypt(data):  
  f = Fernet(os.environ.get("CRYPTO_KEY"))
  encrypted = f.encrypt(data.encode())
  return encrypted.decode()

def decrypt(data):  
  f = Fernet(os.environ.get("CRYPTO_KEY"))
  decrypted = f.decrypt(data.encode())
  return decrypted.decode()