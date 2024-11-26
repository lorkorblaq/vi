import base64
import hashlib
import json
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Load the certificate from the file
with open("publickey509.pem", "rb") as cert_file:
    cert_data = cert_file.read()
    certificate = x509.load_pem_x509_certificate(cert_data, backend=default_backend())

# Extract the public key from the certificate
public_key = certificate.public_key()

# Get the modulus (n) and exponent (e) from the public key
numbers = public_key.public_numbers()
n = numbers.n
e = numbers.e

# Convert modulus (n) and exponent (e) to base64url format (remove padding)
n_b64 = base64.urlsafe_b64encode(n.to_bytes((n.bit_length() + 7) // 8, 'big')).rstrip(b'=').decode('utf-8')
e_b64 = base64.urlsafe_b64encode(e.to_bytes((e.bit_length() + 7) // 8, 'big')).rstrip(b'=').decode('utf-8')

# Generate SHA-256 hash of the public key to use as `kid`
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
public_key_hash = hashlib.sha256(public_key_bytes).hexdigest()

# Create the JWK as a dictionary
jwk = {
    "kty": "RSA",
    "kid": public_key_hash,
    "use": "sig",  # optional, but often "sig" for signature verification
    "alg": "RS384",
    "n": n_b64,
    "e": e_b64
}

# Save the JWK to a JSON file in the current directory
with open("public_key_jwk.json", "w") as jwk_file:
    json.dump(jwk, jwk_file, indent=4)

print("JWK has been saved to public_key_jwk.json")
