import hashlib


class Hasher:
    @staticmethod
    def hash_pass(password):
        return hashlib.sha256(password.encode()).hexdigest()
