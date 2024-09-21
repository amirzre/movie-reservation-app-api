from datetime import datetime, timedelta
from uuid import uuid4

import pytest
import pytest_asyncio
from faker import Faker
from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app.schemas.request import CreateMovieRequest, UpdateMovieRequest

fake = Faker()


@pytest.mark.asyncio
class TestMovieEndpoints:
    @pytest_asyncio.fixture
    async def test_movie(self, client: AsyncClient, auth_token_admin: tuple[str, str]) -> dict:
        movie_data = CreateMovieRequest(
            title=fake.name(),
            description="description",
            genre=fake.name(),
            release_date=(datetime.now() + timedelta(days=1)),
            activated=True,
        )
        movie_data = jsonable_encoder(movie_data)
        access_token, _ = auth_token_admin
        response = await client.post("/api/v1/movies/", json=movie_data, cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_201_CREATED
        return response.json()

    async def test_get_all_movies_non_admin(self, client: AsyncClient, auth_token_user: tuple[str, str]):
        access_token, _ = auth_token_user
        response = await client.get("/api/v1/movies/", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_200_OK
        movies = response.json()
        assert isinstance(movies, list)

    async def test_get_all_movies_admin(self, client: AsyncClient, auth_token_admin: tuple[str, str]):
        access_token, _ = auth_token_admin
        response = await client.get("/api/v1/movies/", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_200_OK
        movies = response.json()
        assert isinstance(movies, list)

    async def test_get_all_movies_unauthorized(self, client: AsyncClient):
        response = await client.get("/api/v1/movies/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_movie_by_id_admin(
        self, client: AsyncClient, auth_token_admin: tuple[str, str], test_movie: dict
    ):
        access_token, _ = auth_token_admin
        movie_uuid = test_movie["uuid"]

        response = await client.get(f"/api/v1/movies/{movie_uuid}", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_200_OK
        movie_data = response.json()
        assert movie_data["uuid"] == movie_uuid

    async def test_get_movie_by_id_non_admin(
        self, client: AsyncClient, auth_token_user: tuple[str, str], test_movie: dict
    ):
        access_token, _ = auth_token_user
        movie_uuid = test_movie["uuid"]

        response = await client.get(f"/api/v1/movies/{movie_uuid}", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_200_OK
        movie_data = response.json()
        assert movie_data["uuid"] == movie_uuid

    async def test_get_movie_by_id_unauthorized(self, client: AsyncClient, test_movie: dict):
        movie_uuid = test_movie["uuid"]
        response = await client.get(f"/api/v1/movies/{movie_uuid}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_create_new_movie_success(self, client: AsyncClient, auth_token_admin: tuple[str, str]):
        access_token, _ = auth_token_admin
        new_movie = CreateMovieRequest(
            title="title",
            description="description",
            genre="action",
            release_date=(datetime.now() + timedelta(days=1)),
            activated=True,
        )
        movie_data = jsonable_encoder(new_movie)
        response = await client.post("/api/v1/movies/", json=movie_data, cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_201_CREATED
        movie = response.json()
        assert movie["title"] == "title"
        assert movie["genre"] == "action"
        assert movie["activated"] is True

    async def test_create_new_movie_non_admin(self, client: AsyncClient, auth_token_user: tuple[str, str]):
        access_token, _ = auth_token_user
        new_movie = CreateMovieRequest(
            title="title",
            description="description",
            genre="action",
            release_date=(datetime.now() + timedelta(days=1)),
            activated=True,
        )
        new_movie = jsonable_encoder(new_movie)
        response = await client.post("/api/v1/movies/", json=new_movie, cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_new_movie_unauthorized(self, client: AsyncClient):
        new_movie = CreateMovieRequest(
            title="title",
            description="description",
            genre="action",
            release_date=(datetime.now() + timedelta(days=1)),
            activated=True,
        )
        new_movie = jsonable_encoder(new_movie)
        response = await client.post("/api/v1/movies/", json=new_movie)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_update_movie_success(self, client: AsyncClient, auth_token_admin: tuple[str, str], test_movie: dict):
        access_token, _ = auth_token_admin
        movie_uuid = test_movie["uuid"]
        updated_movie_data = UpdateMovieRequest(
            title="UpdatedTitle",
            description="UpdatedDescription",
            genre="UpdatedGenre",
        )

        response = await client.put(
            f"/api/v1/movies/{movie_uuid}", json=updated_movie_data.model_dump(), cookies={"Access-Token": access_token}
        )
        assert response.status_code == status.HTTP_200_OK

        updated_movie = response.json()
        assert updated_movie["title"] == "UpdatedTitle"
        assert updated_movie["description"] == "UpdatedDescription"
        assert updated_movie["genre"] == "UpdatedGenre"

    async def test_update_non_existent_movie(
        self, client: AsyncClient, auth_token_admin: tuple[str, str], test_movie: dict
    ):
        access_token, _ = auth_token_admin
        non_existent_uuid = uuid4()
        updated_movie_data = UpdateMovieRequest(
            title="NonExistentTitle",
            description="NonExistentDescription",
            genre="NonExistentGenre",
        )

        response = await client.put(
            f"/api/v1/movies/{non_existent_uuid}",
            json=updated_movie_data.model_dump(),
            cookies={"Access-Token": access_token},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_update_movie_non_admin(
        self, client: AsyncClient, auth_token_user: tuple[str, str], test_movie: dict
    ):
        access_token, _ = auth_token_user
        movie_uuid = test_movie["uuid"]
        updated_movie_data = UpdateMovieRequest(
            title="UpdatedTitle",
            description="UpdatedDescription",
            genre="UpdatedGenre",
        )

        response = await client.put(
            f"/api/v1/movies/{movie_uuid}", json=updated_movie_data.model_dump(), cookies={"Access-Token": access_token}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_update_movie_unauthorized(self, client: AsyncClient, test_movie: dict):
        movie_uuid = test_movie["uuid"]
        updated_movie_data = UpdateMovieRequest(
            title="UpdatedTitle",
            description="UpdatedDescription",
            genre="UpdatedGenre",
        )

        response = await client.put(f"/api/v1/movies/{movie_uuid}", json=updated_movie_data.model_dump())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_delete_movie_success(self, client: AsyncClient, auth_token_admin: tuple[str, str], test_movie: dict):
        access_token, _ = auth_token_admin
        movie_uuid = test_movie["uuid"]

        response = await client.delete(f"/api/v1/movies/{movie_uuid}", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_delete_movie_non_admin(
        self, client: AsyncClient, auth_token_user: tuple[str, str], test_movie: dict
    ):
        access_token, _ = auth_token_user
        movie_uuid = test_movie["uuid"]

        response = await client.delete(f"/api/v1/movies/{movie_uuid}", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_delete_non_existent_movie(self, client: AsyncClient, auth_token_admin: tuple[str, str]):
        access_token, _ = auth_token_admin
        non_existent_uuid = uuid4()

        response = await client.delete(f"/api/v1/movies/{non_existent_uuid}", cookies={"Access-Token": access_token})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_movie_unauthorized(self, client: AsyncClient):
        movie_uuid = uuid4()

        response = await client.delete(f"/api/v1/movies/{movie_uuid}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
