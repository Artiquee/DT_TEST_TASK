from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Cat
from .schemas import SpySchemaUpdate


class CatRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_cat_by_id(self, cat_id: int) -> Cat:
        result = await self.db_session.execute(select(Cat).where(Cat.id == cat_id))
        return result.scalar_one_or_none()

    async def get_cat_by_name(self, cat_name: str) -> Cat:
        result = await self.db_session.execute(select(Cat).where(Cat.name == cat_name))
        return result.scalar_one_or_none()

    async def get_cats(self):
        result = await self.db_session.execute(select(Cat))
        return result.scalars().all()

    async def add_cat(self, cat: Cat):
        self.db_session.add(cat)
        await self.db_session.commit()
        return cat.name

    async def update_cat(self, cat: Cat, updated_data: SpySchemaUpdate) -> Cat:
        for key, value in updated_data.dict().items():
            setattr(cat, key, value)
        self.db_session.add(cat)
        await self.db_session.commit()
        await self.db_session.refresh(cat)
        return cat

    async def delete_cat(self, cat):
        await self.db_session.delete(cat)
        await self.db_session.commit()
        return True