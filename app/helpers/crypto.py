import os
from cryptography.fernet import Fernet
from flask import current_app

def encrypt(data):  
  f = Fernet(current_app.config.get("CRYPTO_KEY"))
  encrypted = f.encrypt(data.encode())
  return encrypted.decode()

def decrypt(data):
  f = Fernet(current_app.config.get("CRYPTO_KEY"))
  decrypted = f.decrypt(data.encode())
  return decrypted.decode()