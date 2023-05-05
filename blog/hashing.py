from passlib.context import CryptContext

# PassWord hashing using passlib
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(password):
        hashPW = pwd_cxt.hash(password)

        return hashPW
