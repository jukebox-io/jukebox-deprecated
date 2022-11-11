from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# Verifies that the given password matches the corresponding hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Builds hash from given password
def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


# Debug
if __name__ == '__main__':
    secret = 'pass123'
    hashed_secret = get_password_hash(secret)
    print(f'{secret} <-> {hashed_secret}')
    print(f'Matched: {verify_password(secret, hashed_secret)}')
