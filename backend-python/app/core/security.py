import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone

from app.utils.exceptions import AuthenticationError, ValidationError

TOKEN_SECRET = os.getenv("AUTH_SECRET", "flowdesk-dev-secret")
TOKEN_EXP_MINUTES = int(os.getenv("AUTH_TOKEN_EXP_MINUTES", "60"))


def _encode_bytes(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("utf-8").rstrip("=")


def _decode_bytes(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(f"{value}{padding}")


def hash_password(password: str) -> str:
    if len(password) < 8:
        raise ValidationError("La contrasena debe tener al menos 8 caracteres.")

    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"{_encode_bytes(salt)}${_encode_bytes(digest)}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt_token, digest_token = password_hash.split("$", 1)
    except ValueError:
        return False

    salt = _decode_bytes(salt_token)
    expected_digest = _decode_bytes(digest_token)
    current_digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return hmac.compare_digest(current_digest, expected_digest)


def create_access_token(*, user_id: int, role_name: str, email: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXP_MINUTES)
    payload = {
        "sub": str(user_id),
        "role": role_name,
        "email": email,
        "exp": int(expires_at.timestamp()),
    }
    payload_token = _encode_bytes(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )
    signature = hmac.new(
        TOKEN_SECRET.encode("utf-8"),
        payload_token.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return f"{payload_token}.{_encode_bytes(signature)}"


def decode_access_token(token: str) -> dict:
    try:
        payload_token, signature_token = token.split(".", 1)
    except ValueError as exc:
        raise AuthenticationError("Token invalido.") from exc

    expected_signature = hmac.new(
        TOKEN_SECRET.encode("utf-8"),
        payload_token.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    if not hmac.compare_digest(expected_signature, _decode_bytes(signature_token)):
        raise AuthenticationError("Token invalido.")

    payload = json.loads(_decode_bytes(payload_token).decode("utf-8"))
    if int(payload["exp"]) < int(datetime.now(timezone.utc).timestamp()):
        raise AuthenticationError("Token expirado.")

    return payload
