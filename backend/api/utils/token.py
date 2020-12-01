import time
import hashlib

def get_token_code(username):
    timesamp = str(time.time())
    md5 = hashlib.md5(username.encode("utf-8"))
    md5.update(timesamp.encode("utf-8"))
    return md5.hexdigest()