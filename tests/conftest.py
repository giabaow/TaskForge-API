import os
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_project_tracker.db"
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from app.db.base import Base
from app.db.session import engine
from app.main import app


@pytest_asyncio.fixture(autouse=True)
async def database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


async def register_and_token(client, email="user@example.com", name="Test User"):
    await client.post("/api/v1/auth/register", json={"email": email, "password": "password123", "full_name": name})
    response = await client.post("/api/v1/auth/login", json={"email": email, "password": "password123"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
