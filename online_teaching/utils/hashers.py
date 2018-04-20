# -*- coding: utf-8 -*-
import hashlib
from config import PASSWORD_SALT


def make_password(raw_password,salt=None):
    if not salt:
        salt = PASSWORD_SALT
    if not raw_password:
        return False
    hash_password = hashlib.md5(raw_password+salt).hexdigest()

    return hash_password


def check_password(raw_password,password):
    if not raw_password:
        return False

    temp_password = make_password(raw_password)
    if temp_password == password:
        return True
    else:
        return False


if __name__ == "__main__":
    pwd = "aaaaaa"
    print make_password(pwd)