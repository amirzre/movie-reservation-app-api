from datetime import datetime, timezone
from unittest.mock import patch

import jwt
import pytest

from core.security.jwt import JWTDecodeError, JWTExpiredError, JWTHandler


class TestJWTHandler:
    @pytest.fixture(scope="class")
    def valid_payload(self):
        return {"user_uuid": "a3b8f042-1e16-4f0a-a8f0-421e16df0a2f", "role": "USER"}

    @pytest.fixture(scope="class")
    def expired_token(self, valid_payload):
        with patch("core.security.jwt.JWTHandler.access_token_expire", -1):
            return JWTHandler.encode(valid_payload)

    @pytest.fixture(scope="class")
    def valid_token(self, valid_payload):
        return JWTHandler.encode(valid_payload)

    @pytest.fixture(scope="class")
    def valid_refresh_token(self, valid_payload):
        return JWTHandler.encode_refresh_token(valid_payload)

    @pytest.fixture(scope="class")
    def invalid_token(self):
        return "invalid.token.string"

    @pytest.fixture(scope="class")
    def malformed_token(self):
        return jwt.encode({"user_uuid": "a3b8f042-1e16-4f0a-a8f0-421e16df0a2f"}, key=JWTHandler.secret_key)[
            :-1
        ]  # Remove last char to corrupt

    def test_encode(self, valid_payload):
        token = JWTHandler.encode(valid_payload)
        assert isinstance(token, str)
        decoded = jwt.decode(token, key=JWTHandler.secret_key, algorithms=[JWTHandler.algorithm])
        assert decoded["user_uuid"] == valid_payload.get("user_uuid")
        assert decoded["role"] == valid_payload.get("role")

    def test_encode_refresh_token(self, valid_payload):
        token = JWTHandler.encode_refresh_token(valid_payload)
        assert isinstance(token, str)
        decoded = jwt.decode(token, key=JWTHandler.secret_key, algorithms=[JWTHandler.algorithm])
        assert decoded["user_uuid"] == valid_payload.get("user_uuid")
        assert decoded["role"] == valid_payload.get("role")

    def test_decode_valid_token(self, valid_token, valid_payload):
        decoded = JWTHandler.decode(valid_token)
        assert decoded["user_uuid"] == valid_payload.get("user_uuid")
        assert decoded["role"] == valid_payload.get("role")

    def test_decode_invalid_token(self, invalid_token):
        with pytest.raises(JWTDecodeError):
            JWTHandler.decode(invalid_token)

    def test_decode_malformed_token(self, malformed_token):
        with pytest.raises(JWTDecodeError):
            JWTHandler.decode(malformed_token)

    def test_decode_expired_token(self, expired_token):
        with pytest.raises(JWTExpiredError):
            JWTHandler.decode(expired_token)

    def test_decode_expired_token_success(self, expired_token, valid_payload):
        decoded = JWTHandler.decode_expired(expired_token)
        assert decoded["user_uuid"] == valid_payload.get("user_uuid")
        assert decoded["role"] == valid_payload.get("role")

    def test_decode_expired_token_invalid(self, invalid_token):
        with pytest.raises(JWTDecodeError):
            JWTHandler.decode_expired(invalid_token)

    def test_token_expiration_valid(self, valid_token):
        expiration = JWTHandler.token_expiration(valid_token)
        assert expiration > datetime.now(timezone.utc)

    def test_token_expiration_expired(self, expired_token):
        with pytest.raises(JWTExpiredError):
            JWTHandler.token_expiration(expired_token)

    def test_token_expiration_invalid(self, invalid_token):
        with pytest.raises(JWTDecodeError):
            JWTHandler.token_expiration(invalid_token)

    def test_token_expiration_malformed(self, malformed_token):
        with pytest.raises(JWTDecodeError):
            JWTHandler.token_expiration(malformed_token)

    def test_decode_with_no_exp_claim(self):
        payload = {"user_uuid": "a3b8f042-1e16-4f0a-a8f0-421e16df0a3g"}
        token = jwt.encode(payload, key=JWTHandler.secret_key, algorithm=JWTHandler.algorithm)
        decoded = JWTHandler.decode_expired(token)
        assert decoded["user_uuid"] == payload["user_uuid"]

    def test_decode_expired_with_no_exp_claim(self):
        payload = {"user_uuid": "a3b8f042-1e16-4f0a-a8f0-421e16df0a3g"}
        token = jwt.encode(payload, key=JWTHandler.secret_key, algorithm=JWTHandler.algorithm)
        decoded = JWTHandler.decode_expired(token)
        assert decoded["user_uuid"] == payload["user_uuid"]
