from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import base64
import os
from datetime import datetime, timedelta, timezone

"""
Validates a digital signature against a given challenge using a public key.

Args:
    challenge (str): The original message or challenge string.
    signature (str): The hexadecimal string representation of the signature to be verified.
    public_key_pem (str): The PEM-encoded public key used for verification.

Returns:
    bool: True if the signature is valid, False otherwise.

Raises:
    Exception: If an error occurs during the verification process, an exception is caught and False is returned.
"""


def validate_signatures(challenge: str, signature: str, public_key_pem: str):
    try:
        public_key = serialization.load_pem_public_key(public_key_pem.encode())

        formatted_signature = signature.replace(" ", "+")

        public_key.verify(
            signature=base64.b64decode(formatted_signature),
            data=challenge.encode(),
            padding=padding.PKCS1v15(),
            algorithm=hashes.SHA256(),
        )

        return True
    except Exception as e:
        print(f"Something went wrong chief:{e}")
        return False


def create_challenge_token():
    challenge = os.urandom(32).hex()
    expiration_time = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()

    return {"challenge": challenge, "expiraton_time": expiration_time}
