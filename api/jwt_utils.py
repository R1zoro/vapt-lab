import base64
import json
import hashlib

SECRET = "secret123"  # weak on purpose

def encode(data):
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode().strip("=")

def decode(data):
    padding = '=' * (-len(data) % 4)
    return json.loads(base64.urlsafe_b64decode(data + padding).decode())

def sign(payload_encoded):
    return hashlib.sha256((payload_encoded + SECRET).encode()).hexdigest()

def generate_token(username, role):
    header = encode({"alg": "HS256", "typ": "JWT"})
    payload = encode({"user": username, "role": role})

    signature = sign(payload)

    return f"{header}.{payload}.{signature}"

def verify_token(token):
    try:
        header, payload, signature = token.split(".")

        expected_signature = sign(payload)

        if expected_signature != signature:
            return None

        return decode(payload)

    except:
        return None