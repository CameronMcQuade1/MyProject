import hashlib
import os


class Hasher:
    @staticmethod
    def hash_pass(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def create_random_password():
        return hashlib.sha256(os.urandom(1024)).hexdigest()
