from hashlib import sha256

print(sha256("12345678".encode('utf-8')).hexdigest())