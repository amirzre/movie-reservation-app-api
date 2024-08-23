import pytest
from passlib.exc import UnknownHashError

from core.security import PasswordHandler


class TestPasswordHandler:
    @pytest.fixture(scope="class")
    def plain_password(self):
        return "secure_password"

    @pytest.fixture(scope="class")
    def hashed_password(self, plain_password):
        return PasswordHandler.hash(plain_password)

    def test_hash_returns_string(self, plain_password):
        hashed = PasswordHandler.hash(plain_password)
        assert isinstance(hashed, str)

    def test_hash_is_different_each_time(self, plain_password):
        hashed1 = PasswordHandler.hash(plain_password)
        hashed2 = PasswordHandler.hash(plain_password)
        assert hashed1 != hashed2

    def test_verify_correct_password(self, plain_password, hashed_password):
        assert PasswordHandler.verify(hashed_password, plain_password)

    def test_verify_incorrect_password(self, hashed_password):
        incorrect_password = "wrong_password"
        assert not PasswordHandler.verify(hashed_password, incorrect_password)

    def test_verify_with_plaintext_password_fails(self, plain_password):
        with pytest.raises(UnknownHashError):
            PasswordHandler.verify(plain_password, plain_password)

    def test_hash_with_empty_password(self):
        hashed = PasswordHandler.hash("")
        assert isinstance(hashed, str)
        assert PasswordHandler.verify(hashed, "")

    def test_hash_with_special_characters(self):
        special_password = "!@#$%^&*()_+[]{};':\",./<>?"
        hashed = PasswordHandler.hash(special_password)
        assert isinstance(hashed, str)
        assert PasswordHandler.verify(hashed, special_password)

    def test_hash_with_unicode_characters(self):
        unicode_password = "pässwörd😊"
        hashed = PasswordHandler.hash(unicode_password)
        assert isinstance(hashed, str)
        assert PasswordHandler.verify(hashed, unicode_password)

    def test_verify_with_modified_hash(self, plain_password, hashed_password):
        modified_hash = hashed_password[:-1] + ("0" if hashed_password[-1] != "0" else "1")
        assert not PasswordHandler.verify(modified_hash, plain_password)

    def test_verify_with_none_as_password(self, hashed_password):
        with pytest.raises(TypeError):
            PasswordHandler.verify(hashed_password, None)

    def test_verify_with_empty_hashed_password(self, plain_password):
        with pytest.raises(UnknownHashError):
            PasswordHandler.verify("", plain_password)

    def test_hash_long_password(self):
        long_password = "a" * 1000
        hashed = PasswordHandler.hash(long_password)
        assert isinstance(hashed, str)
        assert PasswordHandler.verify(hashed, long_password)
