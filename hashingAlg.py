import hashlib
import os

def hash_new_password(password):
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000, dklen=64)
    return salt, dk

def verify_password(stored_salt, stored_hash, password_to_check):
    new_dk = hashlib.pbkdf2_hmac("sha256", password_to_check.encode(), stored_salt, 100000, dklen=64)
    return new_dk == stored_hash

def hash_password_no_salt(password):
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), 100000, dklen=64)
    return dk

print(hash_new_password("kp9"))