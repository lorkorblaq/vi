# createJWT.py
import time
import uuid
import jwt  # PyJWT
from cryptography.hazmat.primitives import serialization

kid = "ed17a986e96eaa1f06fb7b40167da25c93682387fad6e977b47e446cfc3f0b89"

class JWTGenerator:
    def __init__(self, client_id, kid=kid, private_key_path="privatekey.pem", alg="RS384", audience="https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"):
        self.private_key_path = private_key_path
        self.client_id = client_id
        self.kid = kid
        self.alg = alg
        self.audience = audience
        self.private_key = self._load_private_key()

    def _load_private_key(self):
        with open(self.private_key_path, "rb") as key_file:
            private_key_data = key_file.read()
        return serialization.load_pem_private_key(private_key_data, password=None)

    def generate_jwt(self):
        header = {
            "alg": self.alg,
            "typ": "JWT",
            "kid": self.kid,
        }
        payload = {
            "iss": self.client_id,
            "sub": self.client_id,
            "aud": self.audience,
            "jti": str(uuid.uuid4()),
            "exp": int(time.time()) + 300,
        }
        return jwt.encode(payload, self.private_key, algorithm=self.alg, headers=header)
