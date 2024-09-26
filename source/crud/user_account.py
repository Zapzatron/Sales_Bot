from sqlalchemy.ext.asyncio import AsyncSession
from source.models import models
from source.schemas import schemas


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, phone=user.phone, source=user.source)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
