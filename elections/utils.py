from cryptography.fernet import Fernet
import os

# Store encryption key in environment variable
KEY = os.environ.get('VOTE_ENCRYPTION_KEY', Fernet.generate_key())
fernet = Fernet(KEY)

def encrypt_vote(vote_text):
    return fernet.encrypt(vote_text.encode()).decode()

def decrypt_vote(encrypted_text):
    return fernet.decrypt(encrypted_text.encode()).decode()
