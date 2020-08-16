import bcrypt

def encrypt(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()

def validate(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())