import os
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate


def decode_jwt(req):
    issuer = os.getenv("AUTH0_DOMAIN")
    audience = os.getenv("AUTH0_AUDIENCE")
    cert = os.getenv("AUTH0_CERT").encode("utf-8")
    cert = cert.replace(b"\\n", b"\n")
    # Extract the public key from the certificate
    cert_obj = load_pem_x509_certificate(cert, default_backend())
    public_key = cert_obj.public_key()
    token = req.headers.get("Authorization", "").split("Bearer ")[-1]
    decoded_token = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=audience,
        issuer=issuer,
    )
    return decoded_token