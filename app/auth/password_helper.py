from argon2 import PasswordHasher


class PasswordHelper:
    _pw_hasher = PasswordHasher()

    @classmethod
    def hash(cls, password: str) -> str:
        return cls._pw_hasher.hash(password)

    @classmethod
    def verify(cls, pw_hash: str, password: str) -> bool:
        return cls._pw_hasher.verify(pw_hash, password)

    @classmethod
    def is_rehash_needed(cls, pw_hash: str) -> bool:
        return cls._pw_hasher.check_needs_rehash(pw_hash)
