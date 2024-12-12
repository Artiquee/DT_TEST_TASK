from fastapi import HTTPException
from starlette import status
from src.spy_cat.models import Cat
from src.spy_cat.repository import CatRepository
from src.spy_cat.schemas import SpySchemaUpdate
from src.spy_cat.utils import validate_cat_breed


class CatService:
    def __init__(self, cat_repository: CatRepository):
        self.cat_repository = cat_repository

    async def get_cat(self, cat_id):
        cat = await self.cat_repository.get_cat_by_id(cat_id)
        return cat

    async def get_cats(self):
        return await self.cat_repository.get_cats()

    async def add_cat(self, cat):
        spy_cat = Cat(
            name=cat.name,
            years_of_experience=cat.years_of_experience,
            breed=cat.breed,
            salary=cat.salary,
        )
        if await self.cat_repository.get_cat_by_name(cat.name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cat already exists")
        breeds = await validate_cat_breed(cat.breed)
        if isinstance(breeds, list) and len(breeds) > 1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Multiple similar breeds found: {breeds}")
        else:
            cat_name = await self.cat_repository.add_cat(spy_cat)
            return cat_name

    async def delete_cat(self, cat_id: int):
        existing_cat = await self.cat_repository.get_cat_by_id(cat_id=cat_id)
        print(existing_cat.id)
        if not await self.cat_repository.get_cat_by_id(cat_id):
            raise HTTPException(status_code=404, detail="Cat not found")
        delete_status = await self.cat_repository.delete_cat(existing_cat)
        return delete_status

    async def update_cat(self, cat_id, updated_cat: SpySchemaUpdate):
        cat = await self.cat_repository.get_cat_by_id(cat_id)
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        if not updated_cat.secret_access_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No secret_access_key")
        updated_cat = await self.cat_repository.update_cat(cat, updated_cat)
        return updated_cat
