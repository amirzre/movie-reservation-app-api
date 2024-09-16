from uuid import uuid4

import pytest
import pytest_asyncio
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from app.models.user import UserRole
from app.schemas.request import RegisterUserRequest, UpdateUserRequest

fake = Faker()


@pytest.mark.asyncio
class TestUserEndpoints:
    @pytest_asyncio.fixture
    async def test_user(self, client: AsyncClient) -> dict:
        user_data = {
            "email": fake.email(),
            "password": fake.password(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "role": UserRole.USER,
            "activated": True,
        }
        response = await client.post("/api/v1/users/", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()

    async def test_get_all_users(self, client: AsyncClient, auth_token_admin: tuple[str, str]):
        access_token, _ = auth_token_admin
        response = await client.get("/api/v1/users/", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_200_OK
        users = response.json()
        assert isinstance(users, list)

    async def test_get_all_users_non_admin(self, client: AsyncClient, auth_token_user: tuple[str, str]):
        access_token, _ = auth_token_user
        response = await client.get("/api/v1/users/", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_get_all_users_unauthorized(self, client: AsyncClient):
        response = await client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_user_by_id(self, client: AsyncClient, auth_token_admin: tuple[str, str], test_user: dict):
        access_token, _ = auth_token_admin
        user_uuid = test_user["uuid"]

        response = await client.get(f"/api/v1/users/{user_uuid}", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_200_OK
        user_data = response.json()
        assert user_data["uuid"] == user_uuid

    async def test_get_user_by_id_non_admin(
        self, client: AsyncClient, auth_token_user: tuple[str, str], test_user: dict
    ):
        user_uuid = test_user["uuid"]
        access_token, _ = auth_token_user

        response = await client.get(f"/api/v1/users/{user_uuid}", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_register_new_user(self, client: AsyncClient):
        new_user = RegisterUserRequest(
            email="test@email.com",
            first_name="User",
            last_name="test",
            password="password123",
            role=UserRole.USER,
            activated=True,
        )
        response = await client.post("/api/v1/users/", json=new_user.model_dump())
        assert response.status_code == status.HTTP_201_CREATED
        user = response.json()
        assert user["email"] == "test@email.com"
        assert user["first_name"] == "User"
        assert user["last_name"] == "test"

    async def test_register_duplicate_user(self, client: AsyncClient):
        user1 = RegisterUserRequest(
            email="test@email.com",
            first_name="User",
            last_name="test",
            password="password123",
            role=UserRole.USER,
            activated=True,
        )
        response = await client.post("/api/v1/users/", json=user1.model_dump())
        assert response.status_code == status.HTTP_201_CREATED

        user2 = RegisterUserRequest(
            email="test@email.com",
            first_name="User",
            last_name="test",
            password="password123",
            role=UserRole.USER,
            activated=True,
        )
        response = await client.post("/api/v1/users/", json=user2.model_dump())
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_update_user(self, client: AsyncClient, auth_token_user: tuple[str, str], test_user: dict):
        access_token, _ = auth_token_user
        user_uuid = test_user["uuid"]
        updated_user_data = UpdateUserRequest(
            email="updated_email@example.com",
            first_name="UpdatedFirstName",
            last_name="UpdatedLastName",
            password="UpdatedPassword123",
        )

        response = await client.put(
            f"/api/v1/users/{user_uuid}", json=updated_user_data.model_dump(), cookies={"Access-Token": access_token}
        )
        assert response.status_code == status.HTTP_200_OK

        updated_user = response.json()
        assert updated_user["email"] == "updated_email@example.com"
        assert updated_user["first_name"] == "UpdatedFirstName"
        assert updated_user["last_name"] == "UpdatedLastName"

    async def test_update_non_existent_user(self, client: AsyncClient, auth_token_user: tuple[str, str]):
        access_token, _ = auth_token_user
        non_existent_uuid = uuid4()
        updated_user_data = {
            "email": "non_existent@example.com",
            "first_name": "NonExistentFirstName",
            "last_name": "NonExistentLastName",
            "password": "NonExistentPassword",
        }

        response = await client.put(
            f"/api/v1/users/{non_existent_uuid}", json=updated_user_data, cookies={"Access-Token": access_token}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_user(self, client: AsyncClient, auth_token_user: tuple[str, str], test_user: dict):
        access_token, _ = auth_token_user
        user_uuid = test_user["uuid"]

        response = await client.delete(f"/api/v1/users/{user_uuid}", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_delete_non_existent_user(self, client: AsyncClient, auth_token_user: tuple[str, str]):
        access_token, _ = auth_token_user
        non_existent_uuid = uuid4()

        response = await client.delete(f"/api/v1/users/{non_existent_uuid}", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_404_NOT_FOUND
