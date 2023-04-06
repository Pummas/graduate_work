import asyncio
from pathlib import Path

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient

# Для запуска тестов на хосте явно загружаем переменные окружения
# из .env.test в корневой папке до импорта приложения, так как pytest сам по умолчанию
# загружает переменные окружения из .env
base_dir = Path(__file__).parent.parent.parent
env_test = base_dir / ".env.test"
load_dotenv(env_test, override=True)

from app.db.session import async_session  # noqa: E402
from app.db.session import recreate_tables  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def session():
    async with async_session() as session_:
        yield session_


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncClient:
    async with async_session() as session:
        await recreate_tables(session)
    return AsyncClient(app=app, base_url="http://localhost:8000")
