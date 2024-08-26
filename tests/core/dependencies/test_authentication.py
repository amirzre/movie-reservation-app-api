from unittest.mock import MagicMock, patch

import pytest
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials

from core.exceptions import UnauthorizedException
from core.fastapi.dependencies.authentication import AuthenticationHandler
from core.security import JWTHandler


@pytest.mark.asyncio
class TestAuthenticationHandler:
    @pytest.fixture
    def mock_request(self):
        req = MagicMock(spec=Request)
        req.cookies = {"Access-Token": "fake_access_token"}
        return req

    @patch.object(JWTHandler, "decode", return_value={"uuid": "user-uuid"})
    async def test_authenticate_user_success(self, mock_decode, mock_request):
        handler = AuthenticationHandler(mock_request)
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="fake_access_token")

        user_uuid = await handler.authenticate_user(token_type="Access", key="uuid", credentials=credentials)

        assert user_uuid == "user-uuid"
        mock_decode.assert_called_once_with(token="fake_access_token")

    async def test_authenticate_user_missing_token(self, mock_request):
        mock_request.cookies = {}  # No token in cookies
        handler = AuthenticationHandler(mock_request)

        with pytest.raises(UnauthorizedException):
            await handler.authenticate_user(token_type="Access", key="uuid")

    @patch.object(JWTHandler, "decode", return_value={})
    async def test_authenticate_user_invalid_token(self, mock_decode, mock_request):
        handler = AuthenticationHandler(mock_request)
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="fake_access_token")

        with pytest.raises(UnauthorizedException):
            await handler.authenticate_user(token_type="Access", key="uuid", credentials=credentials)

    async def test_authenticate_user_token_validation_failure(self, mock_request):
        handler = AuthenticationHandler(mock_request)
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="wrong_token")

        with pytest.raises(UnauthorizedException):
            await handler.authenticate_user(token_type="Access", key="uuid", credentials=credentials)
