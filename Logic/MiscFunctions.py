import hashlib

def HashString(value):
    hash_object = hashlib.sha256(value.encode('utf-8'))
    x = hash_object.hexdigest()
    return x