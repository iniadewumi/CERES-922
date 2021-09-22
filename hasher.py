import hashlib
import os


def encode():    
    salt = os.urandom(32) # Remember this
    with open('secrets.txt', 'r') as f:
        password = f.read()

    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
password = "Password"

def compare(salt):
    hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
