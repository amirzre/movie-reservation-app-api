from datetime import datetime
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.controllers import MovieController
from app.models import Movie
from app.repositories import MovieRepository
from core.db.session import reset_session_context, set_session_context
from core.exceptions import NotFoundException


@pytest.fixture
def movie_repository():
    """Fixture to mock MovieRepository."""
    return AsyncMock(spec=MovieRepository)


@pytest.fixture
def movie_controller(movie_repository):
    """Fixture to create an instance of MovieController with mocked repository."""
    return MovieController(movie_repository=movie_repository)


@pytest.fixture(autouse=True)
def mock_session_context():
    """Fixture to mock the session context for the tests."""
    token = set_session_context("test-session")
    yield
    reset_session_context(token)


@pytest.fixture(autouse=True)
def mock_db_session():
    """Fixture to mock database session for the tests."""
    with patch("core.db.session.get_session", new_callable=AsyncMock):
        yield


@pytest.mark.asyncio
class TestMovieController:
    async def test_get_movie_success(self, movie_controller, movie_repository):
        movie_uuid = uuid4()
        mock_movie = Movie(id=1, uuid=movie_uuid, title="title")
        movie_repository.get_by_uuid.return_value = mock_movie

        result = await movie_controller.get_movie(movie_uuid=movie_uuid)

        assert result == mock_movie
        movie_repository.get_by_uuid.assert_called_once_with(uuid=movie_uuid)

    async def test_get_movie_not_found(self, movie_controller, movie_repository):
        movie_uuid = uuid4()
        movie_repository.get_by_uuid.return_value = None

        with pytest.raises(NotFoundException):
            await movie_controller.get_movie(movie_uuid=movie_uuid)

        movie_repository.get_by_uuid.assert_called_once_with(uuid=movie_uuid)

    async def test_create_movie_success(self, movie_controller, movie_repository):
        title = "title"
        description = "description"
        genre = "action"
        release_date = datetime.now()

        mock_movie = Movie(id=1, title=title, genre=genre, release_date=release_date, description=description)
        movie_repository.create.return_value = mock_movie

        result = await movie_controller.create_movie(
            title=title,
            description=description,
            genre=genre,
            release_date=release_date,
            activated=True,
        )

        assert result == mock_movie
        movie_repository.create.assert_called_once_with(
            attributes={
                "title": title,
                "description": description,
                "genre": genre,
                "release_date": release_date,
                "activated": True,
            }
        )

    async def test_update_movie_success(self, movie_controller, movie_repository):
        movie_uuid = uuid4()
        mock_movie = Movie(
            id=1,
            uuid=movie_uuid,
            title="title",
            description="description",
            genre="action",
            release_date=datetime.now(),
            activated=True,
        )
        movie_repository.get_by_uuid.return_value = mock_movie
        movie_repository.update.return_value = mock_movie

        result = await movie_controller.update_movie(movie_uuid=movie_uuid, title="newtitle")

        mock_movie.title = "newtitle"

        assert result == mock_movie
        assert mock_movie.title == "newtitle"

        movie_repository.get_by_uuid.assert_called_once_with(uuid=movie_uuid)
        movie_repository.update.assert_called_once_with(
            model=mock_movie, attributes={"title": "newtitle", "activated": True}
        )

    async def test_update_movie_not_found(self, movie_controller, movie_repository):
        movie_uuid = uuid4()
        movie_repository.get_by_uuid.return_value = None

        with pytest.raises(NotFoundException):
            await movie_controller.update_movie(movie_uuid=movie_uuid, title="newtitle")

        movie_repository.get_by_uuid.assert_called_once_with(uuid=movie_uuid)

    async def test_delete_movie_success(self, movie_controller, movie_repository):
        movie_uuid = uuid4()
        mock_movie = Movie(
            id=1,
            uuid=movie_uuid,
            title="title",
            description="description",
            genre="action",
            release_date=datetime.now(),
            activated=True,
        )
        movie_repository.get_by_uuid.return_value = mock_movie

        await movie_controller.delete_movie(movie_uuid=movie_uuid)

        movie_repository.get_by_uuid.assert_called_once_with(uuid=movie_uuid)
        movie_repository.delete.assert_called_once_with(model=mock_movie)

    async def test_delete_movie_not_found(self, movie_controller, movie_repository):
        movie_uuid = uuid4()
        movie_repository.get_by_uuid.return_value = None

        with pytest.raises(NotFoundException):
            await movie_controller.delete_movie(movie_uuid=movie_uuid)

        movie_repository.get_by_uuid.assert_called_once_with(uuid=movie_uuid)
