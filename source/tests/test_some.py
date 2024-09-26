import sys
import pytest
from source.crud import user_account
from source.crud import integration
from secret_data import config

config.DB_NAME = "pytest_sales_bot"
config.DB_USERNAME = "pytestuser1"
config.DB_PASSWORD = "123456"

from source.database import create_all_tables, drop_all_tables, get_db
from source.models import models
from source.schemas import schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import pytest_asyncio
import asyncio
import warnings


@pytest_asyncio.fixture(scope="session")
def event_loop():
    # https://github.com/pvarki/python-rasenmaeher-api/issues/94
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    """
    Creates an instance of the default event loop for the test session.
    """
    # https://github.com/igortg/pytest-async-sqlalchemy#providing-a-session-scoped-event-loop
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # loop = asyncio.new_event_loop()
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def create_tables():
    # print("Creating all tables")
    await create_all_tables()
    yield
    # print("Dropping all tables")
    await drop_all_tables()


@pytest_asyncio.fixture
async def db():
    async for session in get_db():
        yield session


TEST_USERNAME = "testuser1"
TEST_PASSWORD = "testpass"
TEST_TASK_TITLE = "Test Task"
TEST_TASK_DESCRIPTION = "Test Description"
TEST_CRM_NAME = "Bitrix"
TEST_CRM_API_KEY = "sk-sdfssdffsf"


@pytest.mark.asyncio
async def test_create_user(db: AsyncSession):
    user = schemas.UserCreate(name=TEST_USERNAME, email="ivan@example.com", phone="1234567890", source="CRM")
    await user_account.create_user(db, user)

    result = await db.execute(select(models.User).filter(models.User.name == TEST_USERNAME))
    user = result.scalars().first()

    # print(user)

    assert user is not None
    assert user.name == TEST_USERNAME


@pytest.mark.asyncio
async def test_create_integration(db: AsyncSession):
    integration_ = schemas.IntegrationCreate(name=TEST_CRM_NAME, api_key=TEST_CRM_API_KEY)
    await integration.create_integration(db, integration_)

    result = await db.execute(select(models.Integration).filter(models.Integration.name == TEST_CRM_NAME))
    integration_ = result.scalars().first()

    # print(integration_)

    assert integration_ is not None
    assert integration_.name == TEST_CRM_NAME
