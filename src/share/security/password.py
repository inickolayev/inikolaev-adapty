import bcrypt

# bcrypt silently truncates input longer than 72 bytes — truncate explicitly to keep
# hashing and verification consistent.
MAX_PASSWORD_BYTES = 72


def hash_password(plain: str) -> str:
    password_bytes = plain.encode('utf-8')[:MAX_PASSWORD_BYTES]
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    password_bytes = plain.encode('utf-8')[:MAX_PASSWORD_BYTES]
    return bcrypt.checkpw(password_bytes, hashed.encode('utf-8'))
