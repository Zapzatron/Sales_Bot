from sqlalchemy.ext.asyncio import AsyncSession
from source.models import models
from source.schemas import schemas


async def create_integration(db: AsyncSession, integration: schemas.IntegrationCreate):
    db_integration = models.Integration(name=integration.name, api_key=integration.api_key)
    db.add(db_integration)
    await db.commit()
    await db.refresh(db_integration)
    return db_integration
