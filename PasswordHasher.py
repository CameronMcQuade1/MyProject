import hashlib
import os
import base64


class Hasher:
    @staticmethod
    def hash_password(password: str, iterations: int = 100000) -> str:
        salt = os.urandom(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
        salt_b64 = base64.b64encode(salt).decode('utf-8')
        hash_b64 = base64.b64encode(pwd_hash).decode('utf-8')
        return f"{salt_b64}${hash_b64}${iterations}"

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        salt_b64, stored_hash_b64, iterations = stored_password.split('$')
        salt = base64.b64decode(salt_b64.encode('utf-8'))
        iterations = int(iterations)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, iterations)
        return base64.b64encode(pwd_hash).decode('utf-8') == stored_hash_b64

    @staticmethod
    def create_random_password() -> str:
        random_password = base64.b64encode(os.urandom(12)).decode('utf-8')
        hashed_password = Hasher.hash_password(random_password)
        return hashed_password
